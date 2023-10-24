import cv2 
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import math

# UI ---------------------------------------------------------------------------------------------
# Define the tkinter window
root = tk.Tk()
root.title('Shape detection demo')
root.configure(background='skyblue')

leftFrame = tk.Frame(root, widt = 100, height = 100)
leftFrame.grid(row=0, column=0, padx=10, pady=5)

rightFrame = tk.Frame(root, widt = 100, height = 100)
rightFrame.grid(row=0, column=1, padx=10, pady=5)

rightrightFrame = tk.Frame(root, widt = 100, height = 100)
rightrightFrame.grid(row=0, column=2, padx=10, pady=5)

# define the labels for the images, UI stuff 
topImage = tk.Label(leftFrame)
topImage.grid(row=0, column=0)

bottomImage = tk.Label(leftFrame)
bottomImage.grid(row=1, column=0)

topImageRight = tk.Label(rightrightFrame)
topImageRight.grid(row=0, column=0)

bottomImageRight = tk.Label(rightrightFrame)
bottomImageRight.grid(row=1, column=0)

# define sliders for color tresholds, these are default values, not min/max
h_min = 175
h_max = 25
s_min = 160
s_max = 255
v_min = 150
v_max = 255

image_output = 'Orginal'
options = ['Orginal', 'Terskling', 'Erosjon', 'Dialasjon', 'Konturer1', 'Konturer2']

takeSnapshot = False

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

# define function for dropdown menu
def set_output(output):
    global image_output
    image_output = output

# define snapshot button 
def snapshot():
    global takeSnapshot
    takeSnapshot = True

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

# add dropdown menu for selecting output of 2nd image 
output = tk.StringVar(rightFrame)
output.set(image_output)

outputLabel = tk.Label(rightFrame, text='Output:')
outputLabel.grid(row=6, column=0)
outputMenu = tk.OptionMenu(rightFrame, output, *options, command=set_output)
outputMenu.grid(row=6, column=1)

# add snapshot button
snapshotButton = tk.Button(rightFrame, text='Snapshot', command=snapshot)
snapshotButton.grid(row=7, column=0)




# UI ---------------------------------------------------------------------------------------------

# CV2 Setup --------------------------------------------------------------------------------------
cap = cv2.VideoCapture(0)
cap1= cv2.VideoCapture(1)

# set the camera resolution, if resolution is invalid it will choose the closest one
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# get the camera resolution, this is used to calculate the distance from the center of the image
cameraWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cameraHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

cameraWidth1 = cap1.get(cv2.CAP_PROP_FRAME_WIDTH)
cameraHeight1 = cap1.get(cv2.CAP_PROP_FRAME_HEIGHT)

# assumed camera field of view, needs to be calibrated
cameraFOV = 60
cameraFOV1 = 60

# CV2 Setup --------------------------------------------------------------------------------------

