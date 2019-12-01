import json
# 測距センサーの値をdist_inputで擬似的に返す

cnt = 0
while True:
    request = json.loads(input())
    response = {'dist': str(cnt)}
    # 例えば, request = {'module': 'sensor','cmd': 'check_dist'}
    # {"module": "sensor", "cmd": "check_dist"}
    if(request['cmd'] == 'check_dist'):
        print(
            json.dumps({'response': response, 'request': request}),
            flush=True
        )


'''
path = "Sensor/inputSample.txt"
with open(path, 'r') as f:
    for line in f:
        try:
            response = {'dist': line.replace('\n', '')}
            request = json.loads(input())
            # 例えば, request = {'module': 'sensor','cmd': 'check_dist'}
            if(request['cmd'] == 'check_dist'):
                print(json.dumps({'response': response, 'request': request}))
        except EOFError:
            pass
            # except IOError as e:
            # 	if e.errno == errno.EPIPE:
            # 		pass
        # time.sleep(0.1)
# この場合fileは手動closeした方が良いのか？
# -> Use with statement instead of manually closing the io
'''

'''
-------------------------------------
 本番スレッド
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
 			self.app.stdin.write(json.dumps({
 				"response": response, "request": self.request
 			}) + '\n')
'''
