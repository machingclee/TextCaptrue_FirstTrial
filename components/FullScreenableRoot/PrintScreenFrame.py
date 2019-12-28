import tkinter as tk
from .utils import create


class PrintScreenFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.overlayScreenLabel_canvas = create(tk.Canvas(self), row=0, column=0, sticky="nesw")

        self.overlayScreenLabel_canvas.isPressed = False
        self.crop_start = [0,0]
        self.crop_end = [0,0]