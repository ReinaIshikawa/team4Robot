# import requests
import json
import sys
import time
# import wiringpi as wp
import struct
# from Motor import Motor
# import Motor_move as Mmove
# import threading


#テスト用ファイル
#センサからの距離情報によって動きを決定する

def PID(dist):
	KP=200
	KI=10
	KD = 10

	#仮
	diff_1 = 0
	diff_2 = dist
	self_integraled = 2
	self_delta = 1
	p=KP*diff_1
	i=KI*self_integraled
	d=KD*(diff_1-diff_0)/self_delta

	if p+i+d>30000:
		return 30000
	elif p+i+d<-30000:
		return -30000
	else:
		return p + i + d

def Angle(x, y):
	ox=50
	oy=50
	KP=500
	KI=10
	KD = 10
	sinx=(x-ox)/math.sqrt((x-ox)*(x-ox)+(y-oy)*(y-oy))
	cosx=(x-ox)/math.sqrt((x-ox)*(x-ox)+(y-oy)*(y-oy))

	#仮
	p=KP*0
	i=KI*0
	d=KD*sinx
	ans=20*(-p-i+d)
	if p+i+d>30000:
		return 30000
	elif p+i+d<-30000:
		return -30000
	else:
		if self.id==0:
			return ans
		else:
			return - 1 * ans

def Move(direction):
	if (direction == 'front'):
		time.sleep(1)
	elif (direction == 'back'):
		time.sleep(1)
	elif (direction == 'right'):
		time.sleep(1)
	elif (direction == 'left'):
		time.sleep(1)
	elif (direction == 'stay'):
		time.sleep(1)


while True:
	try:
		request = json.loads(input())
		cmd = request['cmd']
		if (cmd == 'check_dist'):
			dist = PID(request['dist'])
		elif (cmd == 'check_angle'):
			angle = Angle(request['x'], reequest['y'])
		elif (cmd == 'move'):
			Move(request['direction'])
	except EOFError:
		pass
	# time.sleep(0.1)




#--------------------------
#本番スレッド
#Motor_move.pyとThreading.Threadを継承?
#初期化の方法は...考える
#1. 距離を受け取り速度を制御
#2. 座標を受け取り角度を制御
#(3. コマンドを受け取り，速度と角度を制御)

# class MotorThread(threading.Thread, Motor):
# 	def _init_(self, request, motor, app):
# 		super(MotorThread, self)._init_()
# 		self.request = request
# 		self.motor = motor
# 		self.speed = 20000
# 		self.app = app

  #PID制御
  #目標までの距離を受け取り速度を出力する
  # def PID(self): ....

  # def Angle(self,x,y): ....

# 	def run(self):
# 		right = Motor_move(0, speed)
# 		left=Motor_move(1,speed)

# 		while True:
# 			if self.request['cmd'] == 'front':
# 				right.Run_forward()
# 				left.Run_forward()
# 				time.sleep(1)

# 			elif self.request['cmd'] == 'back':
# 				right.Run_back()
# 				left.Run_back()
# 				time.sleep(1)

# 			elif self.request['cmd'] == 'right':
# 				right.Turn_right()
# 				left.Turn_right()
# 				time.sleep(1)

# 			elif self.request['cmd'] == 'left':
# 				right.Turn_left()
# 				left.Turn_left()
# 				time.sleep(1)

# 			elif self.request['cmd'] == 'stop':
# 				right.Softstop()
# 				left.Softstop()
# 				right.Softhiz()
# 				left.Softhiz()
# 				self.request['cmd'] = 'stay':

# 			elif self.request['cmd'] == 'stay':
# 				continue
