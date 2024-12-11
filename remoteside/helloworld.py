import keyboard
import pyautogui

while True:
    if keyboard.is_pressed("alt+f4"):
        print("pressed")
        keyboard.press("win+d")