import cv2 
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import math


def find_cameras(max_cameras_to_check=10):
    available_cameras = []
    for i in range(max_cameras_to_check):
        cap = cv2.VideoCapture(i)
        if cap is None or not cap.isOpened():
            cap.release()
        else:
            available_cameras.append(i)
            cap.release()
    print(available_cameras)
    return available_cameras


# Function to calculate the lengths of the other two sides
def calculate_triangle_sides(side_c, angle_a, angle_b):
    # Convert angles from degrees to radians

    angle_c = 180 - angle_a - angle_b

    angle_a_rad = math.radians(angle_a)
    angle_b_rad = math.radians(angle_b)
    angle_c_rad = math.radians(angle_c)

    success = True
    side_a = 0
    side_b = 0
    
    try: # Sometimes sin of andle_c_rad can give 0, this causes a division by zero error. 
        side_b = (side_c * math.sin(angle_b_rad)) / math.sin(angle_c_rad)
    
        side_a = (side_c * math.sin(angle_a_rad)) / math.sin(angle_c_rad)
    
    except ZeroDivisionError:
        success = False

    return success, side_a, side_b



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

cameraL = 0
cameraR = 2

# assumed camera field of view, needs to be calibrated
cameraLFOV = 78

cameraRFOV = 78


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

def set_cameraLFOV(fov):
    global cameraLFOV
    cameraLFOV = float(fov)

def set_cameraRFOV(fov):
    global cameraRFOV
    cameraRFOV = float(fov)


#define function for input camera 
def set_cameraL(camera):
    global cameraL
    global capL 
    global cameraWidthL
    global cameraHeightL

    cameraL = int(camera)

    try: 
        capL.release()
    except:
        pass

    capL = cv2.VideoCapture(cameraL)

    # set the camera resolution, if resolution is invalid it will choose the closest one
    capL.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capL.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # get the camera resolution, this is used to calculate the distance from the center of the image
    cameraWidthL = capL.get(cv2.CAP_PROP_FRAME_WIDTH)
    cameraHeightL = capL.get(cv2.CAP_PROP_FRAME_HEIGHT)



def set_cameraR(camera):
    global cameraR
    global capR
    global cameraWidthR
    global cameraHeightR

    cameraR = int(camera)

    try: 
        capR.release()
    except:
        pass

    capR = cv2.VideoCapture(cameraR)

    capR.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capR.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    cameraWidthR = capR.get(cv2.CAP_PROP_FRAME_WIDTH)
    cameraHeightR = capR.get(cv2.CAP_PROP_FRAME_HEIGHT)



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

# add dropdown menu for selecting input camera 
cameras = find_cameras()
cameraL = tk.StringVar(rightFrame)
cameraL.set(cameras[0])

cameraLabel = tk.Label(rightFrame, text='Camera Left:')
cameraLabel.grid(row=8, column=0)
cameraMenu = tk.OptionMenu(rightFrame, cameraL, *cameras, command=set_cameraL)
cameraMenu.grid(row=8, column=1)

cameraR = tk.StringVar(rightFrame)
cameraR.set(cameras[0])

cameraLabel = tk.Label(rightFrame, text='Camera Right:')
cameraLabel.grid(row=9, column=0)
cameraMenu = tk.OptionMenu(rightFrame, cameraR, *cameras, command=set_cameraR)
cameraMenu.grid(row=9, column=1)

# add an input field for FOV 
fovL = tk.StringVar(rightFrame)
fovL.set(cameraLFOV)

fovLLabel = tk.Label(rightFrame, text='FOV Left:')
fovLLabel.grid(row=10, column=0)
fovLEntry = tk.Entry(rightFrame, textvariable=fovL)
fovLEntry.grid(row=10, column=1)

# add an input field for FOV
fovR = tk.StringVar(rightFrame)
fovR.set(cameraRFOV)

fovRLabel = tk.Label(rightFrame, text='FOV Right:')
fovRLabel.grid(row=11, column=0)
fovREntry = tk.Entry(rightFrame, textvariable=fovR)
fovREntry.grid(row=11, column=1)


# UI ---------------------------------------------------------------------------------------------

# CV2 Setup --------------------------------------------------------------------------------------

#set_cameraL(0)
#set_cameraR(2)

capL = cv2.VideoCapture(int(0))
capR = cv2.VideoCapture(int(2))

# set the camera resolution, if resolution is invalid it will choose the closest one
capL.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capL.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

