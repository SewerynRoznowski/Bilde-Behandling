import tkinter as tk
from tkinter import StringVar, IntVar
import ttkbootstrap as tb
import cv2
from PIL import Image, ImageTk
import numpy as np


# Initialize the cameras
capL = cv2.VideoCapture(0)
capL.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capL.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cameraWidthL = capL.get(cv2.CAP_PROP_FRAME_WIDTH)
cameraHeightL = capL.get(cv2.CAP_PROP_FRAME_HEIGHT)

capR = cv2.VideoCapture(2)
capR.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capR.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cameraWidthR = capR.get(cv2.CAP_PROP_FRAME_WIDTH)
cameraHeightR = capR.get(cv2.CAP_PROP_FRAME_HEIGHT)

bildenr = 0

def mainloop():
    global image_output
    var = 0
    retL, frameL = capL.read()
    retR, frameR = capR.read()
    #print('Mordi')
    if var == 0:
        if retL and retR:
            myColorconverter =ColorConverter(frameL, frameR)
            updateCameraFrames(frameL, frameR, image_output)


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
        topImgR.configure(image=imageR)
        topImgR.image = imageR

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

# Scaler henter inn data fra slidere og gir label en verdi denne må gjøres slik at Hue, Sat og Val blir endret på i bildet
def scaler(e):
    print("Scaler function called")
    print(f"satMinL: {myColorconverter.satMinL}, satMaxL: {myColorconverter.satMaxL}, hueMinL: {myColorconverter.hueMinL}, hueMaxL: {myColorconverter.hueMaxL}, valMinL: {myColorconverter.valMinL}, valMaxL: {myColorconverter.valMaxL}")


    myColorconverter.satMinL = satMinS.get()
    myColorconverter.satMaxL = satMaxS.get()
    satMinL.config(text=f'{int(satMinS.get())}')
    satMaxL.config(text=f'{int(satMaxS.get())}')

    myColorconverter.hueMinL = hueMinS.get()
    myColorconverter.hueMaxL = hueMaxS.get()
    hueMinL.config(text=f'{int(hueMinS.get())}')
    hueMaxL.config(text=f'{int(hueMaxS.get())}')

    myColorconverter.valMinL = valMinS.get()
    myColorconverter.valMaxL = valMaxS.get()
    valMinL.config(text=f'{int(valMinS.get())}')
    valMaxL.config(text=f'{int(valMaxS.get())}')

def set_output(output):
    global image_output
    image_output = output
    menuButton.config(text=output)


class ColorConverter:
   def __init__(self, frameL, frameR):
       self.frameL = frameL
       self.frameR = frameR
       self.hueMinL = 175
       self.hueMaxL = 25
       self.satMinL = 160
       self.satMaxL = 255
       self.valMinL = 150
       self.valMaxL = 255
       self.erodeL = None
       self.erodeR = None
       self.maskL = None
       self.maskR = None
       self.hsvL = cv2.cvtColor(frameL, cv2.COLOR_BGR2HSV)
       self.hsvR = cv2.cvtColor(frameR, cv2.COLOR_BGR2HSV)

   def create_mask(self):
       print(f"satMinLmask: {self.satMinL}, satMaxLmask: {self.satMaxL}, hueMinLmask: {self.hueMinL}, hueMaxLmask: {self.hueMaxL}, valMinLmask: {self.valMinL}, valMaxLmask: {self.valMaxL}")
       if self.hueMinL > self.hueMaxL:
           maskl = cv2.inRange(self.hsvL, (0, self.satMinL, self.valMinL), (self.hueMaxL, self.satMaxL, self.valMaxL))
           maskh = cv2.inRange(self.hsvL, (self.hueMinL, self.satMinL, self.valMinL), (255, self.satMaxL, self.valMaxL))
           self.maskL = cv2.bitwise_or(maskl, maskh)

           maskl = cv2.inRange(self.hsvR, (0, self.satMinL, self.valMinL), (self.hueMaxL, self.satMaxL, self.valMaxL))
           maskh = cv2.inRange(self.hsvR, (self.hueMinL, self.satMinL, self.valMinL), (255,self.satMaxL, self.valMaxL))
           self.maskR = cv2.bitwise_or(maskl, maskh)
       else:
           self.maskL = cv2.inRange(self.hsvL, (self.hueMinL, self.satMinL, self.valMinL), (self.hueMaxL, self.satMaxL, self.valMaxL))
           self.maskR = cv2.inRange(self.hsvR, (self.hueMinL, self.satMinL, self.valMinL), (self.hueMaxL, self.satMaxL, self.valMaxL))

   def erode_mask(self):
        self.create_mask()
        kernel = np.ones((10,10), np.uint8)
        self.maskL = cv2.threshold(self.maskL, 1, 255, cv2.THRESH_BINARY)[1]
        self.maskR = cv2.threshold(self.maskR, 1, 255, cv2.THRESH_BINARY)[1]
        self.erodeL = cv2.erode(self.maskL, kernel, iterations=1)
        self.erodeR = cv2.erode(self.maskR, kernel, iterations=1)
        print('erodeR')

   def dilate_mask(self):
        kernel = np.ones((5,5), np.uint8)

        self.dilateL = cv2.dilate(self.erodeL, kernel, iterations=1)
        self.dilateR = cv2.dilate(self.erodeR, kernel, iterations=1)

