import pigpio
import sys
import time
import Camera
import json
import subprocess

class CameraThread(threading.Thread):
	def _init_(self, app, camera):
		super(CameraThread, self).__init__()
		self.app = app
		self.camera = camera

	def run(self, request=None):
		#  = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		reponse={}
		if(request["cmd"] == "check_angle"):
			camera_glid = self.camera.stdout.readline()
			if not (camera_glid["x"]  == -1):
				response = {"x":camera_glid["x"],"y":camera_glid["y"]}
            jsn = json.dumps({"response": response},{"request": request})
            self.app.stdin.write((jsn + '\n').encode('utf-8'))
            self.app.stdin.flush()

			
		
		