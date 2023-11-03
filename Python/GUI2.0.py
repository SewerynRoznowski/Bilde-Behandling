import tkinter as tk
from tkinter import StringVar, IntVar
import ttkbootstrap as tb
import cv2
from PIL import Image, ImageTk
import numpy as np

class GUI():
    def __init__(self) -> None:
        self.window = tb.Window(themename='superhero')
        self.window.title('Bildebehandling v0.3')
        self.window.geometry('1660x980')

        # Initialize the cameras
        self.capL = cv2.VideoCapture(0)
        if not self.capL.isOpened():
            print("Error: Left Camera not opened")
        else:
            print("Left Camera opened successfully")
        self.capL.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capL.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cameraWidthL = self.capL.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.cameraHeightL = self.capL.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.capR = cv2.VideoCapture(2)
        if not self.capL.isOpened():
            print("Error: Right Camera not opened")
        else:
            print("Right Camera opened successfully")
        self.capR.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capR.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cameraWidthR = self.capR.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.cameraHeightR = self.capR.get(cv2.CAP_PROP_FRAME_HEIGHT)

        retL, frameL = self.capL.read()
        retR, frameR = self.capR.read()

        if retL and retR:
            print("Frames captured successfully from both cameras")
        else:
            print("Failed to capture frames from one or both cameras.")

