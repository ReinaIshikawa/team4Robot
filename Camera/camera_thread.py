import pigpio
import sys
import time
import Camera
import json
import subprocess
import threading
import cv2
import numpy as np
import time

class CameraThread(threading.Thread):
    def __init__(self, app, camera, log):
        super(CameraThread, self).__init__()
        self.app = app
        self.camera = camera
        self.log = log

    def run(self, request=None):
        print("camera thread starts")
        if not request:
            return
        response={}
        if(request["cmd"] == "check_angle"):
            jsn_msg = {}
            count = 0
            while(not jsn_msg):
                count += 1
                jsn_msg = self.camera.stdout.readline().decode('utf-8')
                print("count:", count)
                time.sleep(1)
            print('[CameraThread] jsn {}'.format(jsn_msg))
            msg = json.loads(jsn_msg)
            print('[CameraThread] load done:dump {}'.format(msg))
            
            msg=msg['response']
            #print("msg.{}".format(msg))
            response = {"x":msg["x"],"y":msg["y"]}
            #print("response.{}".format(response))
            jsn = json.dumps({"response": response, "request": request})
            self.log.communication('recieved')
            self.app.stdin.write((jsn + '\n').encode('utf-8'))
            self.app.stdin.flush()
        if(request["cmd"] == "taking_picture"):
            #self.log.communication('[CameraThread] cmd recv {}'.format(request['cmd']))
            jsn_msg = self.camera.stdout.readline().decode('utf-8')
            #self.log.communication('[CameraThread] jsn {}'.format(jsn_msg))
            msg = json.loads(jsn_msg)
            #self.log.communication('[CameraThread] dump {}'.format(msg))
            print(msg)
            msg=msg['response']
#           self.log.communication("msg.{}".format(msg))
            self.communication("here here here hrere")
            cv2.imwrite("example.jpg",np.array(msg["img"]))
            response = {"x":msg["x"],"y":msg["y"]}
            
            jsn = json.dumps({"response": response, "request": request})
            self.log.communication('recieved')
            self.app.stdin.write((jsn + '\n').encode('utf-8'))
            self.app.stdin.flush()
        
