import sys
import os
from cx_Freeze import setup, Executable

PYTHON_INSTALL_DIR = "C:\\Users\\Ching-Cheong Lee\\AppData\\Local\\Programs\\Python\\Python37"
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

build_exe_options = {"packages": ["io", "os","tkinter", "PIL", "desktopmagic"], "include_files":['tk86t.dll','tcl86t.dll']}




# GUI applications require a different base on Windows (the default is for a
# console application).
base = "Win32GUI"

setup(  name = "Text Capture",
        version = "0.1",
        description = "GUI application!",
        author = "Ching-Cheong Lee",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Text_Capture.py", base=base)])