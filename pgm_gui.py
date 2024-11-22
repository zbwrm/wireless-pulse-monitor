#   Isaiah Cabugos

import tkinter as tk
from tkinter import messagebox
from random import randint, random

class PGM_GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("PGM Monitor")

        self.background_frame = tk.Frame(self.root)
        self.bpm = tk.IntVar()
        self.ipm = tk.IntVar()
        self.hrstd = tk.DoubleVar()
        self.rmssd = tk.DoubleVar()

        self.button_frame = tk.Frame(self.root)
        #self.button_frame.configure()
        self.start_button = tk.Button(self.button_frame, text="Start", font=('Comic Sans', 18), command=self.start_pressed)
        self.start_button.pack()

        self.button_frame.pack(fill='both')

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def start_pressed(self):
        self.button_frame.destroy()
        self.begin()

    def begin(self):
        self.background_frame.columnconfigure(index=0, weight=1)
        self.background_frame.columnconfigure(index=1, weight=1)
        self.background_frame.columnconfigure(index=2, weight=1)
        self.background_frame.columnconfigure(index=3, weight=1)
        self.background_frame.grid_rowconfigure(index=0, weight=1)
        self.background_frame.grid_rowconfigure(index=1, weight=1)
        self.background_frame.grid_rowconfigure(index=2, weight=1)
        self.bpm.set(0)
        self.ipm.set(0)
        self.hrstd.set(0.0)
        self.rmssd.set(0.0)

        bpm_label = tk.Label(self.background_frame, text="BPM", font=("Comic Sans", 18))
        ipm_label = tk.Label(self.background_frame, text="IPM", font=("Comic Sans", 18))
        hrstd_label = tk.Label(self.background_frame, text="HRSTD", font=("Comic Sans", 18))
        rmssd_label = tk.Label(self.background_frame, text="RMSSD", font=("Comic Sans", 18))
        bpm_label.grid(row=1, column=0, sticky=tk.W+tk.E)
        ipm_label.grid(row=1, column=1, sticky=tk.W + tk.E)
        hrstd_label.grid(row=1, column=2, sticky=tk.W + tk.E)
        rmssd_label.grid(row=1, column=3, sticky=tk.W + tk.E)

        bpm = tk.Label(self.background_frame, textvariable=self.bpm, font=("Gothic", 18))
        ipm = tk.Label(self.background_frame, textvariable=self.ipm, font=("Gothic", 18))
        hrstd = tk.Label(self.background_frame, textvariable=self.hrstd, font=("Gothic", 18))
        rmssd = tk.Label(self.background_frame, textvariable=self.rmssd, font=("Gothic", 18))
        bpm.grid(row=2, column=0, sticky=tk.W+tk.E)
        ipm.grid(row=2, column=1, sticky=tk.W + tk.E)
        hrstd.grid(row=2, column=2, sticky=tk.W + tk.E)
        rmssd.grid(row=2, column=3, sticky=tk.W + tk.E)

        begin_button = tk.Button(self.background_frame, text="Begin Collection", font=('Helvetica', 14), command=self.collect_data)
        end_button = tk.Button(self.background_frame, text="Reset Collection", font=('Helvetica', 14), command=self.reset)
        exit_button = tk.Button(self.background_frame, text="Exit Program", font=('Helvetica', 14), command=self.on_closing)

        begin_button.grid(row=3, column=0, sticky=tk.W + tk.E, pady=40)
        end_button.grid(row=3, column=1, sticky=tk.W + tk.E, pady=40)
        exit_button.grid(row=3, column=3, sticky=tk.W + tk.E, pady=40)

        self.background_frame.pack(fill='x')

    def collect_data(self):
        self.bpm.set(randint(60, 210))
        self.ipm.set(randint(60, 210))
        self.hrstd.set(random() * randint(0, 100))
        self.rmssd.set(random() * randint(0, 100))

    def reset(self):
        self.bpm.set(0)
        self.ipm.set(0)
        self.hrstd.set(0.0)
        self.rmssd.set(0.0)

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()

PGM_GUI()