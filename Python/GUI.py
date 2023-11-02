import tkinter as tk
import ttkbootstrap as tb
import cv2
from PIL import Image, ImageTk
import subprocess
from Calibration.kalibreringklasse import StereoCameraCapture

# Initialize the cameras
capL = cv2.VideoCapture(0)
capL.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capL.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

capR = cv2.VideoCapture(2)
capR.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capR.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

stereo_capture = StereoCameraCapture()
#var = 0
def mainloop():
    var = 0
    retL, frameL = capL.read()
    retR, frameR = capR.read()

    if var == 0:
        if retL and retR:
            updateCameraFrames(frameL, frameR)


    else:
        ret = startCalibration(frameL, frameR)
        if ret is True:
             var = 0

    window.after(10, mainloop)  # Update frames every 10 milliseconds

def updateCameraFrames(frameL, frameR):
    if frameL is not None and frameR is not None:
        frameL = cv2.cvtColor(frameL, cv2.COLOR_BGR2RGB)
        frameR = cv2.cvtColor(frameR, cv2.COLOR_BGR2RGB)

        imageSourceL = Image.fromarray(frameL)
        imageL = ImageTk.PhotoImage(imageSourceL)

        imageSourceR = Image.fromarray(frameR)
        imageR = ImageTk.PhotoImage(imageSourceR)

        topImgL.configure(image=imageL)
        topImgL.image = imageL
        botImgL.configure(image=imageL)
        botImgL.image = imageL

        topImgR.configure(image=imageR)
        topImgR.image = imageR
        botImgR.configure(image=imageR)
        botImgR.image = imageR

def startCalibration():
    try:
        frameL, frameR = capL.read(), capR.read()
        stereo_capture.capture_images(frameL, frameR)  # Capture images before starting calibration
        result = subprocess.run(["python", '/home/knugen23/Documents/GitHub/Bilde-Behandling/Python/Calibration/kalibreringklasse.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    except Exception as e:
        print("Error:", str(e))

# Create the main window
window = tb.Window(themename='superhero')
window.title('Bildebehandling v0.1')
window.geometry('1280x720')

# Create frames and labels
# Left frame of the program
leftFrame = tb.Frame(window, width=100, height=100)
leftFrame.grid(row=0, column=0, padx=10, pady=5)

topImgL = tb.Label(leftFrame)
topImgL.grid(row=0, column=0)
botImgL = tb.Label(leftFrame)
botImgL.grid(row=1, column=0)

#Center frame of program
centerFrame = tb.Frame(window, width = 100, height= 100)
centerFrame.grid(row=0, column=1, padx=10, pady=5)

calButton = tb.Button(centerFrame, text= 'Kalibrering', command = startCalibration, bootstyle = 'warning')
calButton.grid(row=0, column=1, padx=5, pady=10)

# Right frame of the program
rightFrame = tb.Frame(window, width=100, height=100)
rightFrame.grid(row=0, column=2, padx=10, pady=5)
topImgR = tb.Label(rightFrame)
topImgR.grid(row=0, column=0)
botImgR = tb.Label(rightFrame)
botImgR.grid(row=1, column=0)

# Start updating camera frames
mainloop()

# Start the main loop
window.mainloop()
cv2.destroyAllWindows()
