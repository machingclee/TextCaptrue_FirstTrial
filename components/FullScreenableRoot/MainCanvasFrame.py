import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from tkinter import filedialog
from tkinter import ttk
from .utils import imageToString, crop_range_handler
from .SelectionFrame import SelectionFrame



class MainCanvasFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, sticky="nesw")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.crop_start = [0,0]
        self.crop_end = [0,0]
        self.mainCanvas = tk.Canvas(self)
        self.mainCanvas.grid(
            row=0,
            column=0,
            sticky="nesw"
        )

        self.mainCanvas.bind('<Enter>', self.bound_to_mousewheel)
        self.mainCanvas.bind('<Leave>', self.unbound_to_mousewheel)

        self.main = ttk.Frame(self.mainCanvas, padding=(30, 15))
        self.scollableTextFrame = ttk.Frame(self.main)
        self.scollableTextFrame.grid(row=4, sticky="nw")
        self.text = tk.Text(self.scollableTextFrame)
        self.text.grid(row=0,column=0,sticky="nsew")
        self.vbar = ttk.Scrollbar(self, orient="vertical", command=self.mainCanvas.yview)
        self.hbar = ttk.Scrollbar(self, orient="horizontal", command=self.mainCanvas.xview)
        self.vbar.grid(row=0, column=1, sticky="nesw")
        self.hbar.grid(row=1, column=0, sticky="sew")
        self.mainCanvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set,
                              scrollregion=(0, 0, 2000, 2000))

        # self.uploadButton = ttk.Button(self.main, text="import an image", command=self.uploadAction)
        # self.uploadButton.grid(row=1, pady=10, sticky="nw")
        self.screenShotButton = ttk.Button(
            self.main,
            text="take a screenshot"
        )
        self.screenShotButton.grid(row=2, pady=10, sticky="nw")
        self.mainCanvas.create_window((0, 0), window=self.main, anchor="nw")

        self.text.columnconfigure(0,weight=1)
        self.text.rowconfigure(0, weight=1)
        self.scrollBar = ttk.Scrollbar(self.scollableTextFrame, command=self.text.yview)
        self.scrollBar.grid(row=1,column=1,sticky="nsew")
        self.text.configure(yscrollcommand=self.scrollBar.set)

        self.text.bind('<Enter>', self.bound_to_mousewheel_textFrame)
        self.text.bind('<Leave>', self.unbound_to_mousewheel_textFrame)

        self.imageLabel = ttk.Label(self.main)
        self.imageLabel.grid(row=3, pady=10, sticky="nw")
        self.imageLabel.isPressed = False
        self.init_cropping()

        # self.selection_frame_language = \
        #     SelectionFrame(
        #         self.main,
        #         fieldname = "language",
        #         textvariable = self.master.state["lang"],
        #         values = ("chi_tra+eng", "jpn+eng")
        #     )
        # self.selection_frame_language.grid(
        #     row=0,
        #     column=0,
        #     sticky="nw"
        # )

        # self.selection_frame_language.bind("<<ComboboxSelected>>", self.handle_selection_language)

        self.selection_frame_display = \
            SelectionFrame(
                self.main,
                fieldname = "display",
                textvariable = self.master.state["display_index"],
                values = ("1", "2")
            )
        self.selection_frame_display.grid(
            row=1,
            column=0,
            sticky="nw",
            pady=10
        )
        # self.selection_frame_language.bind("<<ComboboxSelected>>", self.handle_selection_display)

    # def handle_selection_language(self, event):
    #     currentSelection = self.selection_frame_language.get()
    #     self.master.state["display_index"].set(currentSelection)

    def handle_selection_display(self, event):
        currentSelection = self.selection_frame_display.get()
        self.master.state["display_index"].set(currentSelection)

    def uploadAction(self):
        filename = filedialog.askopenfilename()
        image = Image.open(filename)
        self.master.state["imageProcessing"] = image.convert("RGBA")
        capturedText = imageToString( image=image)
        self.text.delete("1.0", "end")
        self.text.insert("1.0", capturedText)
        self.input_into_imageLabel(image)

    def input_into_imageLabel (self, image):
        tkimage = ImageTk.PhotoImage(image)
        self.imageLabel.configure(image=tkimage)
        self.imageLabel.image = tkimage

    def bound_to_mousewheel(self, event):
        self.mainCanvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def unbound_to_mousewheel(self, event):
        self.mainCanvas.unbind_all("<MouseWheel>")

    def bound_to_mousewheel_textFrame(self, event):
        self.text.bind_all("<MouseWheel>", self.on_mousewheel_textFrame)
        self.unbound_to_mousewheel(event)

    def unbound_to_mousewheel_textFrame(self, event):
        self.text.unbind_all("<MouseWheel>")
        self.bound_to_mousewheel(event)


    def on_mousewheel_textFrame(self, event):
        self.mainCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_mousewheel(self, event):
        self.mainCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def init_cropping(self):
        self.imageLabel.bind("<B1-Motion>", self.onMouseDown)
        self.imageLabel.bind("<ButtonRelease-1>", self.onMouseRelease)
        self.imageLabel.configure(cursor="tcross")

    def onMouseDown(self, event):
        if self.imageLabel.isPressed == False:
            self.crop_start = [event.x, event.y]
            self.imageLabel.isPressed = True

        overlay = Image.new(
            'RGBA', self.master.state["imageProcessing"].size, (255, 0, 0, 0)
        )

        drawer = ImageDraw.Draw(overlay)
        drawer.rectangle(
            [
                (self.crop_start[0],self.crop_start[1]),
                 (event.x, event.y)
            ],
            fill=(255, 0, 0, int(255 * 0.4))
        )

        img = Image.alpha_composite(self.master.state["imageProcessing"], overlay)
        tkimage = ImageTk.PhotoImage(img)
        self.imageLabel.configure(image=tkimage)
        self.imageLabel.image = tkimage

    def onMouseRelease(self, event):
        self.imageLabel.isPressed = False
        self.imageLabel.image = ""
        self.crop_end = [event.x, event.y]
        selectionTurple = crop_range_handler(self.crop_start,self.crop_end)

        if selectionTurple[0] != selectionTurple[2] and selectionTurple[1] != selectionTurple[3]:
            image = self.master.state["imageProcessing"].crop(selectionTurple)
            self.master.state["imageProcessing"] = image
            self.input_into_imageLabel(image)
            capturedText = imageToString(image=image)
            self.text.delete("1.0", "end")
            self.text.insert("1.0", capturedText)
            return