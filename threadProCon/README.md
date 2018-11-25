# ProConThread.py

- ProConThread.py contains three thread classes; threadExtract, threadGray and
  threadDisp.
- threadExtract takes a video file and reads it frame by frame, encoding it
  and placing it in a buffer.
- threadGray takes frames from the buffer, decodes and converts them to grayscale, and
  places them in a second buffer.
- threadDisp reads converted frames from the second buffer and displays them
  on screen.
  
All three threads use semaphores (two sets of empty/fill semaphores) upon accessing buffers in order to run simultaneously while avoiding conflict in produce-consume cycles!

# How to Run
To run ProConThread.py:
- enter "python3 ProConThread.py, OR
- enter "./ProConThread.py"
