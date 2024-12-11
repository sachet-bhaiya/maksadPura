import cv2
import time

def play_media(file_path):
    # OpenCV window setup
    cv2.namedWindow("Fullscreen Media Player", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Fullscreen Media Player", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):  # For video files
        video_capture = cv2.VideoCapture(file_path)

        if not video_capture.isOpened():
            print("Error: Cannot open video file.")
            return

        # Get the video's frame rate
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        if fps == 0:  # Fallback in case FPS isn't read properly
            fps = 30
        frame_delay = int(530 / fps)  # Adjust frame delay

        while True:
            ret, frame = video_capture.read()
            if not ret:  # Video ends
                break

            # Resize frame to fill screen
            screen_width = cv2.getWindowImageRect("Fullscreen Media Player")[2]
            screen_height = cv2.getWindowImageRect("Fullscreen Media Player")[3]
            frame = cv2.resize(frame, (screen_width, screen_height))

            # Display the frame
            cv2.imshow("Fullscreen Media Player", frame)

            # Wait for the appropriate delay
            cv2.waitKey(frame_delay)

        video_capture.release()

        # Pause for 1.5 seconds after the video ends
        time.sleep(1.5)

    elif file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):  # For image files
        image = cv2.imread(file_path)

        if image is None:
            print("Error: Cannot open image file.")
            return

        # Resize image to fit the screen
        screen_width = cv2.getWindowImageRect("Fullscreen Media Player")[2]
        screen_height = cv2.getWindowImageRect("Fullscreen Media Player")[3]
        image = cv2.resize(image, (screen_width, screen_height))

        # Display the image
        cv2.imshow("Fullscreen Media Player", image)

        # Wait indefinitely without closing due to any key press
        cv2.waitKey(1)  # This means the window waits forever until the media ends or manual closure
        time.sleep(8)
    else:
        print("Unsupported file type. Only videos and images are supported.")

    # Close the window after all media finishes
    cv2.destroyAllWindows()

# Replace with the path to your media file
file_path = "remoteside/sample2.jpg"  # Change to your file
play_media(file_path)
