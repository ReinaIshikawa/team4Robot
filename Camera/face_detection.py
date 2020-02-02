import time
import picamera
import cv2 as cv

# カメラ初期化
def face_detection(image):
        img =image
        grayimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        face_cascade = cv.CascadeClassifier('opencv-master/data/haarcascades/haarcascade_frontalface_default.xml')
        facerect = face_cascade.detectMultiScale(grayimg, scaleFactor=1.2, minNeighbors=2, minSize=(1, 1))
        if len(facerect) > 0:
                for rect in facerect:
                        cv.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 0, 255), thickness=3)
        return img
