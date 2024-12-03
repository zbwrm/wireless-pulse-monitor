#   Isaiah Cabugos

import tkinter as tk
from tkinter import messagebox
from random import randint, random
import bluetooth
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from time import time, sleep

class PGM_GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("PGM Monitor")

        self.loading_canvas = tk.Canvas()
        self.is_loading = False
        self.loading_loops = 0
        self.load_state = 0
        self.canvas_ID1 = 0
        self.canvas_ID2 = 0
        self.canvas_ID3 = 0

        self.background_frame = tk.Frame(self.root)
        self.bpm = tk.IntVar()
        self.ipm = tk.IntVar()
        self.hrstd = tk.StringVar()
        self.rmssd = tk.StringVar()

        self.button_frame = tk.Frame(self.root, pady= 250)
        #self.button_frame.configure()
        self.start_button = tk.Button(self.button_frame, text="Start", font=('Comic Sans', 18), command=self.start_pressed)
        self.start_button.pack()

        #   =====   Bluetooth   =====
        self.server_address = "2C:CF:67:03:0B:77"
        self.port = 1

        self.client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.data = 0
        self.decoded_data = 0
        self.metrics = 0
        #   =====   END Bluetooth   =====

        #   =====   Graphing    =====
        # Data storage for graphing
        self.timestamps = []
        self.hr_averages = []  # Heart rate averages
        self.hr_stds = []  # Heart rate standard deviations
        self.rmssds = []  # RMSSD (Root Mean Square of Successive Differences)

        # Start the Matplotlib figure
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Heart Rate Metrics Over Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Metrics")
        self.line_hr_avg, = self.ax.plot([], [], label="HR Avg (bpm)", color="red")
        self.line_hr_std, = self.ax.plot([], [], label="HR Std (bpm)", color="blue")
        self.line_rmssd, = self.ax.plot([], [], label="RMSSD", color="green")
        self.ax.legend()

        self.start_time = time()

        #   =====   END Graphing    =====
        self.button_frame.pack(fill='both')

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def start_pressed(self):
        self.button_frame.destroy()
        self.begin()

    def loading(self):
        canv_height = self.loading_canvas.winfo_height()
        if self.loading_loops < 1:
            self.update_graph()

        if self.is_loading:
            match self.load_state:
                case 0:
                    self.canvas_ID1 = self.loading_canvas.create_arc((150, 250), (250, 664 - 250), style=tk.ARC, start=-55,
                                                   extent=145, width=14, outline="#0000AA")
                case 1:
                    self.canvas_ID2 = self.loading_canvas.create_arc((350, 200), (500, 664 - 200), style=tk.ARC, start=-75,
                                                   extent=165, width=14, outline="#0000AA")
                    self.loading_canvas.itemconfig(self.canvas_ID1, outline="#BBBBFF")
                case 2:
                    self.canvas_ID3 = self.loading_canvas.create_arc((550, 150), (750, 664 - 150), style=tk.ARC, start=-90,
                                                   extent=180, width=14, outline="#0000AA")
                    self.loading_canvas.itemconfig(self.canvas_ID2, outline="#BBBBFF")
                case 3:
                    self.loading_loops = self.loading_loops + 1
                    self.loading_canvas.delete(self.canvas_ID1)
                    self.loading_canvas.delete(self.canvas_ID2)
                    self.loading_canvas.delete(self.canvas_ID3)
            self.load_state = self.load_state + 1
            self.load_state = self.load_state % 4
            self.loading_canvas.after(ms=500, func=self.loading)
        else:
            self.loading_canvas.destroy()
        self.loading_loops = self.loading_loops + 1


    def begin(self):

        self.background_frame.config(pady=50)
        self.background_frame.columnconfigure(index=0, weight=1)
        self.background_frame.columnconfigure(index=1, weight=1)
        self.background_frame.columnconfigure(index=2, weight=1)
        self.background_frame.columnconfigure(index=3, weight=1)
        self.background_frame.grid_rowconfigure(index=0, weight=1)
        self.background_frame.grid_rowconfigure(index=1, weight=1)
        self.background_frame.grid_rowconfigure(index=2, weight=1)

        self.reset()

        bpm_label = tk.Label(self.background_frame, text="BPM", font=("Comic Sans", 18))
        hrstd_label = tk.Label(self.background_frame, text="HRSTD", font=("Comic Sans", 18))
        rmssd_label = tk.Label(self.background_frame, text="RMSSD", font=("Comic Sans", 18))
        bpm_label.grid(row=1, column=0, sticky=tk.W + tk.E)
        hrstd_label.grid(row=1, column=1, sticky=tk.W + tk.E)
        rmssd_label.grid(row=1, column=2, sticky=tk.W + tk.E)

        bpm_entry = tk.Entry(self.background_frame, textvariable=self.bpm, font=("Gothic", 18))
        hrstd_entry = tk.Entry(self.background_frame, textvariable=self.hrstd, font=("Gothic", 18))
        rmssd_entry = tk.Entry(self.background_frame, textvariable=self.rmssd, font=("Gothic", 18))
        bpm_entry.grid(row=2, column=0, sticky=tk.W+tk.E)
        hrstd_entry.grid(row=2, column=1, sticky=tk.W + tk.E)
        rmssd_entry.grid(row=2, column=2, sticky=tk.W + tk.E)

        begin_button = tk.Button(self.background_frame, text="Begin Collection", font=('Helvetica', 14), command=self.collect_data)
        end_button = tk.Button(self.background_frame, text="Reset Collection", font=('Helvetica', 14), command=self.reset)
        exit_button = tk.Button(self.background_frame, text="Exit Program", font=('Helvetica', 14), command=self.on_closing)

        begin_button.grid(row=3, column=0, sticky=tk.W + tk.E, pady=40)
        end_button.grid(row=3, column=1, sticky=tk.W + tk.E, pady=40)
        exit_button.grid(row=3, column=2, sticky=tk.W + tk.E, pady=40)

        self.background_frame.pack(fill='x')

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        self.graphing_canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.graphing_canvas.draw()

        # placing the canvas on the Tkinter window
        self.graphing_canvas.get_tk_widget().pack()


    def collect_data(self):
        # Connect to the server
        self.client_sock.connect((self.server_address, self.port))
        print("Connected to server")

        self.loading_canvas = tk.Canvas(self.root, width=1000, height=660, bg='white')
        self.loading_canvas.pack(anchor=tk.CENTER, expand=True)
        self.is_loading = True

        self.loading()

        bpm = randint(60, 210)
        hrstd = random() * randint(0, 100)
        rmssd = random() * randint(0, 100)

        self.bpm.set(bpm)
        self.hrstd.set('{:.2f}'.format(hrstd))
        self.rmssd.set('{:.2f}'.format(rmssd))

    def update_graph(self):
        self.data = self.client_sock.recv(1024)
        if self.data:
            self.is_loading = False
            try:
                # Decode and unpack the received data (example structure)
                self.decoded_data = self.data.decode("utf-8")
                self.metrics = self.decoded_data.split(",")
                sample_time = float(self.metrics[0])
                hr_avg = int(self.metrics[1])
                hr_std = float(self.metrics[2])
                rmssd = float(self.metrics[3])

                # Update graphing data
                self.current_time = time() - self.start_time
                self.timestamps.append(sample_time)
                self.hr_averages.append(hr_avg)
                self.hr_stds.append(hr_std)
                self.rmssds.append(rmssd)

                # Update GUI data
                self.bpm.set(hr_avg)
                self.hrstd.set('{:.2f}'.format(hr_std))
                self.rmssd.set('{:.2f}'.format(rmssd))

                # Limit to the last 100 points
                if len(self.timestamps) > 100:
                    self.timestamps.pop(0)
                    self.hr_averages.pop(0)
                    self.hr_stds.pop(0)
                    self.rmssds.pop(0)

                # Update the lines
                self.line_hr_avg.set_data(self.timestamps, self.hr_averages)
                self.line_hr_std.set_data(self.timestamps, self.hr_stds)
                self.line_rmssd.set_data(self.timestamps, self.rmssds)

                # Adjust the axes
                self.ax.relim()
                self.ax.autoscale_view()

                self.graphing_canvas.draw()

                self.root.after(50, self.update_graph)

            except Exception as e:
                print(f"Error processing data: {e}")

    def reset(self):
        self.timestamps = []
        self.hr_averages = []  # Heart rate averages
        self.hr_stds = []  # Heart rate standard deviations
        self.rmssds = []  # RMSSD (Root Mean Square of Successive Differences)

        # Decode and unpack the received data (example structure)
        hr_avg_val = int(0)
        hr_std_val = float(0)
        rmssd_val = float(0)

        self.bpm.set(hr_avg_val)
        self.hrstd.set('{:.2f}'.format(hr_std_val))
        self.rmssd.set('{:.2f}'.format(rmssd_val))

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()

PGM_GUI()