retL, frameL = capL.read()
retR, frameR = capR.read()
myColorconverter =ColorConverter(frameL, frameR)

def process_images(frameL, frameR, image_output):
    imageL = []
    imageR = []
    myColorconverter.create_mask()
    if image_output == 'Original':
        originalL = cv2.cvtColor(frameL, cv2.COLOR_BGR2RGB)
        imageL = Image.fromarray(originalL)
        originalR = cv2.cvtColor(frameR, cv2.COLOR_BGR2RGB)
        imageR = Image.fromarray(originalR)

    elif image_output == 'Erosion':
        myColorconverter.erode_mask()
        imageL = Image.fromarray(myColorconverter.erodeL)
        imageR = Image.fromarray(myColorconverter.erodeR)
        

    elif image_output == 'Dialation':
        imageL = Image.fromarray(myColorconverter.dilateL)
        imageR = Image.fromarray(myColorconverter.dilateR)

    return imageL, imageR


# Create the main window
window = tb.Window(themename='superhero')
window.title('Bildebehandling v0.3')
window.geometry('1660x980')

# For dropdown menyen og de forskjellige typer masker som kan brukes for å finne hvem hører til hvor
image_output = StringVar(value='Original')
options = ['Original', 'Thresholding', 'Erosion', 'Dialation', 'Contour1', 'Contour2']

# Create frames and labels
# Left frame of the program
leftFrame = tb.Frame(window, width=100, height=100)
leftFrame.grid(row=0, column=0, padx=5, pady=5)

topImgL = tb.Label(leftFrame)
topImgL.grid(row=0, column=0)
botImgL = tb.Label(leftFrame)
botImgL.grid(row=1, column=0)

#Center frame of program
centerFrame = tb.Frame(window, width = 100, height= 100)
centerFrame.grid(row=0, column=1, padx=5, pady=5)

calButton = tb.Button(centerFrame, text= 'Snapshot', command = snapShot, bootstyle = 'warning')
calButton.grid(row=0, column=1, padx=5, pady=5)

menuButton = tb.Menubutton(centerFrame,text='Original', bootstyle = "info")
menu =tb.Menu(menuButton)
for option in options:
    menu.add_radiobutton(label=option, value=option, variable=image_output, command=lambda option=option:set_output(option))
menuButton['menu'] = menu
menuButton.grid(row=1, column=1, padx=5, pady=5)

satMinS = tb.Scale(centerFrame, from_= 0, to=255, command=scaler, bootstyle = 'primary')
satMinS.grid(row=2, column=1, padx=5, pady=0)
satMinL = tb.Label(centerFrame, text="0")
satMinL.grid(row=2, column=2, padx=2, pady=0)
satMinL2 = tb.Label(centerFrame, text="Saturation Min:")
satMinL2.grid(row=2, column=0, padx=2, pady=0)
satMaxS = tb.Scale(centerFrame, from_= 0, to=255, command=scaler, bootstyle = 'primary')
satMaxS.grid(row=3, column=1, padx=2, pady=0)
satMaxL = tb.Label(centerFrame, text="0")
satMaxL.grid(row=3, column=2, padx=2, pady=0)
satMaxL2 = tb.Label(centerFrame, text="Saturation Max:")
satMaxL2.grid(row=3, column=0, padx=2, pady=0)

hueMinS = tb.Scale(centerFrame, from_= 0, to=255, command=scaler, bootstyle = 'primary')
hueMinS.grid(row=4, column=1, padx=5, pady=0)
hueMinL = tb.Label(centerFrame, text="0")
hueMinL.grid(row=4, column=2, padx=2, pady=0)
hueMinL2 = tb.Label(centerFrame, text="Hue Min:")
hueMinL2.grid(row=4, column=0, padx=2, pady=0)
hueMaxS = tb.Scale(centerFrame, from_= 0, to=255, command=scaler, bootstyle = 'primary')
hueMaxS.grid(row=5, column=1, padx=2, pady=0)
hueMaxL = tb.Label(centerFrame, text="0")
hueMaxL.grid(row=5, column=2, padx=2, pady=0)
hueMaxL2 = tb.Label(centerFrame, text="Hue Max:")
hueMaxL2.grid(row=5, column=0, padx=2, pady=0)

valMinS = tb.Scale(centerFrame, from_= 0, to=255, command=scaler, bootstyle = 'primary')
valMinS.grid(row=6, column=1, padx=5, pady=0)
valMinL = tb.Label(centerFrame, text="0")
valMinL.grid(row=6, column=2, padx=2, pady=0)
valMinL2 = tb.Label(centerFrame, text="Value Min:")
valMinL2.grid(row=6, column=0, padx=2, pady=0)
valMaxS = tb.Scale(centerFrame, from_= 0, to=255, command=scaler, bootstyle = 'primary')
valMaxS.grid(row=7, column=1, padx=2, pady=0)
valMaxL = tb.Label(centerFrame, text="0")
valMaxL.grid(row=7, column=2, padx=2, pady=0)
valMaxL2 = tb.Label(centerFrame, text="Value Max:")
valMaxL2.grid(row=7, column=0, padx=2, pady=0)

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
