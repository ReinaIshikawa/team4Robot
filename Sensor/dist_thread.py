import json
import sys
import time
import pigpio
from Sensor.dist import main as dm
import threading

class DistThread(threading.Thread):
    def __init__(self, app):
        super(DistThread, self).__init__()
        self.app = app

    def run(self, request=None):
        if not request:
            return
        response = {"dist" : dm}
        print('motor_thread->motor: {}:{}'.format(response, request))
        #コールバック
