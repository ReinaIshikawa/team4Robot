import json
import sys
import time
# import pigpio
import dist
import threading

#測距センサーの値をdist_inputで擬似的に返す
path = '. / dist_input_sample.txt'

while True:
	with open(path, "r") as file:
		for line in file:
			response = {"dist": line.rstrip('\n')}
			request = input()
			#例えば, request = {'module': 'sensor','cmd': 'check_dist'}
			if(request['cmd'] == 'check_dist'):
				self.app.stdin.write(json.dumps({
					"response": response, "request": request
				}) + '\n')
			time.sleep(0.1)
		#この場合fileは手動closeした方が良いのか？


#-------------------------------------
# 本番スレッド
# class DistThread(threading.Thread):
# 	def _init_(self, request, sensor, app):
# 		super(MotorThread, self)._init_()
# 		self.request = request
# 		self.sensor = sensor
# 		self.app = app

# 	def run(self):
# 		while True:
# 			#コールバック
# 			response = {"dist" : dist.main()}
# 			self.app.stdin.write(json.dumps({
# 				"response": response, "request": self.request
# 			}) + '\n')
