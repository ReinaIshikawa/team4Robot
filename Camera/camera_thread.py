

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

	def run(self, request=None):
		
		
		