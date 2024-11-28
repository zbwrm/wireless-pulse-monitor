import time
import max30102
from collections import deque
from heart_rate import HeartRate

sensor = max30102.MAX30102()
heart_rate = HeartRate()

ir_buf = deque(maxlen=4)

if __name__ == "__main__":
    sensor.setup(0x03)

    while (1):
        red_val, ir_val = sensor.read_fifo()
        ir_buf.append(ir_val)

        ir_avg = 0
        for val in ir_buf:
            ir_avg += val
        ir_avg / 4

        is_hb = heart_rate.checkForBeat(ir_avg)
        if (is_hb):
            print(f"beat! @ {time.time()}")

        time.sleep(0.02)