capR.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capR.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# get the camera resolution, this is used to calculate the distance from the center of the image
cameraWidthL = capL.get(cv2.CAP_PROP_FRAME_WIDTH)
cameraHeightL = capL.get(cv2.CAP_PROP_FRAME_HEIGHT)

cameraWidthR = capR.get(cv2.CAP_PROP_FRAME_WIDTH)
cameraHeightR = capR.get(cv2.CAP_PROP_FRAME_HEIGHT)

# CV2 Setup --------------------------------------------------------------------------------------

#Function that runs every frame
def update_image():
    global takeSnapshot

    # read the image from the webcam
    ret , frame = capL.read()
    ret1 , frame1 = capR.read()

    if not ret or not ret1:
        print('Could not read image from webcam')
        return


    
    #blur = cv2.GaussianBlur(frame, (9, 9), 0)
    #blur = cv2.medianBlur(frame, 13)

    #blur = cv2.GaussianBlur(frame, (9, 9), 0)
    #blur1 = cv2.medianBlur(frame1, 13)

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

            # only keep contours with 4 sides and an area larger than 1000 pixels
            if cv2.contourArea(x) > 100:

                filtered_contours.append(x)

    if len(contours1) > 0:
        for x in contours1:

            if cv2.contourArea(x) > 100:

                filtered_contours1.append(x)

    # contour matching

    matchedContours = []
    matchFilter = 0.2

    if (len (filtered_contours) > 0 and len (filtered_contours1) > 0):
        for idx, x in enumerate(filtered_contours):
            bestMatch = []

            for idy, y in enumerate(filtered_contours1):
                matchChance = cv2.matchShapes(x, y, 1, 0.0)

                if matchChance < matchFilter:
                    bestMatch.append([idx,idy, matchChance])

            if len(bestMatch) > 0:
            
                bestMatch = min(bestMatch, key=lambda x: x[2])

                matchedContours.append(bestMatch)

    for x in matchedContours:
        cv2.drawContours(frame, [filtered_contours[x[0]]], 0, (0, 255, 0), 3)
        cv2.drawContours(frame1, [filtered_contours1[x[1]]], 0, (0, 255, 0), 3)



        M = cv2.moments(filtered_contours[x[0]])
        if M['m00'] > 0:
            cx0 = int(M['m10']/M['m00'])
            cy0 = int(M['m01']/M['m00'])

            angleX0 = (math.degrees(math.atan((cx0 - cameraWidthL/2)/(cameraWidthL/2) * math.tan(math.radians(cameraLFOV/2))))*-1) + 90 
            angleY0 = math.degrees(math.atan((cy0 - cameraHeightL/2)/(cameraHeightL/2) * math.tan(math.radians(cameraLFOV/2))))

            cv2.circle(frame, (cx0, cy0), 5, (0, 0, 255), -1)


        M = cv2.moments(filtered_contours1[x[1]])
        if M['m00'] > 0:
            cx1 = int(M['m10']/M['m00'])
            cy1 = int(M['m01']/M['m00'])

            angleX1 = math.degrees(math.atan((cx1 - cameraWidthR/2)/(cameraWidthR/2) * math.tan(math.radians(cameraRFOV/2)))) + 90
            angleY1 = math.degrees(math.atan((cy1 - cameraHeightR/2)/(cameraHeightR/2) * math.tan(math.radians(cameraRFOV/2))))

            cv2.circle(frame1, (cx1, cy1), 5, (0, 0, 255), -1)


        
        if angleX0 and angleX1: 
            ret, distance1 , distance2 = calculate_triangle_sides(0.18, angleX0, angleX1)

            if ret == True:
                cv2.putText(frame, str(distance2), (cx0 - 20, cy0 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(frame1, str(distance1), (cx1 - 20, cy1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

   


    # Image preview. ---------------------------------------------------------------------------------------------

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


    # elif image_output == 'Blur':
    #     original = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)
    #     image = Image.fromarray(original)
    #     snapshot = original

    #     original1 = cv2.cvtColor(blur1, cv2.COLOR_BGR2RGB)
    #     image1 = Image.fromarray(original1)
    #     snapshot1 = original1   


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
        blank = np.zeros((int(cameraHeightL), int(cameraWidthL),3), np.uint8)
        blank1 = np.zeros((int(cameraHeightR), int(cameraWidthR),3), np.uint8)

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
        blank = np.zeros((int(cameraHeightL), int(cameraWidthL),3), np.uint8)
        blank1 = np.zeros((int(cameraHeightR), int(cameraWidthR),3), np.uint8)
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



    # Image preview. ---------------------------------------------------------------------------------------------s

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

capL.release()
capR.release()


