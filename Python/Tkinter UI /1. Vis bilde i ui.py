import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

# Define the OpenCV webcam object
cap = cv2.VideoCapture(0)

# Set the resolution of the webcam to a lower value
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Define the tkinter window
root = tk.Tk()
root.title('OpenCV Webcam')

# Define the tkinter label for displaying the image
label = tk.Label(root)
label.pack(side='left')

# Define the custom kernel
kernel = np.array([[-4, -3, -2, -1, 0],
                   [-3, -2, -1, 0, 1],
                     [-2, -1, 0, 1, 2],
                     [-1, 0, 1, 2, 3],
                     [0, 1, 2, 3, 4]]) /20
# 5x5 kernel 
kernel1 = np.array ([[-1, -1, -1, -1, 0],
                        [-1, -1, -1, 0, 1],
                        [-1, -1, 0, 1, 1],
                        [-1, 0, 1, 1, 1],
                        [0, 1, 1, 1, 1]]) /10
# 3x3 kernel diagonal edges
kernel2 = np.array ([[-2, -1, 0],
                    [-1, 0, 1],
                    [0, 1, 2]]) /4 

kernel3 = np.array ([[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]]) /4

kernel4 = np.array ([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]]) /4
 
                    
# Define the threshold value
threshold_min = 100
threshold_max = 255

# Define the tkinter slider for adjusting the threshold
def set_threshold_min(threshold):
    global threshold_min

    # Convert the threshold to an integer
    threshold = int(threshold)
    threshold_min = threshold

# create a slider for the threshold
threshold_slider_min = tk.Scale(root, from_=0, to=255, command=set_threshold_min)
threshold_slider_min.pack(side='left')




# Define the function for updating the image
def update_image():
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    filtered = cv2.filter2D(frame, cv2.CV_32F, kernel)

    filtered = cv2.convertScaleAbs(filtered)

    _, filtered = cv2.threshold(filtered, threshold_min, threshold_max, cv2.THRESH_BINARY)

    #filtered1 = cv2.filter2D(frame, cv2.CV_32F, kernel3)

    #filtered1 = cv2.convertScaleAbs(filtered1)

    #_, filtered1 = cv2.threshold(filtered1, threshold_min, threshold_max, cv2.THRESH_BINARY)

    #filtered2 = cv2.filter2D(frame, cv2.CV_32F, kernel4)

    #filtered2 = cv2.convertScaleAbs(filtered2)

    #_, filtered2 = cv2.threshold(filtered2, threshold_min, threshold_max, cv2.THRESH_BINARY)

    #combined = cv2.bitwise_and(filtered, filtered1)
    #combined = cv2.bitwise_and(combined, filtered2)


    #splice with original image 
    combined = cv2.hconcat([frame, filtered])

    # Convert the frame to a PIL ImageTk format
    image = Image.fromarray(combined)
    image_tk = ImageTk.PhotoImage(image)

    # Update the label with the new image
    label.config(image=image_tk)
    label.image = image_tk

    # Schedule the function to be called again in 10 milliseconds
    root.after(10, update_image)

# Call the function to start updating the image
update_image()

# Start the tkinter main loop
root.mainloop()

# Release the webcam object
cap.release()