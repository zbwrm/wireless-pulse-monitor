#   Isaiah Cabugos

import tkinter as tk
from tkinter import messagebox
from random import randint, random

class PGM_GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("PGM Monitor")

        self.loading_canvas = tk.Canvas()

        self.background_frame = tk.Frame(self.root)
        self.bpm = tk.IntVar()
        self.ipm = tk.IntVar()
        self.hrstd = tk.StringVar()
        self.rmssd = tk.StringVar()

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

    def loading(self):
        self.loading_canvas = tk.Canvas(self.root, width=1000, height=660, bg='white')
        self.loading_canvas.pack(anchor=tk.CENTER, expand=True)
        data_loading = True
        load_state = 0
        canv_height = self.loading_canvas.winfo_height()

        canvas_ID1 = 0
        canvas_ID2 = 0
        canvas_ID3 = 0
        while data_loading:
            match load_state:
                case 0:
                    canvas_ID1 = self.loading_canvas.create_arc((100, 250), (200, canv_height - 250), style=tk.ARC, start=-90,
                                                   extent=180, width=4)
                    self.loading_canvas.delete(canvas_ID2)
                    self.loading_canvas.delete(canvas_ID3)
                case 1:
                    canvas_ID2 = self.loading_canvas.create_arc((200, 250), (300, canv_height - 250), style=tk.ARC, start=-90,
                                                   extent=180, width=4)
                case 2:
                    canvas_ID3 = self.loading_canvas.create_arc((300, 250), (400, canv_height - 250), style=tk.ARC, start=-90,
                                                   extent=180, width=4)
            load_state = load_state + 1
            load_state = load_state % 3

    def begin(self):
        self.background_frame.columnconfigure(index=0, weight=1)
        self.background_frame.columnconfigure(index=1, weight=1)
        self.background_frame.columnconfigure(index=2, weight=1)
        self.background_frame.columnconfigure(index=3, weight=1)
        self.background_frame.grid_rowconfigure(index=0, weight=1)
        self.background_frame.grid_rowconfigure(index=1, weight=1)
        self.background_frame.grid_rowconfigure(index=2, weight=1)

        self.reset()

        bpm_label = tk.Label(self.background_frame, text="BPM", font=("Comic Sans", 18))
        ipm_label = tk.Label(self.background_frame, text="IPM", font=("Comic Sans", 18))
        hrstd_label = tk.Label(self.background_frame, text="HRSTD", font=("Comic Sans", 18))
        rmssd_label = tk.Label(self.background_frame, text="RMSSD", font=("Comic Sans", 18))
        bpm_label.grid(row=1, column=0, sticky=tk.W+tk.E)
        ipm_label.grid(row=1, column=1, sticky=tk.W + tk.E)
        hrstd_label.grid(row=1, column=2, sticky=tk.W + tk.E)
        rmssd_label.grid(row=1, column=3, sticky=tk.W + tk.E)

        bpm_entry = tk.Entry(self.background_frame, textvariable=self.bpm, font=("Gothic", 18))
        ipm_entry = tk.Entry(self.background_frame, textvariable=self.ipm, font=("Gothic", 18))
        hrstd_entry = tk.Entry(self.background_frame, textvariable=self.hrstd, font=("Gothic", 18))
        rmssd_entry = tk.Entry(self.background_frame, textvariable=self.rmssd, font=("Gothic", 18))
        bpm_entry.grid(row=2, column=0, sticky=tk.W+tk.E)
        ipm_entry.grid(row=2, column=1, sticky=tk.W + tk.E)
        hrstd_entry.grid(row=2, column=2, sticky=tk.W + tk.E)
        rmssd_entry.grid(row=2, column=3, sticky=tk.W + tk.E)

        begin_button = tk.Button(self.background_frame, text="Begin Collection", font=('Helvetica', 14), command=self.collect_data)
        end_button = tk.Button(self.background_frame, text="Reset Collection", font=('Helvetica', 14), command=self.reset)
        exit_button = tk.Button(self.background_frame, text="Exit Program", font=('Helvetica', 14), command=self.on_closing)

        begin_button.grid(row=3, column=0, sticky=tk.W + tk.E, pady=40)
        end_button.grid(row=3, column=1, sticky=tk.W + tk.E, pady=40)
        exit_button.grid(row=3, column=3, sticky=tk.W + tk.E, pady=40)

        self.background_frame.pack(fill='x')

    def collect_data(self):
        bpm = randint(60, 210)
        ipm = randint(60, 210)
        hrstd = random() * randint(0, 100)
        rmssd = random() * randint(0, 100)


        self.bpm.set(bpm)
        self.ipm.set(ipm)
        self.hrstd.set('{:.2f}'.format(hrstd))
        self.rmssd.set('{:.2f}'.format(rmssd))

    def reset(self):
        bpm = 0
        ipm = 0
        hrstd = 0.00
        rmssd = 0.00

        self.bpm.set(bpm)
        self.ipm.set(ipm)
        self.hrstd.set('{:.2f}'.format(hrstd))
        self.rmssd.set('{:.2f}'.format(rmssd))

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()

PGM_GUI()