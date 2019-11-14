import json
import sys
import time
import pigpio
import dist

class DistThread(threading.Thread):
	def _init_(self, request, sensor):
		super(MotorThread, self)._init_()
		self.request = request
		self.sensor = sensor

	def run(self):
		while True:
			self.sensor.stdin.write(json.dumps({
				"response": dist.main()
			}) + '\n')
