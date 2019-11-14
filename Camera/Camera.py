import json
import sys
import time
import pigpio
from Sensor.dist import main as dm
import threading
from mvnc import mvncapi as mvnc
from library import log
import os
import cv2
import queue
from OpenGL.GLUT import *
from OpenGL.GL import *
import numpy as np


mvnc.SetGlobalOption(mvnc.GlobalOption.LOG_LEVEL, 2)
devices = mvnc.EnumerateDevices()
if len(devices) == 0:
    log.communication("No devices found")
    quit()

devHandle   = []
graphHandle = []

with open("./graph", mode="rb") as f:
    graph = f.read()

for devnum in range(len(devices)):
    devHandle.append(mvnc.Device(devices[devnum]))
    devHandle[devnum].OpenDevice()
    graphHandle.append(devHandle[devnum].AllocateGraph(graph))
    graphHandle[devnum].SetGraphOption(mvnc.GraphOption.ITERATIONS, 1)
    iterations = graphHandle[devnum].GetGraphOption(mvnc.GraphOption.ITERATIONS)
log.communication("\nLoaded Graphs!!!")

for i in range(10):
    cam = cv2.VideoCapture(i)

    if cam.isOpened() != True:
        log.communication("Camera Open Error!!!")
        continue
    else:
        break
    
windowWidth = 1280
windowHeight = 640
cam.set(cv2.CAP_PROP_FRAME_WIDTH, windowWidth)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, windowHeight)

lock = threading.Lock()
frameBuffer = []
results = queue.Queue()
lastresults = None

LABELS = ('background',
        'aeroplane', 'bicycle', 'bird', 'boat',
        'bottle', 'bus', 'car', 'cat', 'chair',
        'cow', 'diningtable', 'dog', 'horse',
        'motorbike', 'person', 'pottedplant',
        'sheep', 'sofa', 'train', 'tvmonitor')

def init():
    glClearColor(0.7, 0.7, 0.7, 0.7)

def idle():
    glutPostRedisplay()

def resizeview(w, h):
    glViewport(0, 0, w, h)
    glLoadIdentity()
    glOrtho(-w / 1920, w / 1920, -h / 1080, h / 1080, -1.0, 1.0)

def keyboard(key, x, y):
    key = key.decode('utf-8')
    if key == 'q':
        lock.acquire()
        while len(frameBuffer) > 0:
            frameBuffer.pop()
        lock.release()
        for devnum in range(len(devices)):
            graphHandle[devnum].DeallocateGraph()
            devHandle[devnum].CloseDevice()
        log.communication("\n\nFinished\n\n")
        sys.exit()

def camThread():
    lastresults=None
    s, img = cam.read()

    if not s:
        log.communication("Could not get frame")
        return 0

    lock.acquire()
    if len(frameBuffer)>10:
        for i in range(10):
            del frameBuffer[0]
    frameBuffer.append(img)
    lock.release()
    res = None

    if not results.empty():
        res = results.get(False)
        flag,img,sumbox = overlay_on_image(img, res)
        if flag!=0:
            response = {"x":sumbox[0],"y":sumbox[1],"img":img.tolist()}
            jsn = json.dumps({"response": response})
            print(jsn,flush=True)
            log.communication('Human found!')
            # self.camera.stdin.write(jsn + '\n')
            # self.camera.stdin.flush()
        else:
            response = {"x":-1,"y":-1,"img":img.tolist()}
            # jsn = json.dumps({"response": response, 'request': request})
            jsn = json.dumps({"response": response})
            print(jsn,flush=True)
            # self.camera.stdin.write(jsn + '\n')
            # self.camera.stdin.flush()
            log.communication('Human not found!')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w = img.shape[:2]
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img)
        lastresults = res
        time.sleep(1)
    else:
        imdraw = overlay_on_image(img, lastresults)
        imdraw = cv2.cvtColor(imdraw, cv2.COLOR_BGR2RGB)
        h, w = imdraw.shape[:2]
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, imdraw)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glEnable(GL_TEXTURE_2D)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glBegin(GL_QUADS)
    glTexCoord2d(0.0, 1.0)
    glVertex3d(-1.0, -1.0,  0.0)
    glTexCoord2d(1.0, 1.0)
    glVertex3d( 1.0, -1.0,  0.0)
    glTexCoord2d(1.0, 0.0)
    glVertex3d( 1.0,  1.0,  0.0)
    glTexCoord2d(0.0, 0.0)
    glVertex3d(-1.0,  1.0,  0.0)
    glEnd()
    glFlush()
    glutSwapBuffers()

