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

        self.myColorconverter = Colorconverter()

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
        self.options = ['Original', 'Thresholding', 'Erosion', 'Dialation', 'Contour1', 'Contour2']

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

        self.snapButton = tb.Button(self.centerFrame, text= 'Snapshot', command = self.snapShot, bootstyle = 'info', width='10')
        self.snapButton.grid(row=1, column=0, padx=2, pady=2)

        self.menuButton = tb.Menubutton(self.centerFrame,text='Original', bootstyle = "info")
        menu =tb.Menu(self.menuButton)
        for option in self.options:
            menu.add_radiobutton(label=option, value=option, variable=self.image_output, command=lambda option=option:self.set_output(option))
        self.menuButton['menu'] = menu
        self.menuButton.grid(row=1, column=1, padx=2, pady=2)

        self.satMinS = tb.Scale(self.centerFrame, from_= 0, to=255, value=self.myColorconverter.satMinL, command=self.scaler_satMin, bootstyle = 'primary')
        self.satMinS.grid(row=2, column=1, padx=5, pady=0)
        self.satMinL = tb.Label(self.centerFrame, text=str(self.myColorconverter.satMinL))
        self.satMinL.grid(row=2, column=2, padx=2, pady=0)
        self.satMinL2 = tb.Label(self.centerFrame, text="Saturation Min:")
        self.satMinL2.grid(row=2, column=0, padx=2, pady=0)
        self.satMaxS = tb.Scale(self.centerFrame, from_= 0, to=255, value=self.myColorconverter.satMaxL, command=self.scaler_satMax, bootstyle = 'primary')
        self.satMaxS.grid(row=3, column=1, padx=2, pady=0)
        self.satMaxL = tb.Label(self.centerFrame, text=str(self.myColorconverter.satMaxL))
        self.satMaxL.grid(row=3, column=2, padx=2, pady=0)
        self.satMaxL2 = tb.Label(self.centerFrame, text="Saturation Max:")
        self.satMaxL2.grid(row=3, column=0, padx=2, pady=0)

        self.hueMinS = tb.Scale(self.centerFrame, from_= 0, to=255, value=self.myColorconverter.hueMinL , command=self.scaler_hueMin, bootstyle = 'primary')
        self.hueMinS.grid(row=4, column=1, padx=5, pady=0)
        self.hueMinL = tb.Label(self.centerFrame, text=str(self.myColorconverter.hueMinL))
        self.hueMinL.grid(row=4, column=2, padx=2, pady=0)
        self.hueMinL2 = tb.Label(self.centerFrame, text="Hue Min:")
        self.hueMinL2.grid(row=4, column=0, padx=2, pady=0)
        self.hueMaxS = tb.Scale(self.centerFrame, from_= 0, to=255, value=self.myColorconverter.hueMaxL, command=self.scaler_hueMax, bootstyle = 'primary')
        self.hueMaxS.grid(row=5, column=1, padx=2, pady=0)
        self.hueMaxL = tb.Label(self.centerFrame, text=str(self.myColorconverter.hueMaxL))
        self.hueMaxL.grid(row=5, column=2, padx=2, pady=0)
        self.hueMaxL2 = tb.Label(self.centerFrame, text="Hue Max:")
        self.hueMaxL2.grid(row=5, column=0, padx=2, pady=0)

        self.valMinS = tb.Scale(self.centerFrame, from_= 0, to=255, value=self.myColorconverter.valMinL, command=self.scaler_valMin, bootstyle = 'primary')
        self.valMinS.grid(row=6, column=1, padx=5, pady=0)
        self.valMinL = tb.Label(self.centerFrame, text=str(self.myColorconverter.valMinL))
        self.valMinL.grid(row=6, column=2, padx=2, pady=0)
        self.valMinL2 = tb.Label(self.centerFrame, text="Value Min:")
        self.valMinL2.grid(row=6, column=0, padx=2, pady=0)
        self.valMaxS = tb.Scale(self.centerFrame, from_= 0, to=255, value=self.myColorconverter.valMaxL, command=self.scaler_valMax, bootstyle = 'primary')
        self.valMaxS.grid(row=7, column=1, padx=2, pady=0)
        self.valMaxL = tb.Label(self.centerFrame, text=str(self.myColorconverter.valMaxL))
        self.valMaxL.grid(row=7, column=2, padx=2, pady=0)
        self.valMaxL2 = tb.Label(self.centerFrame, text="Value Max:")
        self.valMaxL2.grid(row=7, column=0, padx=2, pady=0)

        #Center frame end

        # Right frame of the program
        self.rightFrame = tb.Frame(self.window, width=100, height=100)
        self.rightFrame.grid(row=0, column=3, padx=10, pady=5)
        self.topImgR = tb.Label(self.rightFrame)
        self.topImgR.grid(row=0, column=0)
        self.botImgR = tb.Label(self.rightFrame)
        self.botImgR.grid(row=1, column=0)

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
        self.proj_MatxL = cv2.FileStorage('projMatrixL.xml', cv2.FILE_STORAGE_WRITE)
        self.proj_MatxR = cv2.FileStorage('projMatrixR.xml', cv2.FILE_STORAGE_WRITE)

        self.kalib_data.write('stereoMapL_x', stereoMapL[0])
        self.kalib_data.write('stereoMapL_y', stereoMapL[1])
        self.kalib_data.write('stereoMapR_x', stereoMapR[0])
        self.kalib_data.write('stereoMapR_y', stereoMapR[1])
        self.proj_MatxL.write('projMatrixL', projMatrixL)
        self.proj_MatxR.write('projMatrixR', projMatrixR)

        self.kalib_data.release()
    
    def set_output(self, output):
        self.image_output.set(output)
        self.menuButton.config(text=output)

    def updateCameraFrames(self, frameL, frameR):
        if frameL is not None and frameR is not None:

            if self.calibEnabled.get() == 1:
                # Apply remapping here when calibration is enabled
                frameL = cv2.remap(frameL, self.stereoMapL_x, self.stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
                frameR = cv2.remap(frameR, self.stereoMapR_x, self.stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
                

            processedImageL = self.myColorconverter.main_process_pipeline(frameL)
            processedImageR = self.myColorconverter.main_process_pipeline(frameR)

            # pass the filtered contours from the left and right frames to the contour matching function
            matchedContours = self.myColorconverter.contour_matching(processedImageL[7], processedImageR[7])


            # Draw contours on the original frames ----------------------------------------
            # SKAL FLYTTES TIL EGEN FUNKSJON TIL MANDAG
            for x in matchedContours:
                cv2.drawContours(frameL, x[0], -1, (0,255,0), 3)
                cv2.drawContours(frameR, x[1], -1, (0,255,0), 3)

                # find center of contours
                M = cv2.moments(x[0])
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                M = cv2.moments(x[1])
                cX1 = int(M["m10"] / M["m00"])
                cY1 = int(M["m01"] / M["m00"])

                # draw the contour and center of the shape on the image
                cv2.circle(frameL, (cX, cY), 7, (255, 255, 255), -1)
                cv2.putText(frameL, "center", (cX - 20, cY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.circle(frameR, (cX1, cY1), 7, (255, 255, 255), -1)
                cv2.putText(frameR, "center", (cX1 - 20, cY1 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
            # --------------------------------------------------------------------------------

            # Convert frames to RGB format for display in top labels
            topLabelFrameL = cv2.cvtColor(frameL, cv2.COLOR_BGR2RGB)
            topLabelFrameR = cv2.cvtColor(frameR, cv2.COLOR_BGR2RGB)

            # Convert frames to HSV format for color conversion
            imageL = ImageTk.PhotoImage(Image.fromarray(topLabelFrameL))
            imageR = ImageTk.PhotoImage(Image.fromarray(topLabelFrameR))

            # Update topImgL and topImgR labels with the original frames
            self.topImgL.configure(image=imageL)
            self.topImgL.image = imageL
            self.topImgR.configure(image=imageR)
            self.topImgR.image = imageR

            # Display the processed image in the bottom labels if the function was successful
            if processedImageL[0] == True and processedImageR[0] == True:

                selecedOutput = self.image_output.get()
                selectedOutputIndex = self.options.index(selecedOutput)
                
                # Create PhotoImage objects for botImgL and botImgR labels
                imageL = ImageTk.PhotoImage(Image.fromarray(processedImageL[selectedOutputIndex +1]))
                imageR = ImageTk.PhotoImage(Image.fromarray(processedImageR[selectedOutputIndex +1]))

                # Update botImgL and botImgR labels with the calibrated frames
                self.botImgL.configure(image=imageL)
                self.botImgL.image = imageL
                self.botImgR.configure(image=imageR)
                self.botImgR.image = imageR

    def update(self):

        ret,frameL = self.capL.read()
        ret1,frameR = self.capR.read()



        if ret and ret1:
            self.updateCameraFrames(frameL, frameR)

        self.window.after(25, self.update)




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

    def scaler_satMin(self, value):
        rounded_value = round(float(value)) 
        self.myColorconverter.satMinL = int(rounded_value)
        self.satMinL.config(text=f'{rounded_value}')     

    def scaler_satMax(self, value):
        rounded_value = round(float(value)) 
        self.myColorconverter.satMaxL = int(rounded_value)
        self.satMaxL.config(text=f'{rounded_value}')

    def scaler_hueMin(self, value):
        rounded_value = round(float(value)) 
        self.myColorconverter.hueMinL = int(rounded_value)
        self.hueMinL.config(text=f'{rounded_value}')
  
    def scaler_hueMax(self, value):
        rounded_value = round(float(value)) 
        self.myColorconverter.hueMaxL = int(rounded_value)
        self.hueMaxL.config(text=f'{rounded_value}')

    def scaler_valMin(self, value):
        rounded_value = round(float(value)) 
        self.myColorconverter.valMinL = int(rounded_value)
        self.valMinL.config(text=f'{rounded_value}')

    def scaler_valMax(self, value):
        rounded_value = round(float(value)) 
        self.myColorconverter.valMaxL = int(rounded_value)
        self.valMaxL.config(text=f'{rounded_value}')
    
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

class Colorconverter():
    def __init__(self) -> None:
        # self.frameL = frameL
        # self.frameR = frameR
        self.hueMinL = 120
        self.hueMaxL = 11
        self.satMinL = 120
        self.satMaxL = 255
        self.valMinL = 79
        self.valMaxL = 255
        self.erodeL = None
        self.erodeR = None
        self.maskL = None
        self.maskR = None
        # self.hsvL = cv2.cvtColor(frameL, cv2.COLOR_BGR2HSV)
        # self.hsvR = cv2.cvtColor(frameR, cv2.COLOR_BGR2HSV)

    def mask_from_HSV(self, HSVImage, hueMinL, hueMaxL, satMinL, satMaxL, valMinL, valMaxL):
        
        '''
        Creates a binary mask based on the HSV values given by UI sliders.

        Parameters:
            A HSV image 
         
        Returns: 
            Whether or not the funtion was successful (Bool true/false)
            A binary image 
        '''

        try: 
            if hueMinL > hueMaxL:
                # If hueMin is greater than hueMax, the mask must be created in two parts and combined
                maskl = cv2.inRange(HSVImage, (0, satMinL, valMinL), (hueMaxL, satMaxL, valMaxL))
                maskh = cv2.inRange(HSVImage, (hueMinL, satMinL, valMinL), (255, satMaxL, valMaxL))
                binaryMask = cv2.bitwise_or(maskl, maskh)

            else:
                # If hueMin is less than hueMax, the mask can be created in one part
                binaryMask = cv2.inRange(HSVImage, (hueMinL, satMinL, valMinL), (hueMaxL, satMaxL, valMaxL))
            
            return True, binaryMask 
        except: 
            print("Error: Could not create mask")
            return False, None
        

    def erode_binary_mask(self, binaryImage):
        '''
        Erodes a binary image to remove noise.

        Parameters:
            A binary image

        Returns:
            Whether or not the function was successful (Bool true/false)
            A binary image
        '''
        try:

            # create a kernel for erosion (!SIZE MUST BE ODD!, for example (5,5))
            kernel = np.ones((5,5), np.uint8)

            erodedMask = cv2.erode(binaryImage, kernel, iterations=1)

            return True, erodedMask
        
        except: 
            print("Error: Could not erode mask")
            return False, None

    def dilate_binary_mask(self, binaryImage):
            '''
            Dilates a binary image to restore original shapes.

            Parameters:
                A binary image

            Returns:
                Whether or not the function was successful (Bool true/false)
                A binary image
            '''
            try: 

                # create a kernel for dialation (!SIZE MUST BE ODD!, for example (5,5))
                kernel = np.ones((5,5), np.uint8)

                dialatedMask = cv2.dilate(binaryImage, kernel, iterations=1)

                return True, dialatedMask
            
            except:
                print("Error: Could not dilate mask")
                return False, None
            
    def find_contours(self, binaryImage):
        '''
        Finds contours in a binary image. 

        Parameters:
            MatLike: A binary image

        Returns:
            Bool: Whether or not the function was successful (Bool true/false)
            Tuple: A chaincode for all contours in the image
        '''

        try:
            # Find contours in the binary image
            contours = cv2.findContours(binaryImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            
            return True, contours
        
        except:
            print("Error: Could not find contours")
            return False, None

    def filter_contour_by_size(self, contourstobefiltered, contourMinSize): 
        '''
        Filters contours by size. 

        Parameters:
            Tuple: A chaincode for all contours in the image
            Int: The minimum size of the contours to be kept

        Returns:
            Bool: Whether or not the function was successful (Bool true/false)
            Tuple: Chaincode for all the contours that are larger than the minimum size
        '''

        try:
            # Filter contours by size
            filteredContours = []
            for x in contourstobefiltered:
                if cv2.contourArea(x) > contourMinSize:
                    filteredContours.append(x)
            
            return True, filteredContours
        
        except:
            print("Error: Could not filter contours by size")
            return False, None
        
    def draw_contours(self, image, contours):
        '''
        Draws contours on an image. 

        Parameters:
            MatLike: An image
            Tuple: A chaincode for all contours in the image

        Returns:
            Bool: Whether or not the function was successful (Bool true/false)
            MatLike: An image with the contours drawn on it
        '''

        try:
            # Draw contours on the image
            imageCopy = image.copy()
            cv2.drawContours(imageCopy, contours, -1, (0,255,0), 2)

            return True, imageCopy
        
        except:
            print("Error: Could not draw contours")
            return False, None
        
    def main_process_pipeline(self, frame):
        
        '''
        The main process pipeline for a single camera. 

        Parameters:
            MatLike: An image

        Returns: 
            Bool: Whether or not the function was successful (Bool true/false)
            MatLike: The original image
            MatLike: A binary mask
            MatLike: An eroded binary mask
            MatLike: A dilated binary mask
            MatLike: An image with contours drawn on it
            MatLike: An image with filtered contours drawn on it
            Tuple: A chaincode for all the filtered contours

        '''
        returnValues = [False, None, None, None, None, None]
        contourFilterSize = 1000

        # Convert frame to HSV
        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        maskSuccess, binaryMask = self.mask_from_HSV(hsvImage, self.hueMinL, self.hueMaxL, self.satMinL, self.satMaxL, self.valMinL, self.valMaxL)

        if maskSuccess == False: 
            return returnValues

        erodeSuccess, erodedMask = self.erode_binary_mask(binaryMask)

        if erodeSuccess == False:
            return returnValues
        
        dilateSuccess, dilatedMask = self.dilate_binary_mask(erodedMask)

        if dilateSuccess == False:
            return returnValues
        
        contourSuccess, contours = self.find_contours(dilatedMask)

        if contourSuccess == False:
            return returnValues
        
        drawSuccess, imageWithContours = self.draw_contours(frame, contours)

        if drawSuccess == False:
            return returnValues
        
        filterSuccess, filteredContours = self.filter_contour_by_size(contours, contourFilterSize)

        if filterSuccess == False:
            return returnValues
        
        drawSuccess, imageWithFilteredContours = self.draw_contours(frame, filteredContours)

        if drawSuccess == False:
            return returnValues
        
        returnValues = [True, frame ,binaryMask, erodedMask, dilatedMask,imageWithContours, imageWithFilteredContours, filteredContours]

        return returnValues
    
    def contour_matching(self, contoursFromLeftFrame, ContoursFromRightFrame):
        '''
        Matches contours from two frames.

        Parameters:
            Tuple: A chaincode for all contours in the left image
            Tuple: A chaincode for all contours in the right image

        Returns:
            Bool: Whether or not the function was successful (Bool true/false)
            List: A list of the best matches [chaincode for contour in left image, chaincode for contour in right image, match score]

        '''

        # Define empty lists for storing matches and matched contours
        allMatches = [] # contans all matches and their scores
        matchedContoursLeft = []
        matchedContoursRight = []
        bestMatches = []

        for idx, x in enumerate(contoursFromLeftFrame):
            for idy, y in enumerate(ContoursFromRightFrame):
                matchScore = cv2.matchShapes(x, y, 1, 0.0)
                allMatches.append([idx, idy, matchScore])

        # Sort the matches by score
        allMatches.sort(key=lambda match: match[2])

        # Find the best matches and add them to the bestMatches list
        # Also add the matched contours to the matchedContoursLeft and matchedContoursRight lists
        # This is done to avoid matching the same contour twice
        for x in allMatches:
            if x[0] not in matchedContoursLeft and x[1] not in matchedContoursRight:
                matchedContoursLeft.append(x[0])
                matchedContoursRight.append(x[1])
                bestMatches.append([contoursFromLeftFrame[x[0]], ContoursFromRightFrame[x[1]], x[2]])

        return bestMatches
    

    def stereo_triangulation(self, matches, contoursL, contoursR):
        '''
        Triangulates the matched contours from two frames.

        Parameters:
            List: A list of the best matches (Contains the index of the contour in the left image, the index of the contour in the right image and the match score)
            Tuple: A chaincode for all contours in the left image
            Tuple: A chaincode for all contours in the right image

        Returns:
            Bool: Whether or not the function was successful (Bool true/false)
            List: A list of the triangulated points
        ''' 

        triangulatedPoints = []

        for x in matches:
            # Get the coordinates of the matched contours
            leftContour = contoursL[x[0]]
            rightContour = contoursR[x[1]]

            # Find the center of the contours
            leftCenter = cv2.moments(leftContour)
            rightCenter = cv2.moments(rightContour)

            # Calculate the triangulated point
            triangulatedPoint = cv2.triangulatePoints(projMatrixL, projMatrixR, leftCenter, rightCenter)

            # Add the triangulated point to the list
            triangulatedPoints.append(triangulatedPoint)
    
if __name__ == '__main__':

    app = GUI()
    app.run()
