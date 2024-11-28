import time
import max30102
import numpy as np
from collections import deque
from heart_rate import HeartRate

# chosen arbitrarily; 30 heartbeats is under 30s worth of data
HB_TIMESTAMP_BUFFER_LEN = 30

sensor = max30102.MAX30102()
heart_rate = HeartRate()

ir_buf = deque(maxlen=4)
hb_buf = deque(maxlen=HB_TIMESTAMP_BUFFER_LEN)

if __name__ == "__main__":
    sensor.setup(0x03)

    while (1):
        red_val, ir_val = sensor.read_fifo()
        ir_buf.append(ir_val)

        ir_avg = 0
        for val in ir_buf:
            ir_avg += val
        ir_avg / 4

        is_hb = heart_rate.checkForBeat(ir_val)
        if (is_hb):
            hb_buf.append(time.time())
            print("beat!", end="  ")

            if (len(hb_buf) == HB_TIMESTAMP_BUFFER_LEN):
                tstamps = np.array(hb_buf)
                intervals = np.diff(tstamps)
                rates = np.reciprocal(intervals) * 60
                hr_avg = np.average(rates)
                hr_std = np.std(rates)
                rmssd = np.sqrt(np.sum(np.square(intervals)))
                print(hr_avg, hr_std, rmssd)
    
                # TODO: NN50/20, pNN50/20

                # if time >= packet_period:
                    # pack + send BT packet
            else:
                print(f"not enough data! need {HB_TIMESTAMP_BUFFER_LEN - len(hb_buf)} more beats")
        

        # maybe remove/adjust this -- needs testing
        time.sleep(0.025)
