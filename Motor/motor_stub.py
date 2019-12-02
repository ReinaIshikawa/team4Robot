import threading
# import time


class MotorStub(threading.Thread):
    def __init__(self, app):
        super(MotorStub, self).__init__()
        # self.request = request
        self.app = app
        self.cnt = 0

    def run(self, request=None):
        if not request:
            return
        print('motor_thread->motor: {}:{}'.format(self.cnt, request))
        self.cnt += 1
