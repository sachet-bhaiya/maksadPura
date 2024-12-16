import os
import shutil

if os.listdir("build"):
    shutil.rmtree("build")