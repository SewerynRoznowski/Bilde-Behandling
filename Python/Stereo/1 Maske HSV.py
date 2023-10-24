import cv2 
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# Define the tkinter window
root = tk.Tk()
root.title('Shape detection demo')
root.configure(background='skyblue')

leftFrame = tk.Frame(root, widt = 100, height = 100)
leftFrame.grid(row=0, column=0, padx=10, pady=5)

rightFrame = tk.Frame(root, widt = 100, height = 100)
rightFrame.grid(row=0, column=1, padx=10, pady=5)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

topImage = tk.Label(leftFrame)
topImage.grid(row=0, column=0)

bottomImage = tk.Label(leftFrame)
bottomImage.grid(row=1, column=0)

# define sliders for color tresholds
h_min = 175
h_max = 25
s_min = 160
s_max = 255
v_min = 150
v_max = 255

#define sliders for color tresholds
def set_h_min(h):
    global h_min
    h_min = int(h)
def set_h_max(h):
    global h_max
    h_max = int(h)
def set_s_min(s):
    global s_min
    s_min = int(s)
def set_s_max(s):
    global s_max
    s_max = int(s)
def set_v_min(v):
    global v_min
    v_min = int(v)
def set_v_max(v):
    global v_max
    v_max = int(v)

# create a slider for the threshold
h_slider_min_label = tk.Label(rightFrame, text='Hue min:')
h_slider_min_label.grid(row=0, column=0)
h_slider_min = tk.Scale(rightFrame, from_=0, to=255, command=set_h_min, orient='horizontal')
h_slider_min.grid(row=0, column=1)
h_slider_min.set(h_min)

h_slider_max_label = tk.Label(rightFrame, text='Hue max:')
h_slider_max_label.grid(row=1, column=0)
h_slider_max = tk.Scale(rightFrame, from_=0, to=255, command=set_h_max, orient='horizontal')
h_slider_max.grid(row=1, column=1)
h_slider_max.set(h_max)

s_slider_min_label = tk.Label(rightFrame, text='Saturation min:')
s_slider_min_label.grid(row=2, column=0)
s_slider_min = tk.Scale(rightFrame, from_=0, to=255, command=set_s_min, orient='horizontal')
s_slider_min.grid(row=2, column=1)
s_slider_min.set(s_min)

s_slider_max_label = tk.Label(rightFrame, text='Saturation max:')
s_slider_max_label.grid(row=3, column=0)
s_slider_max = tk.Scale(rightFrame, from_=0, to=255, command=set_s_max, orient='horizontal')
s_slider_max.grid(row=3, column=1)
s_slider_max.set(s_max)

v_slider_min_label = tk.Label(rightFrame, text='Value min:')
v_slider_min_label.grid(row=4, column=0)
v_slider_min = tk.Scale(rightFrame, from_=0, to=255, command=set_v_min, orient='horizontal')
v_slider_min.grid(row=4, column=1)
v_slider_min.set(v_min)

v_slider_max_label = tk.Label(rightFrame, text='Value max:')
v_slider_max_label.grid(row=5, column=0)
v_slider_max = tk.Scale(rightFrame, from_=0, to=255, command=set_v_max, orient='horizontal')
v_slider_max.grid(row=5, column=1)
v_slider_max.set(v_max)

def update_image():
    
    ret , frame = cap.read()

    if not ret:
        print('Could not read image from webcam')
        return

    # convert the image to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if h_min > h_max:
        mask1 = cv2.inRange(hsv, (0, s_min, v_min), (h_max, s_max, v_max))
        mask2 = cv2.inRange(hsv, (h_min, s_min, v_min), (255, s_max, v_max))
        mask = cv2.bitwise_or(mask1, mask2)

    else:
        mask = cv2.inRange(hsv, (h_min, s_min, v_min), (h_max, s_max, v_max))

    image = Image.fromarray(mask)
    imagetk = ImageTk.PhotoImage(image) 

    bottomImage.imagetk = imagetk
    bottomImage.configure(image=imagetk)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(frame)
    imagetk = ImageTk.PhotoImage(image)

    topImage.imagetk = imagetk
    topImage.configure(image=imagetk)

    root.after(10, update_image)

update_image()

root.mainloop()

cap.release()


