from PIL import Image, ImageTk
import tkinter as tk
import math
import asyncio
from .MainCanvasFrame import MainCanvasFrame
from .PrintScreenFrame import PrintScreenFrame
from .utils import google_image_to_string, imageToString, crop_range_handler, create
from desktopmagic.screengrab_win32 import (getDisplayRects, getRectAsImage)




class FullScreenableRoot(tk.Tk):
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.state = {}
        self.state["lang"] = tk.StringVar(value="chi_tra+eng")
        self.state["display_index"] = tk.StringVar(value="1")
        self.title("Text Capture")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.bind("<Control-Shift-C>", self.toggle_fullscreen)
        self.is_fullscreen = True
        self.crop_start = [0, 0]
        self.crop_end = [0, 0]
        self.tkimage = ""
        self.prevRectangle=None
        self.anchor = "nw"
        self.photoImageOverlay = ""
        self.crop_cancel = False

        self.printScreenFrame = create(PrintScreenFrame(self), row=0, column=0, sticky="nesw")
        """ 
        instead of writing:
        self.printScreenFrame = PrintScreenFrame(self)
        self.printScreenFrame.grid(row=0, column=0, sticky="nesw")
        and for further configuration we use self.printScreenFrame.configure(kwargs).
        """
        self.mainCanvasFrame = create(MainCanvasFrame(self), row=0, column=0, sticky="nesw")
        self.mainCanvasFrame.screenShotButton.configure(
            command = self.takeScreenShot
        )

        self.init_cropping()
        self.bind("<Escape>", self.quit_screenshot)

    def quit_screenshot(self, event):
        self.printScreenFrame.overlayScreenLabel_canvas.delete("all")
        self.mainCanvasFrame.tkraise()
        if self.printScreenFrame.overlayScreenLabel_canvas.isPressed:
            self.crop_cancel = True
        self.attributes("-fullscreen", False)





    def determine_anchor(self, x1, y1, x2, y2):
        try:
            degree = math.degrees(math.atan2(y2-y1,x2-x1))
            if 0 <= degree < 90:
                self.anchor="nw"
            if 90 <= degree < 180:
                self.anchor= "ne"
            if -180 <= degree < -90:
                self.anchor="se"
            if -90 <= degree < 0:
                self.anchor="sw"
        except Exception as e:
            print(e)

    def takeScreenShot(self):
        screen_rectangles = getDisplayRects()
        numberOfScreens = len(screen_rectangles)
        screenIndex = min(int(self.state["display_index"].get()) - 1, numberOfScreens)
        image = getRectAsImage(screen_rectangles[screenIndex]).convert("RGBA")
        self.state["imageProcessing"] = image
        self.state["imageProcessing"] = image
        self.mainCanvasFrame.text.delete("1.0", "end")
        self.attributes("-fullscreen", True)
        self.tkimage = ImageTk.PhotoImage(image)
        self.printScreenFrame.tkraise()
        self.printScreenFrame.overlayScreenLabel_canvas.config(width=screen_rectangles[screenIndex][0],
                                                               height=screen_rectangles[screenIndex][1])
        self.printScreenFrame.overlayScreenLabel_canvas.create_image(0, 0, anchor="nw", image=self.tkimage)



    def init_cropping(self):
        self.printScreenFrame.overlayScreenLabel_canvas.bind("<B1-Motion>", self.onMouseDown_fullscreen)
        self.printScreenFrame.overlayScreenLabel_canvas.bind("<ButtonRelease-1>", self.onMouseRelease_fullScreen)
        self.printScreenFrame.overlayScreenLabel_canvas.configure(cursor="tcross")

    def onMouseDown_fullscreen(self, event):
        if self.printScreenFrame.overlayScreenLabel_canvas.isPressed == False:
            self.crop_start = [event.x, event.y]
            self.printScreenFrame.overlayScreenLabel_canvas.isPressed = True

        overlay = Image.new(
            'RGBA', (abs(event.x - self.crop_start[0]), abs(event.y - self.crop_start[1])), (255, 0, 0, int(0.4*255))
        )
        self.photoImageOverlay = ImageTk.PhotoImage(overlay)

        try:
            self.printScreenFrame.overlayScreenLabel_canvas.delete(self.prevRectangle)
        except Exception as e:
            print(e)
        finally:
            self.determine_anchor(self.crop_start[0],self.crop_start[1],event.x, event.y)
            self.prevRectangle = self.printScreenFrame.overlayScreenLabel_canvas.create_image(self.crop_start[0], self.crop_start[1], anchor=self.anchor, image=self.photoImageOverlay)





    def onMouseRelease_fullScreen(self, event):
        if self.crop_cancel:
            self.crop_cancel = False
            self.printScreenFrame.overlayScreenLabel_canvas.isPressed = False
            return
        self.printScreenFrame.overlayScreenLabel_canvas.isPressed = False
        if abs(event.x - self.crop_start[0]) < 15 or abs(event.y - self.crop_start[1]) < 15:
            self.printScreenFrame.overlayScreenLabel_canvas.delete(self.prevRectangle)
            return
        else:
            self.crop_end = [event.x, event.y]
            selectionTurple = (
                self.crop_start[0], self.crop_start[1],
                self.crop_end[0], self.crop_end[1]
            )
            selectionTurple = crop_range_handler(self.crop_start, self.crop_end)

            if selectionTurple[0] != selectionTurple[2] and selectionTurple[1] != selectionTurple[3]:
                image = self.state["imageProcessing"].crop(selectionTurple)
                self.state["imageProcessing"] = image
                self.mainCanvasFrame.input_into_imageLabel(image)
                self.end_fullscreen()
                self.mainCanvasFrame.tkraise()
                capturedText_task = imageToString(image)
                self.mainCanvasFrame.text.delete("1.0", "end")
                self.mainCanvasFrame.text.insert("1.0", data.resuul)
                return



    def toggle_fullscreen(self, event=None):
        if self.is_fullscreen:
            self.start_fullscreen()
        else:
            self.end_fullscreen()

    def start_fullscreen(self):
        self.attributes("-fullscreen", True)
        self.is_fullscreen = not self.is_fullscreen

    def end_fullscreen(self):
        self.attributes("-fullscreen", False)
        self.is_fullscreen = not self.is_fullscreen
