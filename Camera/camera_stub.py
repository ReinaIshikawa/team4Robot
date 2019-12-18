import sys
import time
import Camera
import json


while True:
	request = json.loads(input())
	cmd = request['cmd']
	if (cmd == 'imag'):
		pass
		#do something
	time.sleep(1)
