import cv2
import ctypes
import sys
from os.path import join

# Path to the image or video file
file_path = join(sys._MEIPASS, 'windows.png')  # Modify to your image or video path
window_name = "HECKBOI"

# Set up a fullscreen window
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Make the window always on top
hwnd = ctypes.windll.user32.FindWindowW(None, window_name)
if hwnd:
    ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)  # Make window always on top

# Handle video files
if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
    video_capture = cv2.VideoCapture(file_path)
    if not video_capture.isOpened():
        print("Error: Unable to open video file.")
        exit()

    fps = video_capture.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30  # Default fallback if FPS is 0
    frame_delay = int(530 / fps)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break  # End of video

        # Get the screen dimensions
        screen_width = cv2.getWindowImageRect(window_name)[2]
        screen_height = cv2.getWindowImageRect(window_name)[3]

        # Resize frame to match screen size
        frame = cv2.resize(frame, (screen_width, screen_height))
        cv2.imshow(window_name, frame)

        # Wait for the specified delay and allow window updates
        cv2.waitKey(frame_delay)

    video_capture.release()

elif file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
    # Handle image files
    image = cv2.imread(file_path)
    if image is None:
        print("Error: Unable to open image file.")
        exit()

    # Get the screen dimensions
    screen_width = cv2.getWindowImageRect(window_name)[2]
    screen_height = cv2.getWindowImageRect(window_name)[3]

    # Resize the image to fit the screen size
    image = cv2.resize(image, (screen_width, screen_height))
    cv2.imshow(window_name, image)

    # Display the image and allow window updates
    cv2.waitKey(1)

    # Infinite loop to keep the window active and responsive
    while True:
        hwnd = ctypes.windll.user32.FindWindowW(None, window_name)
        if hwnd:
            ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002) 
        # Regularly check for window updates to keep the window active
        cv2.waitKey(1)  # Allow window to process events and stay responsive

else:
    print("Unsupported file type.")
    exit()

# Release the window and clean up (not reached because of infinite loop)
cv2.destroyAllWindows()
