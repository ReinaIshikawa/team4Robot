# import requests
import json
import sys
import time
import wiringpi as wp
import struct
import Motor
import Motor_move as Mmove
import threading

class MotorThread(threading.Thread):
	def _init_(self, request, motor, app):
		super(MotorThread, self)._init_()
		self.request = request
		self.motor = motor
		self.speed = 20000
		self.app = app

	dis=ex.main() #距離センサ
	#self.rad=
	#PID制御
	#目標までの距離を受け取り速度を出力する
	def PID(self):
		KP=200
		KI=10
		KD=10
		self.diff.insert(0,self.diff(1))
		self.diff.insert(1,self.dis)
		self.integrald+=(self.diff(0)+self.diff(1))/2.0*self.delta
		p=KP*self.diff(1)
		i=KI*self.integrald
		d=KD*(self.diff(1)-self.diff(0))/self.delta
		if p+i+d>30000:
				return 30000
		elif p+i+d<-30000:
			return -30000
		else:
			return p+i+d


	def Angle(self,x,y):
		ox=50
		oy=50
		KP=500
        KI=10
        KD=10
        sinx=(x-ox)/math.sqrt((x-ox)*(x-ox)+(y-oy)*(y-oy))
        cosx=(x-ox)/math.sqrt((x-ox)*(x-ox)+(y-oy)*(y-oy))
        self.diff.insert(0,self.diff(1))
        self.diff.insert(1,cosx)
        self.integrald+=sinx
        p=KP*self.diff(1)
        i=KI*self.integrald
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
                return -1*ans

	def Move(direction):
		if (direction == 'front'):
			right.Run_forward()
			left.Run_forward()
			time.sleep(1)
		elif (direction == 'back'):
			right.Run_back()
			left.Run_back()
			time.sleep(1)
		elif (direction == 'right'):
			right.Turn_right()
			left.Turn_right()
			time.sleep(1)
		elif (direction == 'left'):
			right.Turn_left()
			left.Turn_left()
			time.sleep(1)
		elif (direction == 'stop'):
			right.Softstop()
			left.Softstop()
			right.Softhiz()
			left.Softhiz()
			time.sleep(1)
		elif (direction == 'stay'):
			time.sleep(1)

	def run(self):
		right = Motor_move(0, speed)
		left = Motor_move(1, speed)
		while True:
			try:
				request = json.loads(self.motor.stdout.readline())
				cmd = request['motor_cmd']
				if (cmd == 'check_dist'):
					dist = PID(request['dist'])
				elif (cmd == 'check_angle'):
					angle = Angle(request['x'], reequest['y'])
				elif (cmd == 'move'):
					Move(request['direction'])
			except EOFError:
				pass
			time.sleep(1)
