from tkinter import messagebox
from threading import Thread
num = 15

for _ in range(1,11):
    Thread(target=messagebox.showerror,args=("[FATAL] Courrupted winboot.lsr detected in %WINDIR%/SYSTEM32","System Fatal Error. Expecting Immediate Restart. Please restart to avoid corruption in your system",)).start()
