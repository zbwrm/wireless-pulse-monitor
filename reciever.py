# import pgm_gui
import max30102

sensor = max30102.MAX30102()
# gui = pgm_gui.PGM_GUI()


if __name__ == "__main__":
    sensor.setup(0x03)

    while (1):
        red_buf, ir_buf = sensor.read_fifo()
        print(red_buf, ir_buf)
