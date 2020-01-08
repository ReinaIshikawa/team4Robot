# import pigpio
import sys
import time
# import Camera
import json
# import subprocess
import threading
# import cv2
# import numpy as np

class CameraStub(threading.Thread):
    def __init__(self, app, camera, log):
        super(CameraStub, self).__init__()
        self.app = app
        self.camera = camera
        self.log = log
        self.msg_x = 10
        self.msg_y = 20

    def run(self, request=None):
        if not request:
            return
        response={}
        if(request["cmd"] == "check_angle"):
            self.log.communication('[CameraThread] cmd recv {}'.format(request['cmd']))
            response = {"x": self.msg_x, "y": self.msg_y}
            self.msg_x = self.msg_x + 5
            # write on pipe
            jsn = json.dumps({"response": response, "request": request})
            self.log.communication('recieved')
            self.app.stdin.write((jsn + '\n').encode('utf-8'))
            self.app.stdin.flush()
        if(request["cmd"] == "taking_picture"):
            self.log.communication('[CameraThread] cmd recv {}'.format(request['cmd']))
            print("-------- Are you ready? Say cheese!---------")
