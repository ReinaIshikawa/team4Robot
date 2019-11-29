import json
import sys
import time
import pigpio
import dist
import threading

class DistThread(threading.Thread):
	def _init_(self, request, sensor, app):
		super(MotorThread, self)._init_()
		self.request = request
		self.sensor = sensor
		self.app = app

	def run(self):
		while True:
			#コールバック
			response = {"dist" : dist.main()}
			# response = {"dist" :100}
			self.app.stdin.write(json.dumps({
				"response": response, "request": self.request
			}) + '\n')