def inferencer(results, lock, frameBuffer, handle):
    failure = 0
    #time.sleep(3)
    while failure < 100:
        lock.acquire()
        if len(frameBuffer) == 0:
            lock.release()
            failure += 1
            continue

        img = frameBuffer[-1].copy()
        del frameBuffer[-1]
        failure = 0
        lock.release()

        now = time.time()
        im = preprocess_image(img)
        handle.LoadTensor(im.astype(np.float16), None)
        out, userobj = handle.GetResult()

        results.put(out)


def preprocess_image(src):
    img = cv2.resize(src, (300, 300))
    img = img - 127.5
    img = img * 0.007843
    return img

def overlay_on_image(display_image, object_info):
    sumbox=[0,0]
    flag=0
    if isinstance(object_info, type(None)):
        return display_image
    
    num_valid_boxes = int(object_info[0])
    img_cp = display_image.copy()

    if num_valid_boxes > 0:
        for box_index in range(num_valid_boxes):
            base_index = 7+ box_index * 7
            if (not np.isfinite(object_info[base_index]) or
                not np.isfinite(object_info[base_index + 1]) or
                not np.isfinite(object_info[base_index + 2]) or
                not np.isfinite(object_info[base_index + 3]) or
                not np.isfinite(object_info[base_index + 4]) or
                not np.isfinite(object_info[base_index + 5]) or
                not np.isfinite(object_info[base_index + 6])):
                continue

            x1 = max(0, int(object_info[base_index + 3] * img_cp.shape[0]))
            y1 = max(0, int(object_info[base_index + 4] * img_cp.shape[1]))
            x2 = min(img_cp.shape[0], int(object_info[base_index + 5] * img_cp.shape[0]))
            y2 = min(img_cp.shape[1], int(object_info[base_index + 6] * img_cp.shape[1]))

            x1_ = str(x1)
            y1_ = str(y1)
            x2_ = str(x2)
            y2_ = str(y2)
            if (object_info[base_index + 2])>flag:
                flag=int(object_info[base_index + 2])
                sumbox=[(int(x1_)+int(x2_))//2,(int(y1_)+int(y2_))//2]
        # log.communication('box at index: ' + str(box_index) + ' : ClassID: ' + LABELS[int(object_info[base_index + 1])] + '  '
            #   'Confidence: ' + str(object_info[base_index + 2]*100) + '%  ' +
            #     'Top Left: (' + x1_ + ', ' + y1_ + ')  Bottom Right: (' + x2_ + ', ' + y2_ + ')')
            """object_info_overlay = object_info[base_index:base_index + 7]

            min_score_percent = 10
            source_image_width = img_cp.shape[1]
            source_image_height = img_cp.shape[0]

            base_index = 0
            class_id = object_info_overlay[base_index + 1]
            percentage = int(object_info_overlay[base_index + 2] * 100)
            if (percentage <= min_score_percent):
                continue

            label_text = LABELS[int(class_id)] + " (" + str(percentage) + "%)"
            box_left = int(object_info_overlay[base_index + 3] * source_image_width)
            box_top = int(object_info_overlay[base_index + 4] * source_image_height)
            box_right = int(object_info_overlay[base_index + 5] * source_image_width)
            box_bottom = int(object_info_overlay[base_index + 6] * source_image_height)

            box_color = (255, 128, 0)
            box_thickness = 1
            cv2.rectangle(img_cp, (box_left, box_top), (box_right, box_bottom), box_color, box_thickness)

            label_background_color = (125, 175, 75)
            label_text_color = (255, 255, 255)

            label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            label_left = box_left
            label_top = box_top - label_size[1]
            if (label_top < 1):
                label_top = 1
            label_right = label_left + label_size[0]
            label_bottom = label_top + label_size[1]
            cv2.rectangle(img_cp, (label_left - 1, label_top - 1), (label_right + 1, label_bottom + 1), label_background_color, -1)
            cv2.putText(img_cp, label_text, (label_left, label_bottom), cv2.FONT_HERSHEY_SIMPLEX, 0.5, label_text_color, 1)"""
    if sumbox==[0,0]:
        return 0,img_cp,sumbox
    else:
        return 1,img_cp,sumbox

glutInitWindowPosition(0, 0)
glutInitWindowSize(1280,640) 
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE )
glutCreateWindow("DEMO")
glutDisplayFunc(camThread)
glutReshapeFunc(resizeview)
glutKeyboardFunc(keyboard)
init()
glutIdleFunc(idle)

threads = []

for devnum in range(len(devices)):
    t = threading.Thread(target=inferencer, args=(results, lock, frameBuffer, graphHandle[devnum]))
    t.start()
    threads.append(t)

glutMainLoop()