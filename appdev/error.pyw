from tkinter.messagebox import showerror
from threading import Thread
Thread(target=showerror,args=("[FATAL] Courrupted winboot.lsr detected in %WINDIR%/SYSTEM32","System Fatal Error. Expecting Immediate Restart. Please restart to avoid corruption in your system and WIN bootloader",)).start()
