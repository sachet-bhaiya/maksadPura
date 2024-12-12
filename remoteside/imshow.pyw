import cv2
import time
import ctypes
import os 
data = os.listdir("assets")
if not data:
    exit()
file_path = "assets/"+data[0]
window_name = "HECKBOI"
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

hwnd = ctypes.windll.user32.FindWindowW(None, window_name)
if hwnd:
    ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)

if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
    video_capture = cv2.VideoCapture(file_path)
    if not video_capture.isOpened():
        exit()

    fps = video_capture.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30
    frame_delay = int(530 / fps)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        screen_width = cv2.getWindowImageRect(window_name)[2]
        screen_height = cv2.getWindowImageRect(window_name)[3]
        frame = cv2.resize(frame, (screen_width, screen_height))
        cv2.imshow(window_name, frame)
        cv2.waitKey(frame_delay)

    video_capture.release()
    time.sleep(1.5)

elif file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
    image = cv2.imread(file_path)
    if image is None:
        exit()

    screen_width = cv2.getWindowImageRect(window_name)[2]
    screen_height = cv2.getWindowImageRect(window_name)[3]
    image = cv2.resize(image, (screen_width, screen_height))
    cv2.imshow(window_name, image)
    cv2.waitKey(1)
    time.sleep(8)

else:
    exit()

cv2.destroyAllWindows()
