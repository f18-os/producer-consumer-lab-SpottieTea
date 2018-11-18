import threading
import cv2
import numpy as np
import queue

extractionBuffer = queue.Queue()
grayBuffer = queue.Queue()

class threadExtract(threading.Thread):
    def __init__(self):        
        Thread.__init__(self)
        self.start()
    def run(self):
        
        global extractionBuffer

        name = "producer-consumer-lab-SpottieTea/client.mp4"
        
        #frame number
        fCount = 0;

        #open file
        vidFile = cv2.VideoCapture(name)

        image = vidcap.read()

        while image:
            #get frame (encoded as jpeg)
            jpegFrame = cv2.imencode('.jpg',image)

            #add to buffer
            extractionBuffer.put(jpegFrame)

            image = vidcap.read()

            fCount += 1
            
        print("Extraction complete!")

class threadGray(threading.Thread):
    def __init__(self):        
        Thread.__init__(self)
        self.start()
    def run(self):

        global extractionBuffer
        global grayBuffer
                
        #frame number
        fCount = 0;

        #get frame
        vidFrame = extractionBuffer.get()
        
        #TODO: implement semaphores. For now, just make sure it works!
        while not extractionBuffer.empty():

            deVidFrame = cv2.imdecode(vidFrame, cv2.IMREAD_UNCHANGED) 
        
            fCount += 1
            
        print("Conversion complete!")
