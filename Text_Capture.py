import os
from components.FullScreenableRoot.FullScreenableRoot import FullScreenableRoot
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import asyncio

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ".\\environment_variable.json"


def main():
    root = FullScreenableRoot()
    root.mainloop()

main()

