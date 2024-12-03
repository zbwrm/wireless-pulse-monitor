import bluetooth
import time
import max30102
import numpy as np
from collections import deque
from heart_rate import HeartRate

# chosen arbitrarily; 30 heartbeats is under 30s worth of data
HB_TIMESTAMP_BUFFER_LEN = 30

# Set up the Bluetooth server
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

print("Waiting for connection...")
client_sock, address = server_sock.accept()
print(f"Connected to {address}")

heart_rate = HeartRate()

ir_buf = deque(maxlen=4)
hb_buf = deque(maxlen=HB_TIMESTAMP_BUFFER_LEN)

sensor = max30102.MAX30102()
sensor.setup(0x03)

try:
    while True:
        red_val, ir_val = sensor.read_fifo()
        ir_buf.append(ir_val)

        ir_avg = 0
        for val in ir_buf:
            ir_avg += val
        ir_avg / 4

        is_hb = heart_rate.checkForBeat(ir_avg)
        if (is_hb):
            hb_buf.append(time.time())
            print("beat!", end="  ")

            if (len(hb_buf) == HB_TIMESTAMP_BUFFER_LEN):
                tstamps = np.array(hb_buf)

                intervals = np.diff(tstamps)
                successive_differences = np.diff(intervals)
                rmssd = np.sqrt(np.sum(np.square(successive_differences)))
                NN50 = np.count_nonzero(successive_differences > 0.05) # timestamps are in seconds
                NN20 = np.count_nonzero(successive_differences > 0.02)
                pNN50 = NN50 / len(successive_differences)
                pNN20 = NN20 / len(successive_differences)

                rates = np.reciprocal(intervals) * 60
                hr_avg = np.average(rates)
                hr_std = np.std(rates)

                print(hr_avg, hr_std, rmssd)
    
                bt_string = f"{int(hr_avg)},{hr_std:.3f},{rmssd:.3f}"
                pulse_data = bt_string.encode('utf-8')
                client_sock.send(pulse_data)
                print(f"Sent: {pulse_data}")

            else:
                print(f"not enough data! need {HB_TIMESTAMP_BUFFER_LEN - len(hb_buf)} more beats")
        
        # maybe remove/adjust this -- needs testing
        time.sleep(0.025)
except Exception as e:
    print(f"Error: {e}")
finally:
    client_sock.close()
    server_sock.close()
