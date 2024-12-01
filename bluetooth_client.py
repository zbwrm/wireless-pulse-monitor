import bluetooth
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from time import time

# Bluetooth setup
server_address = "2C:CF:67:03:0B:77"
port = 1

client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# Data storage for graphing
timestamps = []
hr_averages = []  # Heart rate averages
hr_stds = []      # Heart rate standard deviations
rmssds = []       # RMSSD (Root Mean Square of Successive Differences)

try:
    # Connect to the server
    client_sock.connect((server_address, port))
    print("Connected to server")

    # Start the Matplotlib figure
    fig, ax = plt.subplots()
    ax.set_title("Heart Rate Metrics Over Time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Metrics")
    line_hr_avg, = ax.plot([], [], label="HR Avg (bpm)", color="red")
    line_hr_std, = ax.plot([], [], label="HR Std (bpm)", color="blue")
    line_rmssd, = ax.plot([], [], label="RMSSD", color="green")
    ax.legend()

    start_time = time()

    def update(frame):
        data = client_sock.recv(1024)
        if data:
            try:
                # Decode and unpack the received data (example structure)
                decoded_data = data.decode("utf-8")
                metrics = decoded_data.split(",")
                hr_avg = float(metrics[0])
                hr_std = float(metrics[1])
                rmssd = float(metrics[2])

                # Update graphing data
                current_time = time() - start_time
                timestamps.append(current_time)
                hr_averages.append(hr_avg)
                hr_stds.append(hr_std)
                rmssds.append(rmssd)

                # Limit to the last 100 points
                if len(timestamps) > 100:
                    timestamps.pop(0)
                    hr_averages.pop(0)
                    hr_stds.pop(0)
                    rmssds.pop(0)

                # Update the lines
                line_hr_avg.set_data(timestamps, hr_averages)
                line_hr_std.set_data(timestamps, hr_stds)
                line_rmssd.set_data(timestamps, rmssds)

                # Adjust the axes
                ax.relim()
                ax.autoscale_view()

            except Exception as e:
                print(f"Error processing data: {e}")

    # Set up the animation
    ani = FuncAnimation(fig, update, interval=100)  # Update every 100ms
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Error: {e}")
finally:
    client_sock.close()
