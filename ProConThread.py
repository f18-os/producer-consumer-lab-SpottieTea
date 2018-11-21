import threading
from threading import Semaphore, Thread
import cv2
import numpy as np
import queue
import base64

class Q:
    def __init__(self, initArray = []):
        self.a = []
        self.a = [x for x in initArray]
    def put(self, item):
        self.a.append(item)
    def get(self):
        a = self.a
        item = a[0]
        del a[0]
        return item
    def __repr__(self):
        return "Q(%s)" % self.a

#initialize semaphore
mut = Semaphore(1)
fill = Semaphore(0)
empty  = Semaphore(10)


mut2 = Semaphore(1)
fill2 = Semaphore(0)
empty2 = Semaphore(10)

extractionBuffer = Q()
grayBuffer = Q()

class threadExtract(threading.Thread):
    def __init__(self):        
        threading.Thread.__init__(self)
        #self.start()
    def run(self):

        global extractionBuffer

        # Initialize frame count 
        count = 0

        # open video file
        vidcap = cv2.VideoCapture("clip.mp4")

        # read first image
        success,image = vidcap.read()

        
        print("Reading frame {} {} ".format(count, success))
        count +=1
        
        while success:
            # get a jpg encoded frame
            success, jpgImage = cv2.imencode('.jpg', image)

            #encode the frame as base 64 to make debugging easier
            #jpgAsText = base64.b64encode(jpgImage)

            # add the frame to the buffer
            empty.acquire()
           # mut.acquire()
            extractionBuffer.put(jpgImage)
            #mut.release()
            fill.release()
            success,image = vidcap.read()
            print('Reading frame {} {}'.format(count, success))
            count += 1

        print("Frame extraction complete")
    


class threadGray(threading.Thread):
    def __init__(self):        

        threading.Thread.__init__(self)

    def run(self):

        global extractionBuffer
        global grayBuffer

        #frame number
        fCount = 0;

        #get frame
        
        #Push converted, grayscale frames to the grayscale Buffer grayBuffer, which will be
        #accessed by the extraction function
        while True:

            #get frame from buffer
            fill.acquire()
            #mut.acquire()
            vidFrameText = extractionBuffer.get()
            #mut.release()
            empty.release()
            #decode and gray out frame
            #vidFrame = base64.b64decode(vidFrameText)

            frame = np.asarray(bytearray(vidFrameText),dtype=np.uint8)
           
            vidFrameFinal = cv2.imdecode(frame,cv2.IMREAD_UNCHANGED)

            #print(vidFrameFinal)
            
            grayFrame = cv2.cvtColor(vidFrameFinal,cv2.COLOR_BGR2GRAY)

            #print(grayFrame)
            
            #put frame in buffer
            codeGray = cv2.imencode('.jpg',grayFrame)

            #print(codeGray)
            
            #codeGrayText = base64.b64encode(codeGray)

            empty2.acquire()
            #mut2.acquire()
            grayBuffer.put(grayFrame)
            #mut2.release()
            fill2.release()
            #increment frame count.
            print("Converted frame ",fCount)
            fCount += 1
            
        print("Conversion complete!")

class threadDisp(threading.Thread):
    def __init__(self):
        
        threading.Thread.__init__(self)
        
    def run(self):

        global grayBuffer

        print("Display begins...")
        #frame number
        fCount = 0;

        # go through each frame in the buffer until the buffer is empty
        while True:
            # get the next frame
            fill2.acquire()
            #mut2.acquire()
            frame = grayBuffer.get()
            #mut2.release()
            empty2.release()

            #print(frame)
            
            # decode the frame 
            #jpgRawImage = base64.b64decode(frameAsText)

            # convert the raw frame to a numpy array
            jpgImage = np.asarray(bytearray(frame), dtype=np.uint8)

            #print (jpgImage)
            
            # get a jpg encoded frame
            img = cv2.imdecode(jpgImage,cv2.IMREAD_UNCHANGED)

            print("Displaying frame {}".format(fCount))        

            # display the image in a window called "video" and wait 42ms
            # before displaying the next frame
            cv2.imshow("Video", img)
            if cv2.waitKey(42) and 0xFF == ord("q"):
                break

            fCount += 1

    print("Finished displaying all frames")
    # cleanup the windows
    cv2.destroyAllWindows()
    

#Running threads
eThread = threadExtract()
gThread = threadGray()
dThread=threadDisp()

eThread.start()
gThread.start()
dThread.start()
