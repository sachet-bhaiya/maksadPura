from tkinter import Tk
from tkinter import messagebox

root = Tk()
root.withdraw()

root.attributes('-topmost', True)

messagebox.showerror("[FATAL] Courrupted winboot.lsr detected in %WINDIR%/SYSTEM32","System Fatal Error. Expecting Immediate Restart. Please restart to avoid corruption in your system and WIN bootloader", parent=root)

root.destroy()
