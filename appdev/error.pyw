from tkinter import messagebox
from threading import Thread
num = 15

for _ in range(1,11):
    Thread(target=messagebox.showerror,args=("Fatal error detected in %WINDIR%/SYSTEM32","System Fatal Error. Expecting Immediate Restart. Please restart to avoid corruption in your system",)).start()
