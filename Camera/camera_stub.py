import sys
import time
import Camera
import json


while True:
	request = json.loads(input())
	cmd = request['cmd']
	if (cmd == 'imag'):
		#do something
	time.sleep(1)
