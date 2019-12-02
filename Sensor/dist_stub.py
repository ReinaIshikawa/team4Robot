import json
import threading


class SensorStub(threading.Thread):
    def __init__(self, app):
        super(SensorStub, self).__init__()
        # self.request = request
        self.app = app
        self.cnt = 0

    def run(self, request=None):
        if not request:
            return
        response = {'dist': str(self.cnt)}
        self.cnt += 1
        if(request['cmd'] == 'check_dist'):
            jsn = json.dumps({"response": response, 'request': request})
            self.app.stdin.write(jsn + '\n')
            self.app.stdin.flush()
            print('sensor_thread->app: {}'.format(jsn))
