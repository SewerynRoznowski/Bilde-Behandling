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
r_min = 165
r_max = 255
g_min = 0
g_max = 70
b_min = 0
b_max = 70

#define sliders for color tresholds
def set_r_min(r):
    global r_min
    r_min = int(r)
def set_r_max(r):
    global r_max
    r_max = int(r)
def set_g_min(g):
    global g_min
    g_min = int(g)
def set_g_max(g):
    global g_max
    g_max = int(g)
def set_b_min(b):
    global b_min
    b_min = int(b)
def set_b_max(b):
    global b_max
    b_max = int(b)

# create a slider for the threshold

r_slider_min_label = tk.Label(rightFrame, text='Red min:')
r_slider_min_label.grid(row=0, column=0)
r_slider_min = tk.Scale(rightFrame, from_=0, to=255, command=set_r_min, orient='horizontal')
r_slider_min.grid(row=0, column=1)
r_slider_min.set(r_min)

r_slider_max_label = tk.Label(rightFrame, text='Red max:')
r_slider_max_label.grid(row=1, column=0)
r_slider_max = tk.Scale(rightFrame, from_=0, to=255, command=set_r_max, orient='horizontal')
r_slider_max.grid(row=1, column=1)
r_slider_max.set(r_max)

g_slider_min_label = tk.Label(rightFrame, text='Green min:')
g_slider_min_label.grid(row=2, column=0)
g_slider_min = tk.Scale(rightFrame, from_=0, to=255, command=set_g_min, orient='horizontal')
g_slider_min.grid(row=2, column=1)
g_slider_min.set(g_min)

g_slider_max_label = tk.Label(rightFrame, text='Green max:')
g_slider_max_label.grid(row=3, column=0)
g_slider_max = tk.Scale(rightFrame, from_=0, to=255, command=set_g_max, orient='horizontal')
g_slider_max.grid(row=3, column=1)
g_slider_max.set(g_max)

b_slider_min_label = tk.Label(rightFrame, text='Blue min:')
b_slider_min_label.grid(row=4, column=0)
b_slider_min = tk.Scale(rightFrame, from_=0, to=255, command=set_b_min, orient='horizontal')
b_slider_min.grid(row=4, column=1)
b_slider_min.set(b_min)

b_slider_max_label = tk.Label(rightFrame, text='Blue max:')
b_slider_max_label.grid(row=5, column=0)
b_slider_max = tk.Scale(rightFrame, from_=0, to=255, command=set_b_max, orient='horizontal')
b_slider_max.grid(row=5, column=1)
b_slider_max.set(b_max)

def update_image():
    
    ret , frame = cap.read()

    if not ret:
        print('Could not read image from webcam')
        return

    # convert the image to hsv
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mask = cv2.inRange(rgb, (r_min, g_min, b_min), (r_max, g_max, b_max))

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


