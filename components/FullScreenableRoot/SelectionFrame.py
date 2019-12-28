
from tkinter import ttk



class SelectionFrame(ttk.Frame):
    def __init__(self, container,  **args):
        super().__init__(container)
        self.boxName = ttk.Label(self, text=args["fieldname"], )
        self.boxName.grid(row=0, column=0, padx=(0,10))
        self.selectionBox = ttk.Combobox(self, textvariable=args["textvariable"])
        self.selectionBox.grid(row=0, column=1)
        self.selectionBox["state"] = "readonly"
        self.selectionBox["values"] = args["values"]