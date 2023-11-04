import cv2
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from PIL import Image, ImageTk
import numpy as np

class CameraViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Viewer")

        # Create two frames to display camera feeds
        self.frame1 = ttk.Frame(self.root)
        self.frame1.pack(side=tk.LEFT, padx=10, pady=10)
        self.frame2 = ttk.Frame(self.root)
        self.frame2.pack(side=tk.RIGHT, padx=10, pady=10)

        # Initialize OpenCV video capture for two cameras
        self.cap1 = cv2.VideoCapture(0)
        self.cap2 = cv2.VideoCapture(2)

        # Create labels for camera feed displays
        self.label1 = ttk.Label(self.frame1, text="Camera 1")
        self.label1.pack()
        self.label2 = ttk.Label(self.frame2, text="Camera 2")
        self.label2.pack()

        # Start a loop to continuously update camera feeds
        self.update()

    def update(self):
        ret1, frame1 = self.cap1.read()
        ret2, frame2 = self.cap2.read()

        if ret1 and ret2:
            # Convert OpenCV BGR frames to RGB
            frame1_rgb = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            frame2_rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

            # Convert frames to PIL Image
            image1 = Image.fromarray(frame1_rgb)
            image2 = Image.fromarray(frame2_rgb)

            # Convert PIL Images to Tkinter PhotoImage
            photo1 = ImageTk.PhotoImage(image=image1)
            photo2 = ImageTk.PhotoImage(image=image2)

            # Update labels with new frames
            self.label1.config(image=photo1)
            self.label1.image = photo1
            self.label2.config(image=photo2)
            self.label2.image = photo2

        # Schedule the update method to run again after 10ms
        self.root.after(10, self.update)

    def __del__(self):
        # Release camera resources when the application is closed
        self.cap1.release()
        self.cap2.release()

if __name__ == "__main__":
    root = tk.Tk()
    style = Style(theme='superhero')
    app = CameraViewer(root)
    root.mainloop()

                cv2.drawChessboardCorners(imgL, chessboardSize, cornersL, retL)
                self.save_traceL = cv2.imwrite('Python/Calibration/images/LeftTrace/TraceL' + str(self.bildenr1) + '.png', imgL)
                cv2.drawChessboardCorners(imgR, chessboardSize, cornersR, retR)
                self.save_traceR = cv2.imwrite('Python/Calibration/images/RightTrace/TraceR' + str(self.bildenr1) + '.png', imgR)
                self.bildenr1 += 1 # Increment bildenr1 with +1
                cv2.waitKey(10)
    
            if frameL is not None and frameR is not None:
            frameL = cv2.cvtColor(frameL, cv2.COLOR_BGR2RGB)
            frameR = cv2.cvtColor(frameR, cv2.COLOR_BGR2RGB)

            self.imageSourceL = Image.fromarray(frameL)
            imageL = ImageTk.PhotoImage(self.imageSourceL)
            self.imageSourceR = Image.fromarray(frameR)
            imageR = ImageTk.PhotoImage(self.imageSourceR)
            # print(frameL.min(), frameL.max())
            # print(frameR.min(), frameR.max())

            self.topImgL.configure(image=imageL)
            self.topImgL.image = imageL
            self.topImgR.configure(image=imageR)
            self.topImgR.image = imageR

            self.botImgL.configure(image=imageL)
            self.botImgL.image = imageL
            self.botImgR.configure(image=imageR)
            self.botImgR.image = imageR