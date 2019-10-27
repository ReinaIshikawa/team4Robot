import cv2
import sys
import time
import face_detection as fd
def get_image():
    camera_id=0
    delay=1
    window_name='frame'

    cap=cv2.VideoCapture(camera_id)

    if not cap.isOpened():
        sys.exit()

    while True:
        
        #time.sleep(3)
        ret,frame=cap.read()
        frame=fd.face-detection(frame)
        cv2.imshow(window_name,frame)
        print("a")
        if cv2.waitKey(delay)&0xFF==ord('q'):
            break

    cv2.destroyWindow(window_name)

get_image()
