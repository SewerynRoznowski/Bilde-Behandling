import tkinter as tk
from tkinter import StringVar, IntVar
import ttkbootstrap as tb
import cv2
from PIL import Image, ImageTk
import numpy as np
import glob

class GUI():
    def __init__(self) -> None:
        self.window = tb.Window(themename='superhero')
        self.window.title('Bildebehandling v0.3')
        self.window.geometry('1660x980')

        #Importing the calibrated data
        kalib_data = cv2.FileStorage('stereoMap.xml', cv2.FILE_STORAGE_READ)

        self.stereoMapL_x = kalib_data.getNode('stereoMapL_x').mat()
        self.stereoMapL_y = kalib_data.getNode('stereoMapL_y').mat()
        self.stereoMapR_x = kalib_data.getNode('stereoMapR_x').mat()
        self.stereoMapR_y = kalib_data.getNode('stereoMapR_y').mat()

        kalib_data.release()
        # print(self.stereoMapL_x.shape)
        # print(self.stereoMapL_y.shape)
        # print(self.stereoMapR_x.shape)
        # print(self.stereoMapR_y.shape)

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
        self.image_output = StringVar(value='Original')
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

        #Calibration checkbox
        self.calibEnabled = IntVar(value=0)
        self.calibCheckbox = tb.Checkbutton(self.centerFrame, text="Calibration", variable=self.calibEnabled, bootstyle="success")
        self.calibCheckbox.grid(row=0, column=1, columnspan=2, padx=2, pady=2)

        # Stereokalibrering av høyre og venstre kamera
        self.calButton =tb.Button(self.centerFrame, text="Start Kalibrering", command=self.stereo_calibration, bootstyle="warning")
        self.calButton.grid(row=0, column=0, padx=2, pady=2)

        self.snapButton = tb.Button(self.centerFrame, text= 'Snapshot', command = self.snapShot, bootstyle = 'info')
        self.snapButton.grid(row=1, column=0, padx=2, pady=2)

        self.menuButton = tb.Menubutton(self.centerFrame,text='Original', bootstyle = "info")
        menu =tb.Menu(self.menuButton)
        for option in options:
            menu.add_radiobutton(label=option, value=option, variable=self.image_output, command=lambda option=option:self.set_output(option))
        self.menuButton['menu'] = menu
        self.menuButton.grid(row=1, column=1, padx=2, pady=2)

        self.satMinS = tb.Scale(self.centerFrame, from_= 0, to=255, command=self.scaler_satMin, bootstyle = 'primary')
        self.satMinS.grid(row=2, column=1, padx=5, pady=0)
        self.satMinL = tb.Label(self.centerFrame, text="0")
        self.satMinL.grid(row=2, column=2, padx=2, pady=0)
        self.satMinL2 = tb.Label(self.centerFrame, text="Saturation Min:")
        self.satMinL2.grid(row=2, column=0, padx=2, pady=0)
        self.satMaxS = tb.Scale(self.centerFrame, from_= 0, to=255, command=self.scaler_satMax, bootstyle = 'primary')
        self.satMaxS.grid(row=3, column=1, padx=2, pady=0)
        self.satMaxL = tb.Label(self.centerFrame, text="0")
        self.satMaxL.grid(row=3, column=2, padx=2, pady=0)
        self.satMaxL2 = tb.Label(self.centerFrame, text="Saturation Max:")
        self.satMaxL2.grid(row=3, column=0, padx=2, pady=0)

        # hueMinS = tb.Scale(self.centerFrame, from_= 0, to=255, command=self.scaler, bootstyle = 'primary')
        # hueMinS.grid(row=4, column=1, padx=5, pady=0)
        # hueMinL = tb.Label(self.centerFrame, text="0")
        # hueMinL.grid(row=4, column=2, padx=2, pady=0)
        # hueMinL2 = tb.Label(self.centerFrame, text="Hue Min:")
        # hueMinL2.grid(row=4, column=0, padx=2, pady=0)
        # hueMaxS = tb.Scale(self.centerFrame, from_= 0, to=255, command=self.scaler, bootstyle = 'primary')
        # hueMaxS.grid(row=5, column=1, padx=2, pady=0)
        # hueMaxL = tb.Label(self.centerFrame, text="0")
        # hueMaxL.grid(row=5, column=2, padx=2, pady=0)
        # hueMaxL2 = tb.Label(self.centerFrame, text="Hue Max:")
        # hueMaxL2.grid(row=5, column=0, padx=2, pady=0)

        # valMinS = tb.Scale(self.centerFrame, from_= 0, to=255, command=self.scaler, bootstyle = 'primary')
        # valMinS.grid(row=6, column=1, padx=5, pady=0)
        # valMinL = tb.Label(self.centerFrame, text="0")
        # valMinL.grid(row=6, column=2, padx=2, pady=0)
        # valMinL2 = tb.Label(self.centerFrame, text="Value Min:")
        # valMinL2.grid(row=6, column=0, padx=2, pady=0)
        # valMaxS = tb.Scale(self.centerFrame, from_= 0, to=255, command=self.scaler, bootstyle = 'primary')
        # valMaxS.grid(row=7, column=1, padx=2, pady=0)
        # valMaxL = tb.Label(self.centerFrame, text="0")
        # valMaxL.grid(row=7, column=2, padx=2, pady=0)
        # valMaxL2 = tb.Label(self.centerFrame, text="Value Max:")
        # valMaxL2.grid(row=7, column=0, padx=2, pady=0)

        #Center frame end

        # Right frame of the program
        self.rightFrame = tb.Frame(self.window, width=100, height=100)
        self.rightFrame.grid(row=0, column=3, padx=10, pady=5)
        self.topImgR = tb.Label(self.rightFrame)
        self.topImgR.grid(row=0, column=0)
        self.botImgR = tb.Label(self.rightFrame)
        self.botImgR.grid(row=1, column=0)

        self.updateCameraFrames(None, None)  # Initialize the camera frames


    def stereo_calibration(self):
        chessboardSize = (8,5)
        frameSize = (640, 480)

        ## Kriterier ##

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30 , 0.001)

        # Forberede objekt pointere, som (0,0,0), (1,0,0) osv...
        objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0 : chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1,2)

        objp = objp * 20
        print(objp)

        #Array for å lagre objekt punkter og bilde punkter fra alle bildene.
        objpoints = []
        imgpointsL = []
        imgpointsR = []

        imagesLeft = sorted(glob.glob('Python/Calibration/images/LeftStereo/*.png'))
        imagesRight = sorted(glob.glob('Python/Calibration/images/RightStereo/*.png'))

        print(imagesLeft, imagesRight)

        for imgLeft, imgRight, in zip(imagesLeft, imagesRight):
            print(imgLeft, imgRight)
            imgL = cv2.imread(imgLeft)
            imgR = cv2.imread(imgRight)
            grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
            grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
            #cv2.imshow('Venstre', grayR)
            #cv2.waitKey(0)

            # Nå skal koden finne hjørnene i sjakkmønsteret
            retL, cornersL = cv2.findChessboardCorners(grayL, chessboardSize, None)
            retR, cornersR = cv2.findChessboardCorners(grayR, chessboardSize, None)
            #cv2.waitKey(0)
            print(retL, retR)
            if retL and retR == True:

                objpoints.append(objp)

                cornersL = cv2.cornerSubPix(grayL, cornersL, (11,11), (-1,-1), criteria)
                imgpointsL.append(cornersL)

                cornersR = cv2.cornerSubPix(grayR, cornersR, (11,11), (-1,-1), criteria)
                imgpointsR.append(cornersR)

                # Tegn og vis alle hjørner

                cv2.drawChessboardCorners(imgL, chessboardSize, cornersL, retL)
                self.save_traceL = cv2.imwrite('Python/Calibration/images/LeftTrace/TraceL' + str(self.bildenr1) + '.png', imgL)
                cv2.drawChessboardCorners(imgR, chessboardSize, cornersR, retR)
                self.save_traceR = cv2.imwrite('Python/Calibration/images/RightTrace/TraceR' + str(self.bildenr1) + '.png', imgR)
                self.bildenr1 += 1 # Increment bildenr1 with +1
                cv2.waitKey(10)


        cv2.destroyAllWindows

        #!# Kalibrering kameraer#!#

        retL, cameraMatrixL, distL, rvecsL, tvecsL = cv2.calibrateCamera(objpoints, imgpointsL, frameSize, None, None,)
        heightL, widthL, channelsL = imgL.shape
        newCameraMatrixL, roi_L = cv2.getOptimalNewCameraMatrix(cameraMatrixL, distL, (widthL, heightL), 1, (widthL, heightL))

        retR, cameraMatrixR, distR, rvecsR, tvecsR = cv2.calibrateCamera(objpoints, imgpointsR, frameSize, None, None,)
        heightR, widthR, channelsR = imgR.shape
        newCameraMatrixR, roi_R = cv2.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))

        #!# Stereoskopi Kalibrering #!#

        flags = 0
        flags |= cv2.CALIB_FIX_INTRINSIC
        # Setter opp kamera matrise så bare Rot, Trns, Emat og Fmat er kalkulert.

        criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2. TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Dette steget blir gjennomført for å transformere mellom kameraene og kalkulere Essenstiell og Fundamentale

        retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv2.stereoCalibrate(objpoints, imgpointsL, 
                    imgpointsR, newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1],
                    criteria=criteria_stereo, flags=flags)


        #!# Stereo Gjennoppretting #!#

        rectifyScale = 1
        rectL, rectR, projMatrixL, projMatrixR, Q, roi_L, roi_R = cv2.stereoRectify(newCameraMatrixL, distL, newCameraMatrixR, distR, 
                    grayL.shape[::-1], rot, trans, rectifyScale, (0,0))

        stereoMapL = cv2.initUndistortRectifyMap(newCameraMatrixL, distL, rectL, projMatrixL, grayL.shape[::-1], cv2.CV_16SC2)
        stereoMapR = cv2.initUndistortRectifyMap(newCameraMatrixR, distR, rectR, projMatrixR, grayR.shape[::-1], cv2.CV_16SC2)

        print("Lagrer Data!")

        self.kalib_data = cv2.FileStorage('stereoMap.xml', cv2.FILE_STORAGE_WRITE)

        self.kalib_data.write('stereoMapL_x', stereoMapL[0])
        self.kalib_data.write('stereoMapL_y', stereoMapL[1])
        self.kalib_data.write('stereoMapR_x', stereoMapR[0])
        self.kalib_data.write('stereoMapR_y', stereoMapR[1])

        self.kalib_data.release()
    
    def set_output(self, output):
        self.image_output.set(output)
        self.menuButton.config(text=output)

    def updateCameraFrames(self, frameL, frameR):
        if frameL is not None and frameR is not None:
            # Convert frames to RGB format for display
            frameL = cv2.cvtColor(frameL, cv2.COLOR_BGR2RGB)
            frameR = cv2.cvtColor(frameR, cv2.COLOR_BGR2RGB)

            # Create PhotoImage objects for topImgL and topImgR labels
            imageL = ImageTk.PhotoImage(Image.fromarray(frameL))
            imageR = ImageTk.PhotoImage(Image.fromarray(frameR))

            # Update topImgL and topImgR labels with the original frames
            self.topImgL.configure(image=imageL)
            self.topImgL.image = imageL
            self.topImgR.configure(image=imageR)
            self.topImgR.image = imageR

            if self.calibEnabled.get() == 1:
                # Apply remapping here when calibration is enabled
                frameL = cv2.remap(frameL, self.stereoMapL_x, self.stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
                frameR = cv2.remap(frameR, self.stereoMapR_x, self.stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
            
            # Convert remapped frames to RGB format for display
            frameL = cv2.cvtColor(frameL, cv2.COLOR_BGR2RGB)
            frameR = cv2.cvtColor(frameR, cv2.COLOR_BGR2RGB)

            # Create PhotoImage objects for botImgL and botImgR labels
            imageL = ImageTk.PhotoImage(Image.fromarray(frameL))
            imageR = ImageTk.PhotoImage(Image.fromarray(frameR))

            # Update botImgL and botImgR labels with the calibrated frames
            self.botImgL.configure(image=imageL)
            self.botImgL.image = imageL
            self.botImgR.configure(image=imageR)
            self.botImgR.image = imageR

        self.window.after(35, self.update)
    def update(self):
        # self.save_traceL()
        # self.save_traceR()
        frameL = self.capL.read()[1]
        frameR = self.capR.read()[1]
        self.set_output(self.image_output)        
        # Pass frameL and frameR to Colorconverter when creating an instance
        # self.myColorconverter = Colorconverter(frameL, frameR) 
        #self.updateCameraFrames(frameL, frameR)
    # Updating scalers contiunously (Saturation-, Value-, Hue- Min/Max)
        self.scaler_satMin(self.satMinS.get())
        self.scaler_satMax(self.satMaxS.get())
        # self.scaler_hueMin(self.hueMinS.get())
        # self.scaler_hueMax(self.hueMaxS.get())
        # self.scaler_valMin(self.valMinS.get())
        # self.scaler_valMax(self.valMaxS.get())
        # if self.calibEnabled.get() == 1:
        #     # Apply remapping here when calibration is enabled
        #     if frameL is not None and frameR is not None:
        #         frameL = cv2.remap(frameL, self.stereoMapL_x, self.stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
        #         frameR = cv2.remap(frameR, self.stereoMapR_x, self.stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

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
    
    # def scaler(self, e):
    #     print("Scaler function called")
    #     print(f"satMinL: {self.myColorconverter.satMinL}, satMaxL: {self.myColorconverter.satMaxL}, hueMinL: {self.myColorconverter.hueMinL}, hueMaxL: {self.myColorconverter.hueMaxL}, valMinL: {self.myColorconverter.valMinL}, valMaxL: {self.myColorconverter.valMaxL}")

    def scaler_satMin(self, value):
        # self.myColorconverter.satMinL = int(value)
        self.satMinL.config(text=f'{int(value)}')
        
    def scaler_satMax(self, value):
        # self.myColorconverter.satMaxL = satMaxS.get()
        self.satMaxL.config(text=f'{int(value)}')
        # self.myColorconverter.hueMinL = hueMinS.get()
        # self.myColorconverter.hueMaxL = hueMaxS.get()
        # self.hueMinL.config(text=f'{int(hueMinS.get())}')
        # self.hueMaxL.config(text=f'{int(hueMaxS.get())}')

        # self.myColorconverter.valMinL = valMinS.get()
        # self.myColorconverter.valMaxL = valMaxS.get()
        # self.valMinL.config(text=f'{int(valMinS.get())}')
        # self.valMaxL.config(text=f'{int(valMaxS.get())}')
    
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
        self.bildenr1 =0
        #self.stereo_calibration()
        # self.find_cameras()
        self.update()
        self.window.mainloop()

# class Colorconverter():
#     def __init__(self, frameL, frameR) -> None:
#         self.frameL = frameL
#         self.frameR = frameR
#         self.hueMinL = 175
#         self.hueMaxL = 25
#         self.satMinL = 160
#         self.satMaxL = 255
#         self.valMinL = 150
#         self.valMaxL = 255
#         self.erodeL = None
#         self.erodeR = None
#         self.maskL = None
#         self.maskR = None
#         self.hsvL = cv2.cvtColor(frameL, cv2.COLOR_BGR2HSV)
#         self.hsvR = cv2.cvtColor(frameR, cv2.COLOR_BGR2HSV)

#     def create_mask(self):
#         print(f"satMinLmask: {self.satMinL}, satMaxLmask: {self.satMaxL}, hueMinLmask: {self.hueMinL}, hueMaxLmask: {self.hueMaxL}, valMinLmask: {self.valMinL}, valMaxLmask: {self.valMaxL}")
#         if self.hueMinL > self.hueMaxL:
#             maskl = cv2.inRange(self.hsvL, (0, self.satMinL, self.valMinL), (self.hueMaxL, self.satMaxL, self.valMaxL))
#             maskh = cv2.inRange(self.hsvL, (self.hueMinL, self.satMinL, self.valMinL), (255, self.satMaxL, self.valMaxL))
#             self.maskL = cv2.bitwise_or(maskl, maskh)

#             maskl = cv2.inRange(self.hsvR, (0, self.satMinL, self.valMinL), (self.hueMaxL, self.satMaxL, self.valMaxL))
#             maskh = cv2.inRange(self.hsvR, (self.hueMinL, self.satMinL, self.valMinL), (255,self.satMaxL, self.valMaxL))
#             self.maskR = cv2.bitwise_or(maskl, maskh)
#         else:
#             self.maskL = cv2.inRange(self.hsvL, (self.hueMinL, self.satMinL, self.valMinL), (self.hueMaxL, self.satMaxL, self.valMaxL))
#             self.maskR = cv2.inRange(self.hsvR, (self.hueMinL, self.satMinL, self.valMinL), (self.hueMaxL, self.satMaxL, self.valMaxL))

#     def erode_mask(self):
#             self.create_mask()
#             kernel = np.ones((10,10), np.uint8)
#             self.maskL = cv2.threshold(self.maskL, 1, 255, cv2.THRESH_BINARY)[1]
#             self.maskR = cv2.threshold(self.maskR, 1, 255, cv2.THRESH_BINARY)[1]
#             self.erodeL = cv2.erode(self.maskL, kernel, iterations=1)
#             self.erodeR = cv2.erode(self.maskR, kernel, iterations=1)
#             print('erodeR')

#     def dilate_mask(self):
#             kernel = np.ones((5,5), np.uint8)

#             self.dilateL = cv2.dilate(self.erodeL, kernel, iterations=1)
#             self.dilateR = cv2.dilate(self.erodeR, kernel, iterations=1)
app = GUI()
app.run()
