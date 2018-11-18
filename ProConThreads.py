import threading
import cv2
import numpy as np
import queue


class threadExtract(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()
    def run(self):

        name = "client.mp4"
        
        #frame number
        fCount = 0;

        #open file
        vidFile = cv2.VideoCapture()
    
