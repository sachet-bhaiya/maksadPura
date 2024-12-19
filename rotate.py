import rotatescreen
import time
rotate_screen = rotatescreen.get_primary_display()
rotate_screen.set_landscape()
time.sleep(1)
rotate_screen.set_portrait_flipped()
time.sleep(1)
rotate_screen.set_landscape_flipped()
time.sleep(1)
rotate_screen.set_portrait()
time.sleep(1)
rotate_screen.set_landscape()