import pigpio
import sys
import time
import Camera
import json
import subprocess
import threading


class CameraThread(threading.Thread):
	def __init__(self, app, camera):
		super(CameraThread, self).__init__()
		self.app = app
		self.camera = camera

	def run(self, request=None):
                if not request:
                        return
                response={}
                if(request["cmd"] == "check_angle"):
                        camera_glid = json.loads(self.camera.stdout.readline().decode('utf-8'))
                        if not (camera_glid["x"]  == -1):
                                response = {"x":camera_glid["x"],"y":camera_glid["y"]}
                jsn = json.dumps({"response": response},{"request": request})
                self.app.stdin.write((jsn + '\n').encode('utf-8'))
                self.app.stdin.flush()

			
		
		
