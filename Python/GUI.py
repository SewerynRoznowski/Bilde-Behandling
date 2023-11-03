import tkinter as tk
from tkinter import StringVar
import ttkbootstrap as tb
import cv2
from PIL import Image, ImageTk


# Initialize the cameras
capL = cv2.VideoCapture(0)
capL.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capL.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

capR = cv2.VideoCapture(2)
capR.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capR.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

bildenr = 0

#var = 0
def mainloop():
    var = 0
    retL, frameL = capL.read()
    retR, frameR = capR.read()

    if var == 0:
        if retL and retR:
            updateCameraFrames(frameL, frameR)


    else:
        ret = snapShot(frameL, frameR)
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

# Denne definisjonen tar bilde av høyre og venstre kamera og lagrer de i en predefinert mappe.
def snapShot():
    global bildenr
    try:
        retL, frameL = capL.read()
        retR, frameR = capR.read()
        test = cv2.imwrite('Python/Calibration/images/LeftStereo/ImageL' + str(bildenr) + '.png', frameL)
        test1 = cv2.imwrite('Python/Calibration/images/RightStereo/ImageR' + str(bildenr) + '.png', frameR)
        if test == True and test1 == True:
            print('Images saved!')
        bildenr += 1
    except Exception as e:
        print("Error:", str(e))

# Scaler henter inn data fra slidere og gir label en verdi
def scaler(e):
    SatMinL.config(text=f'{int(SatMinS.get())}')
    SatMaxL.config(text=f'{int(SatMaxS.get())}')

def set_output(output):
    global image_output
    image_output = output
    menuButton.config(text=output)


# Create the main window
window = tb.Window(themename='superhero')
window.title('Bildebehandling v0.1')
window.geometry('1560x980')

image_output = StringVar(value='Original')
options = ['Original', 'Thresholding', 'Erosion', 'Dialation', 'Contour1', 'Contour2']

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

calButton = tb.Button(centerFrame, text= 'Snapshot', command = snapShot, bootstyle = 'warning')
calButton.grid(row=0, column=1, padx=5, pady=5)

menuButton = tb.Menubutton(centerFrame,text='Original', bootstyle = "info")
menu =tb.Menu(menuButton)
for option in options:
    menu.add_radiobutton(label=option, value=option, variable=image_output, command=lambda option=option:set_output(option))
menuButton['menu'] = menu
menuButton.grid(row=1, column=1, padx=5, pady=5)

SatMinS = tb.Scale(centerFrame, from_= 0, to=255, command=scaler, bootstyle = 'primary')
SatMinS.grid(row=2, column=1, padx=2, pady=0)
SatMinL = tb.Label(centerFrame, text="0")
SatMinL.grid(row=2, column=2, padx=2, pady=0)
SatMinL2 = tb.Label(centerFrame, text="SatMin:")
SatMinL2.grid(row=2, column=0, padx=2, pady=0)

SatMaxS = tb.Scale(centerFrame, from_= 0, to=255, command=scaler, bootstyle = 'primary')
SatMaxS.grid(row=3, column=1, padx=2, pady=0)
SatMaxL = tb.Label(centerFrame, text="0")
SatMaxL.grid(row=3, column=2, padx=2, pady=0)
SatMaxL2 = tb.Label(centerFrame, text="SatMax:")
SatMaxL2.grid(row=3, column=0, padx=2, pady=0)

#Center frame end

# Right frame of the program
rightFrame = tb.Frame(window, width=100, height=100)
rightFrame.grid(row=0, column=3, padx=10, pady=5)
topImgR = tb.Label(rightFrame)
topImgR.grid(row=0, column=0)
botImgR = tb.Label(rightFrame)
botImgR.grid(row=1, column=0)

# Start updating camera frames
mainloop()

# Start the main loop
window.mainloop()
cv2.destroyAllWindows()
1