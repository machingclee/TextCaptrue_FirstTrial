from PIL import ImageEnhance, ImageOps

import io
from google.cloud import vision
from google.cloud.vision import types



def google_image_to_string(PIL_img):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    # Convert Pillow image into bytes
    imgByteArr = io.BytesIO()
    PIL_img.save(imgByteArr, format='PNG')
    image = types.Image(content=imgByteArr.getvalue())

    # Performs label detection on the image file
    try:
        response = client.text_detection(image=image)
        texts = response.text_annotations
        return texts[0].description
    except Exception as e:
        print("error", e)
        return "no text detected, please try again."

def reverseBlackWhite(image):
    inverted_image = ImageOps.invert(image)
    return inverted_image

# environment variable:
# funcs = reverseBlackWhite

def imageProcessingMethod(image):
    enhancer_brightness = ImageEnhance.Brightness(image)
    image = enhancer_brightness.enhance(1.4)
    enhancer_contrast = ImageEnhance.Contrast(image)
    image = enhancer_contrast.enhance(5)
    return image

def do_nth(image):
    return image

def imageToString(*functions, **kwargs):
    #key words include lang: string, image: PIL image

    image = kwargs["image"].convert("L")
    structuredText = ""

    if len(functions) == 0:
       structuredText = google_image_to_string(image)
    else:
        newfunctions = lambda imarg_arg: imarg_arg, *functions
        for index, image_method in enumerate(newfunctions):
            newImage = image.copy()
            newImage = image_method(newImage)
            result = google_image_to_string(newImage)
            structuredText = structuredText + f"Result {str(index)}: {result} \n\n---------------------------------\n\n"


    return structuredText


def crop_range_handler(point1, point2):
    smallestX = min(point1[0],point2[0])
    biggestX = max(point1[0],point2[0])
    smallestY = min(point1[1],point2[1])
    biggestY = max(point1[1],point2[1])

    return smallestX,smallestY,biggestX,biggestY

def create(ttk_element, **kwargs):
    ttk_element.grid(**kwargs)
    return ttk_element