#        self.find_cameras()  # Call the find_cameras method to check available cameras
        
        # For dropdown menyen og de forskjellige typer masker som kan brukes for å finne hvem hører til hvor
        image_output = StringVar(value='Original')
        options = ['Original', 'Thresholding', 'Erosion', 'Dialation', 'Contour1', 'Contour2']

        # Create frames and labels
        # Left frame of the program
        self.leftFrame = tb.Frame(self.window, width=100, height=100)
        self.leftFrame.grid(row=0, column=0, padx=5, pady=5)

        self.topImgL = tb.Label(self.leftFrame)
        self.topImgL.grid(row=0, column=0)
        self.botImgL = tb.Label(self.leftFrame)
        self.botImgL.grid(row=1, column=0)
        #Center frame of program
        self.centerFrame = tb.Frame(self.window, width = 100, height= 100)
        self.centerFrame.grid(row=0, column=1, padx=5, pady=5)

        # calButton = tb.Button(centerFrame, text= 'Snapshot', command = snapShot, bootstyle = 'warning')
        # calButton.grid(row=0, column=1, padx=5, pady=5)

        menuButton = tb.Menubutton(self.centerFrame,text='Original', bootstyle = "info")
        menu =tb.Menu(menuButton)
        for option in options:
            menu.add_radiobutton(label=option, value=option, variable=image_output, command=lambda option=option:set_output(option))
        menuButton['menu'] = menu
        menuButton.grid(row=1, column=1, padx=5, pady=5)

        satMinS = tb.Scale(self.centerFrame, from_= 0, to=255, command=self.scaler, bootstyle = 'primary')
        satMinS.grid(row=2, column=1, padx=5, pady=0)
        satMinL = tb.Label(self.centerFrame, text="0")
        satMinL.grid(row=2, column=2, padx=2, pady=0)
        satMinL2 = tb.Label(self.centerFrame, text="Saturation Min:")
        satMinL2.grid(row=2, column=0, padx=2, pady=0)
        satMaxS = tb.Scale(self.centerFrame, from_= 0, to=255, command=self.scaler, bootstyle = 'primary')
        satMaxS.grid(row=3, column=1, padx=2, pady=0)
        satMaxL = tb.Label(self.centerFrame, text="0")
        satMaxL.grid(row=3, column=2, padx=2, pady=0)
        satMaxL2 = tb.Label(self.centerFrame, text="Saturation Max:")
        satMaxL2.grid(row=3, column=0, padx=2, pady=0)

        hueMinS = tb.Scale(self.centerFrame, from_= 0, to=255, command=self.scaler, bootstyle = 'primary')
        hueMinS.grid(row=4, column=1, padx=5, pady=0)
        hueMinL = tb.Label(self.centerFrame, text="0")
        hueMinL.grid(row=4, column=2, padx=2, pady=0)
        hueMinL2 = tb.Label(self.centerFrame, text="Hue Min:")
        hueMinL2.grid(row=4, column=0, padx=2, pady=0)
        hueMaxS = tb.Scale(self.centerFrame, from_= 0, to=255, command=self.scaler, bootstyle = 'primary')
        hueMaxS.grid(row=5, column=1, padx=2, pady=0)
        hueMaxL = tb.Label(self.centerFrame, text="0")
        hueMaxL.grid(row=5, column=2, padx=2, pady=0)
        hueMaxL2 = tb.Label(self.centerFrame, text="Hue Max:")
        hueMaxL2.grid(row=5, column=0, padx=2, pady=0)

        valMinS = tb.Scale(self.centerFrame, from_= 0, to=255, command=self.scaler, bootstyle = 'primary')
        valMinS.grid(row=6, column=1, padx=5, pady=0)
        valMinL = tb.Label(self.centerFrame, text="0")
        valMinL.grid(row=6, column=2, padx=2, pady=0)
        valMinL2 = tb.Label(self.centerFrame, text="Value Min:")
        valMinL2.grid(row=6, column=0, padx=2, pady=0)
        valMaxS = tb.Scale(self.centerFrame, from_= 0, to=255, command=self.scaler, bootstyle = 'primary')
        valMaxS.grid(row=7, column=1, padx=2, pady=0)
        valMaxL = tb.Label(self.centerFrame, text="0")
        valMaxL.grid(row=7, column=2, padx=2, pady=0)
        valMaxL2 = tb.Label(self.centerFrame, text="Value Max:")
        valMaxL2.grid(row=7, column=0, padx=2, pady=0)

        #Center frame end

        # Right frame of the program
        self.rightFrame = tb.Frame(self.window, width=100, height=100)
        self.rightFrame.grid(row=0, column=3, padx=10, pady=5)
        self.topImgR = tb.Label(self.rightFrame)
        self.topImgR.grid(row=0, column=0)
        self.botImgR = tb.Label(self.rightFrame)
        self.botImgR.grid(row=1, column=0)

    def updateCameraFrames(self, frameL, frameR):
        # retL, frameL = self.capL.read()
        # retR, frameR = self.capR.read()
        if frameL is not None and frameR is not None:
            frameL = cv2.cvtColor(frameL, cv2.COLOR_BGR2RGB)
            frameR = cv2.cvtColor(frameR, cv2.COLOR_BGR2RGB)

            self.imageSourceL = Image.fromarray(frameL)
            imageL = ImageTk.PhotoImage(self.imageSourceL)
            self.imageSourceR = Image.fromarray(frameR)
            imageR = ImageTk.PhotoImage(self.imageSourceR)

            self.topImgL.configure(image=imageL)
            self.topImgL.image = imageL
            self.topImgR.configure(image=imageR)
            self.topImgR.image = imageR

        self.window.after(50, self.update)
    def update(self):
        frameL = self.capL.read()[1]
        frameR = self.capR.read()[1]
        
        # Pass frameL and frameR to Colorconverter when creating an instance
        self.myColorconverter = Colorconverter(frameL, frameR) 

        self.updateCameraFrames(frameL, frameR)




    def snapShot(self):
        try:
            retL, frameL = self.capL.read()
            retR, frameR = self.capR.read()
            test = cv2.imwrite('Python/Calibration/images/LeftStereo/ImageL' + str(self.bildenr) + '.png', frameL)
            test1 = cv2.imwrite('Python/Calibration/images/RightStereo/ImageR' + str(self.bildenr) + '.png', frameR)
            if test == True and test1 == True:
                print('Images saved!')
            self.bildenr += 1
        except Exception as e:
            print("Error:", str(e))
    
    def scaler(self, e):
        print("Scaler function called")
        print(f"satMinL: {self.myColorconverter.satMinL}, satMaxL: {self.myColorconverter.satMaxL}, hueMinL: {self.myColorconverter.hueMinL}, hueMaxL: {self.myColorconverter.hueMaxL}, valMinL: {self.myColorconverter.valMinL}, valMaxL: {self.myColorconverter.valMaxL}")


        self.myColorconverter.satMinL = satMinS.get()
        self.myColorconverter.satMaxL = satMaxS.get()
        satMinL.config(text=f'{int(satMinS.get())}')
        satMaxL.config(text=f'{int(satMaxS.get())}')

        self.myColorconverter.hueMinL = hueMinS.get()
        self.myColorconverter.hueMaxL = hueMaxS.get()
        hueMinL.config(text=f'{int(hueMinS.get())}')
        hueMaxL.config(text=f'{int(hueMaxS.get())}')

        self.myColorconverter.valMinL = valMinS.get()
        self.myColorconverter.valMaxL = valMaxS.get()
        valMinL.config(text=f'{int(valMinS.get())}')
        valMaxL.config(text=f'{int(valMaxS.get())}')
    
    # def find_cameras(self, max_cameras_to_check=10):
    #     self.available_cameras = []
    #     for i in range(max_cameras_to_check):
    #         cap = cv2.VideoCapture(i)
    #         if cap is None or not cap.isOpened():
    #             cap.release()
    #         else:
    #             self.available_cameras.append(i)
    #             cap.release()
    #     print(self.available_cameras)
    
    

    def run(self):
        self.bildenr = 0
#        self.find_cameras()
#        self.update()
        self.window.mainloop()

class Colorconverter():
    def __init__(self, frameL, frameR) -> None:
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
app = GUI()
app.run()
