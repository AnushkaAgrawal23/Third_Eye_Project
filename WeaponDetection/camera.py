import cv2
import imutils
import datetime
gun_cascade = cv2.CascadeClassifier('cascade.xml')

firstFrame = None
gun_exist = False

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        global gun_exist,firstFrame
        ret, frame = self.video.read()

        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize = (100, 100))
    
        if len(gun) > 0:
            gun_exist = True
            #ser.write(b'H')
        
        for (x,y,w,h) in gun:
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]    

        """if firstFrame is None:
            firstFrame = gray
            continue"""

        #print(datetime.date(2019))
        # draw the text and timestamp on the frame
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)


        if gun_exist:
            print("guns detected")
    
        else:
            print("guns NOT detected")

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
