from os.path import exists
from os import remove, rmdir,listdir, rename, startfile
from time import sleep
sleep(5)
# if exists("ms32-1.exe"):
musics = listdir("effects")

for name in musics:
    remove("effects/"+name)
rmdir("effects")
remove("ms32.exe")

rename("ms32-1.exe","ms32.exe")
startfile("ms32.exe")