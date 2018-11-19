import threading
from threading import Semaphore, Thread
import cv2
import numpy as np
import queue


sem1 = Semaphore(1)
sem2 = Semaphore(1)

extractionBuffer = queue.Queue()
grayBuffer = queue.Queue()
#dispBuffer = queue.Queue()

class threadExtract(threading.Thread):
    def __init__(self):        
        threading.Thread.__init__(self)
        #self.start()
    def run(self):
        
        global extractionBuffer

        name = "producer-consumer-lab-SpottieTea/client.mp4"
        
        #frame number
        fCount = 0;

        #open file
        vidFile = cv2.VideoCapture(name)

        s, image = vidFile.read()
        
        #push frames to the appropriate queue (to the extraction buffer)
        while s:
            #get frame (encoded as jpeg)
            jpegFrame = cv2.imencode('.jpg',image)

            #add to buffer
            extractionBuffer.put(jpegFrame)
            #read frame for next loop
            s,image = vidFile.read()

            fCount += 1
            
        print("Extraction complete!")

class threadGray(threading.Thread):
    def __init__(self):        
        threading.Thread.__init__(self)
        #self.start()
    def run(self):

        global extractionBuffer
        global grayBuffer
        global dispBuffer
                
        #frame number
        fCount = 0;

        #get frame
       
        
        #TODO: implement semaphores. For now, just make sure it works!
        #Push converted, grayscale frames to the grayscale Buffer grayBuffer, which will be
        #accessed by the extraction function
        while not extractionBuffer.empty():

            #get frame from buffer
            vidFrame = extractionBuffer.get()

            #decode frame
            deVidFrame = cv2.imdecode(vidFrame, cv2.IMREAD_UNCHANGED)
            #gray out frame
            grayFrame = cv2cvtColor(deVidFrame,cv2.COLOR_BGR2GRAY)
            #encode frame
            jpegFrame = cv2.imencode('.jpg',grayFrame)
            #put frame in buffer
            grayBuffer.put(jpegFrame)
            #increment frame count. Unused for now
            fCount += 1
            
        print("Conversion complete!")
class threadDisp(threading.Thread):
    def __init__(self):        
        threading.Thread.__init__(self)
        #self.start()
    def run(self):

        global grayBuffer
                
        #frame number
        fCount = 0;

        #get frame
       
        
        #TODO: implement semaphores. For now, just make sure it works!
        #Get grayscale buffers and display them!
        while not grayBuffer.empty():
            #get grayscale frame
            gFrame = grayBuffer.get()
            #decode grayscale frame
            frame =  cv2.imdecode(gFrame, cv2.IMREAD_UNCHANGED)
            #display frame
            cv2.imshow("Video",frame)
            #wait 42 seconds
            if cv2.waitKey(42) and 0xFF == ord("q"):
                break

            fCount += 1

    print("Display complete!")
    cv2.destroyAllWindows()    

#Running threads
eThread = threadExtract()
#gThread = threadGray()
#dThread = threadDisp()