#Function that runs every frame
def update_image():
    global takeSnapshot

    # read the image from the webcam
    ret , frame = cap.read()
    ret1 , frame1 = cap1.read()

    if not ret or not ret1:
        print('Could not read image from webcam')
        return

    # convert the image to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

    # the hue axis is a circle. This means certain colors can be tricky to treshhold. Like red.
    # To solve this we can use two tresholds, one for the lower values and one for the higher values
    if h_min > h_max:
        maskl = cv2.inRange(hsv, (0, s_min, v_min), (h_max, s_max, v_max))
        maskh = cv2.inRange(hsv, (h_min, s_min, v_min), (255, s_max, v_max))
        mask = cv2.bitwise_or(maskl, maskh)

        maskl = cv2.inRange(hsv1, (0, s_min, v_min), (h_max, s_max, v_max))
        maskh = cv2.inRange(hsv1, (h_min, s_min, v_min), (255, s_max, v_max))
        mask1 = cv2.bitwise_or(maskl, maskh)
    else:
        mask = cv2.inRange(hsv, (h_min, s_min, v_min), (h_max, s_max, v_max))
        mask1 = cv2.inRange(hsv1, (h_min, s_min, v_min), (h_max, s_max, v_max))

    # Erode the mask, this removes small blobs
    kernel = np.ones((5,5), np.uint8)
    erode = cv2.erode(mask, kernel, iterations=1)
    erode1 = cv2.erode(mask1, kernel, iterations=1)

    # dialate the mask, restores the size remaining blobs
    dialate = cv2.dilate(erode, kernel, iterations=1)
    dialate1 = cv2.dilate(erode1, kernel, iterations=1)
    
    # find contours in the mask
    contours = cv2.findContours(dialate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    contours1 = cv2.findContours(dialate1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    filtered_contours = []
    filtered_contours1 = []
    # Approximate the contour shape and filter out small contours
    if len(contours) > 0:
        for x in contours:
            epsilon = 0.01*cv2.arcLength(x, True) 
            approx = cv2.approxPolyDP(x, epsilon, True)

            sides = len(approx)

            # only keep contours with 4 sides and an area larger than 1000 pixels
            if sides == 4 and cv2.contourArea(x) > 1000:

                filtered_contours.append(x)

    if len(contours1) > 0:
        for x in contours1:
            epsilon = 0.01*cv2.arcLength(x, True) 
            approx = cv2.approxPolyDP(x, epsilon, True)

            sides = len(approx)

            # only keep contours with 4 sides and an area larger than 1000 pixels
            if sides == 4 and cv2.contourArea(x) > 1000:

                filtered_contours1.append(x)

    # Go through filitered contours and draw them on the image
    for x in filtered_contours:
        cv2.drawContours(mask, [x], 0, 255, -1)
        M = cv2.moments(x)
        if M['m00'] > 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # convert cx and cy to degrees from center 
            angleX = math.degrees(math.atan((cx - cameraWidth/2)/(cameraWidth/2) * math.tan(math.radians(cameraFOV/2))))
            angleY = math.degrees(math.atan((cy - cameraHeight/2)/(cameraHeight/2) * math.tan(math.radians(cameraFOV/2))))

            cv2.putText(frame, str(angleX), (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, str(angleY), (cx - 20, cy - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    for x in filtered_contours1:
        cv2.drawContours(mask1, [x], 0, 255, -1)
        M = cv2.moments(x)
        if M['m00'] > 0:
            cy = int(M['m10']/M['m00'])
            cx = int(M['m01']/M['m00'])
            cv2.circle(frame1, (cy, cx), 5, (0, 0, 255), -1)

            # convert cx and cy to degrees from center
            angleX = math.degrees(math.atan((cy - cameraWidth1/2)/(cameraWidth1/2) * math.tan(math.radians(cameraFOV1/2))))
            angleY = math.degrees(math.atan((cx - cameraHeight1/2)/(cameraHeight1/2) * math.tan(math.radians(cameraFOV1/2))))

            cv2.putText(frame1, str(angleX), (cy - 20, cx - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame1, str(angleY), (cy - 20, cx - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)



    image = []
    image1 = []
    snapshot = []
    snapshot1 = []
    # switchcase 
    if image_output == 'Orginal':
        original = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(original)
        snaphot = original

        original1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        image1 = Image.fromarray(original1)
        snaphot1 = original1

    elif image_output == 'Terskling':
        image = Image.fromarray(mask)
        snapshot = mask

        image1 = Image.fromarray(mask1)
        snapshot1 = mask1

    elif image_output == 'Erosjon':
        image = Image.fromarray(erode)
        snapshot = erode

        image1 = Image.fromarray(erode1)
        snapshot1 = erode1

    elif image_output == 'Dialasjon':
        image = Image.fromarray(dialate)
        snapshot = dialate

        image1 = Image.fromarray(dialate1)
        snapshot1 = dialate1

    elif image_output == 'Konturer1':
        #create a blank image of same size as camera image
        blank = np.zeros((int(cameraHeight), int(cameraWidth),3), np.uint8)
        blank1 = np.zeros((int(cameraHeight1), int(cameraWidth1),3), np.uint8)

        #draw contours on blank image
        for x in contours:
            cv2.drawContours(blank, [x], 0, (0, 255, 0), 3)

        for x in contours1:
            cv2.drawContours(blank1, [x], 0, (0, 255, 0), 3)
        
        image = Image.fromarray(blank)
        image1 = Image.fromarray(blank1)

        snapshot = blank
        snapshot1 = blank1
    elif image_output == 'Konturer2':
        #create a blank image of same size as camera image
        blank = np.zeros((int(cameraHeight), int(cameraWidth),3), np.uint8)
        blank1 = np.zeros((int(cameraHeight1), int(cameraWidth1),3), np.uint8)
        #draw contours on blank image
        for x in filtered_contours:
            cv2.drawContours(blank, [x], 0, (0, 255, 0), 3)

        for x in filtered_contours1:
            cv2.drawContours(blank1, [x], 0, (0, 255, 0), 3)

        image = Image.fromarray(blank)
        image1 = Image.fromarray(blank1)
        snapshot = blank
        snapshot1 = blank1
    else:
        image = Image.fromarray(frame)
        snapshot = frame

        image = Image.fromarray(frame1)
        snapshot = frame1

    
    if takeSnapshot == True:
        cv2.imwrite('Snapshot 0 Source.png', frame)
        cv2.imwrite('Snapshot 0 Output.png', snapshot)
        cv2.imwrite('Snapshot 1 Source.png', frame1)
        cv2.imwrite('Snapshot 1 Output.png', snapshot1)

        takeSnapshot = False

    # convert the mask to an image compatible with tkinter 
    imagetk = ImageTk.PhotoImage(image) 

    # update the image in the UI
    bottomImage.imagetk = imagetk
    bottomImage.configure(image=imagetk)

    imagetk = ImageTk.PhotoImage(image1)

    bottomImageRight.imagetk = imagetk
    bottomImageRight.configure(image=imagetk)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)

    imageSource = Image.fromarray(frame)
    
    imagetk = ImageTk.PhotoImage(imageSource)

    topImage.imagetk = imagetk
    topImage.configure(image=imagetk)

    imageSource = Image.fromarray(frame1)

    imagetk = ImageTk.PhotoImage(imageSource)

    topImageRight.imagetk = imagetk
    topImageRight.configure(image=imagetk)

    root.after(100, update_image)

update_image()

root.mainloop()

cap.release()


