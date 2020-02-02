import json
import sys
import time
import pigpio
from Sensor.dist import main as dm
import threading
from library import log

class DistThread(threading.Thread):
    def __init__(self, app):
        super(DistThread, self).__init__()
        self.app = app

    def run(self, request=None):
        time.sleep(1)
        if not request:
            return
        if(request['cmd'] == 'check_dist'):
            distance = dm()
            response = {"dist" : distance}
            log.communication('dist_thread:' + str(distance))
            jsn = json.dumps({"response": response, 'request': request})
            self.app.stdin.write((jsn + '\n').encode('utf-8'))
            self.app.stdin.flush()
            print('dist_thread->dist: {}:{}'.format(response, request))
        #コールバック
