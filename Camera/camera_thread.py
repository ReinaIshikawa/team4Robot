#Core.pyから呼び出し

import pigpio
import sys
import time
import Camera
import json

class CameraThread(threading.Thread):
	def _init_(self, request, camera):
		super(CameraThread, self).__init__()
		self.request = request
		self.camera = camera

	def run(self):
		#とりあえずcamera.pyと同じことをするだけ
		Camera.get_image();
		# cmd = self.request['command']
		# if cmd == 'face_positions':
		#     self.camera.stdin.write(cmd + '\n')
		#     response = self.camera.stdout.readline()
		# response = json.loads(response)
		# self.app.stdin.write(json.dumps({"response":response, 'request':self.request}) + '\n')
