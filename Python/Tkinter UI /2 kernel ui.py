import cv2 
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

# Define the tkinter window
root = tk.Tk()
root.title('Kernel demo')
root.configure(background='skyblue')

leftFrame = tk.Frame(root, widt = 100, height = 100)
leftFrame.grid(row=0, column=0, padx=10, pady=5)

rightFrame = tk.Frame(root, widt = 100, height = 100)
rightFrame.grid(row=0, column=1, padx=10, pady=5)

kernelFrame = tk.Frame(rightFrame, widt = 100, height = 100)
kernelFrame.grid(row=0, column=0, padx=10, pady=5)

settingsFrame = tk.Frame(rightFrame, widt = 100, height = 100)
settingsFrame.grid(row=1, column=0, padx=10, pady=5)


image_label = tk.Label(leftFrame)
image_label.grid(row=0, column=0)

# 5x5 comnvolution kernel 
kernelDivisor = 1
kernel = np.array([[0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]]) / kernelDivisor

threshold_min = 100
threshold_max = 255

# Define the 5x5 matrix of Entry widgets
matrix = []
for i in range(5):
    row = []
    for j in range(5):
        entry = tk.Entry(kernelFrame, width=5)
        entry.grid(row=i, column=j)
        entry.insert(0, str(kernel[i][j]*kernelDivisor))
        row.append(entry)
    matrix.append(row)

# Define the additional Entry widget
label = tk.Label(settingsFrame, text='Kernel Divisor:')
label.grid(row=6, column=0)
entry = tk.Entry(settingsFrame, width=5)
entry.grid(row=6, column=1)
entry.insert(0, str(kernelDivisor))

# Define the tkinter slider for adjusting the threshold
def set_threshold_min(threshold):
    global threshold_min

    # Convert the threshold to an integer
    threshold = int(threshold)
    threshold_min = threshold

# create a slider for the threshold
thresholdLabel = tk.Label(settingsFrame, text='Threshold:')
thresholdLabel.grid(row=6, column=2)
threshold_slider_min = tk.Scale(settingsFrame, from_=0, to=255,orient= 'horizontal', command=set_threshold_min)
threshold_slider_min.grid(row=6, column=3)

# Define the function for getting the values from the matrix
def get_matrix_values():
    global kernel
    global kernelDivisor

    # Get the kernel divisor
    try:
        kernelDivisor = float(entry.get())
        if kernelDivisor == 0:
            kernelDivisor = 1
            entry.delete(0, 'end')
            entry.insert(0, '1')

    except ValueError:
        kernelDivisor = 1

    for i in range(5):
        for j in range(5):
            # check if the entry is a number
            # Either float or integer is accepted
            try:
                value = float(matrix[i][j].get()) / kernelDivisor
            except ValueError:
                value = 0
            kernel[i][j] = value


# Define the tkinter button for getting the values from the matrix
button = tk.Button(settingsFrame, text='Update Kernel', command=get_matrix_values)
button.grid(row=5, column=2)

thresholdBool = tk.BooleanVar()
tickbox = tk.Checkbutton(settingsFrame, text='Treshold', variable=thresholdBool)
tickbox.grid(row=5, column=3)

absoluteBool = tk.BooleanVar()
tickbox = tk.Checkbutton(settingsFrame, text='Absolute', variable=absoluteBool)
tickbox.grid(row=5, column=4)



# define webcam object 
cap = cv2.VideoCapture(0)

# Set the resolution of the webcam to a lower value
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# Define the function for updating the image
def update_image():
    # Read a frame from the webcam
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)

    # Convert the frame to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    filtered = cv2.filter2D(frame, cv2.CV_32F, kernel)

    if absoluteBool.get() == 1:
        filtered = cv2.filter2D(frame, cv2.CV_32F, kernel)
        filtered = cv2.convertScaleAbs(filtered)
    else: 
        filtered = cv2.filter2D(frame, -1, kernel)

    if thresholdBool.get() == 1:
        _, filtered = cv2.threshold(filtered, threshold_min, threshold_max, cv2.THRESH_BINARY)


    #splice with original image 
    combined = cv2.vconcat([frame, filtered])

    # Convert the frame to a PIL ImageTk format
    image = Image.fromarray(combined)
    image_tk = ImageTk.PhotoImage(image)

    # Update the label with the new image
    image_label.config(image=image_tk)
    image_label.image = image_tk

    # Schedule the function to be called again in 10 milliseconds
    root.after(10, update_image)

# Call the function to start updating the image
update_image()

# Start the tkinter main loop
root.mainloop()

# Release the webcam object
cap.release()
