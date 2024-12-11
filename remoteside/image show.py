import tkinter as tk
import cv2
from PIL import Image, ImageTk

# Function to close the window after a delay
def close_window():
    root.quit()

# Function to display the video frame-by-frame
def show_video_frame():
    global video_capture, label, video_ended

    # Read the next frame from the video
    ret, frame = video_capture.read()

    if ret:  # If there are frames left
        # Resize the frame to fit the window size
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (root.winfo_width(), root.winfo_height()))  # Resize to fill the window

        # Convert frame to ImageTk format for displaying in Tkinter
        frame_image = ImageTk.PhotoImage(image=Image.fromarray(frame))

        # Update the label with the new frame
        label.config(image=frame_image)
        label.image = frame_image  # Keep a reference to avoid garbage collection

        # Schedule the next frame update
        root.after(10, show_video_frame)
    else:
        # If video ends, mark as ended and wait 3 seconds before closing
        if not video_ended:
            video_ended = True
            root.after(3000, close_window)  # Wait 3 seconds after video ends

# Function to handle image files (JPEG, PNG)
def show_image(image_path):
    image = Image.open(image_path)
    
    # Resize the image to fit the window size
    image = image.resize((root.winfo_width(), root.winfo_height()), Image.Resampling.LANCZOS)
    
    # Convert to Tkinter-compatible photo object
    photo = ImageTk.PhotoImage(image)

    # Update the label to display the image
    label.config(image=photo)
    label.image = photo
    
    # Wait 8 seconds before closing the window
    root.after(8000, close_window)

# Create the main window
root = tk.Tk()

# Set the window title
root.title("Fullscreen Keep On Top Window")

# Set the "keep on top" feature
root.attributes('-topmost', 1)

# Set the window to fullscreen
root.attributes('-fullscreen', True)

# Remove the window decorations (close, minimize, etc.)
root.overrideredirect(True)

# Set the background color of the window to black
root.configure(bg='black')

# Create a label for displaying images or video frames
label = tk.Label(root, bg='black')  # Set label background to black
label.place(x=0, y=0, relwidth=1, relheight=1)

# Set this flag to detect if video has ended
video_ended = False

# Path to the file (change this path to your file)
file_path = "remoteside/sample2.jpg"  # Replace with your file path

# Check if the file is a video or image
if file_path.lower().endswith(('mp4', 'avi', 'mov')):
    # If it's a video file
    video_capture = cv2.VideoCapture(file_path)
    show_video_frame()
else:
    # If it's an image file
    show_image(file_path)

# Run the Tkinter event loop
root.mainloop()
