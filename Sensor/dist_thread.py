import json
import sys
import time
import pigpio
import dist
import threading

class DistThread(threading.Thread):
    def _init_(self, sensor, app):
        super(MotorThread, self)._init_()
        self.sensor = sensor
        self.app = app

    def run(self, request=None):
        if not request:
            return
        response = {"dist" : dist.main()}
        print('motor_thread->motor: {}:{}'.format(response, request))
        #コールバック