import json
import threading


class SensorStub(threading.Thread):
    def __init__(self, app):
        super(SensorStub, self).__init__()
        # self.request = request
        self.app = app
        self.cnt = 0

    def run(self, request):
        if not request:
            return
        request = json.loads(request)
        response = {'dist': str(self.cnt)}
        self.cnt += 1
        if(request['cmd'] == 'check_dist'):
            self.app.stdin.write(
                json.dumps({"response": response, 'request': request}) + '\n'
            )
