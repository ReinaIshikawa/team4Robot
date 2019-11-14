#!/usr/bin/env python
# -*- coding: utf-8 -*-
import  Adafruit_PCA9685
import time
import sys
import json
import servo

class ServoThread(threading.Thread):
	def _init_(self, request, servo):
		self.request = request
		self.servo = servo

	def run(self):
		servo0 = servo.servo_Class(Channel=0, ZeroOffset=-5)
		# servo1 = servo.servo_Class(Channel=1, ZeroOffset=-5)
		# servo2 = servo.servo_Class(Channel=2, ZeroOffset=-5)
