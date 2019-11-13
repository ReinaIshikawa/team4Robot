import subprocess
import socket
import string
import os
import random
import numpy as np
from numpy.random import *
import time

from Motor import Motor
from Motor_move import Motor_move
class Voice:


	def __init__(self):
		self.host = "localhost"
		self.port = 10500
		self.motor_speed = 1000
		self.state = 0

	def move(self):
		while True:
			if (self.state == 1):#前, 進め
				right.Run_forward()
				left.Run_forward()

			elif (self.state == 2):#右
				right.Turn_right()
				left.Turn_right()

			elif (self.state == 3):#左
				right.Turn_left()
				left.Turn_left()

			elif (self.state == 4):#後ろ
				right.Run_back()
				left.Run_back()

			if (self.state == 0):
				break
			time.sleep(1)

	def switchState(self, statenum):
		if(self.state != statenum)
			self.state = 0
			time.sleep(2)
			self.state = statenum
			move()

	if __name__=="__main__":

		p = subprocess.Popen(["./julius_start.sh"], stdout=subprocess.PIPE, shell=True)
		pid = str(p.stdout.read().decode('utf-8')) # juliusのプロセスIDを取得
		time.sleep(5)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((host, port))

		right = Motor_move(0,speed)
		left = Motor_move(1,speed)

		data =""
		killword = ""
		while True:

			while (1):
				if '</RECOGOUT>\n.' in data:
					#data = data + sock.recv(1024)
					strTemp = ""
					for line in data.split('\n'):
					index = line.find('WORD="')
						if index != -1:
						line = line[index+6:line.find('"',index+6)]
						strTemp += str(line)

						if strTemp == 'カメラ':
							if killword != 'カメラ':
								print ("Result: " + strTemp)
								#カメラを立ち上げて，自動的にbreak
								print ("<<<please speak>>>")
								killword = "カメラ"

						elif strTemp == '進め':
							if killword != '進め':
								print("Result: " + strTemp)
								switchState(1)
								print ("<<<please speak>>>")
								killword = "進め"

						elif strTemp == '前':
								if killword != "前":
								print("Result: " + strTemp)
								switchState(1)
								print ("<<<please speak>>>")
								killword = "前"

						elif strTemp == '後ろ':
							if killword != "後ろ":
								print("Result: " + strTemp)
								switchState(4)
								print("<<<please speak>>>")
								killword = "後ろ"

						elif strTemp == '右':
							if killword != "右":
								print("Result: " + strTemp)
								switchState(2)
								print ("<<<please speak>>>")
								killword = "右"

						elif strTemp == '左':
							if killword != "左":
								print("Result: " + strTemp)
								switchState(3)
								print ("<<<please speak>>>")
								killword = "左"

						elif strTemp == 'とまれ':
							if killword != "とまれ":
								print("Result: " + strTemp)
								self.state = 0
								print ("<<<please speak>>>")
								killword = "とまれ"

						elif strTemp == 'ストップ':
							if killword != "ストップ":
								print("Result: " + strTemp)
								self.state = 0
								print ("<<<please speak>>>")
								killword = "ストップ"

						elif strTemp == '友達':
							if killword != "友達":
								print("Result: " + strTemp)

								print ("<<<please speak>>>")
								killword = "友達"

						elif strTemp == 'ついて来て':
							if killword != "ついて来て":
								print("Result: " + strTemp)
								#何か返答
								print ("<<<please speak>>>")
								killword = "ついて来て"

						elif strTemp == '終了':
							if killword != "終了":
								print("Result: " + strTemp)
								move(0)
								print ("<<<please speak>>>")
								killword = "終了"

						else:
							print("Result:" + strTemp)

							print ("<<<please speak>>>")
						data = ""

				else:
					data += str(sock.recv(1024).decode('utf-8'))