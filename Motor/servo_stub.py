import threading
from library import log

class ServoStub(threading.Thread):
    def __init__(self, app):
        super(ServoStub, self).__init__()
        # self.request = request
        self.app = app
        self.cnt = 0

    def run(self, request=None):
        if not request:
            return
        print('ServoStub: {}:{}'.format(self.cnt, request))
        self.cnt += 1
        self.request = request
        # 縦に動かす
        if self.request['cmd'] == 'clean':
            print("[ServoStub] cmd:", self.request['cmd'])

        # 横に動かす
        if self.request['cmd'] == 'attack':
            print("[ServoStub] cmd:", self.request['cmd'])

        # 止める
        if self.request['cmd'] == 'quit':
            print("[ServoStub] cmd:", self.request['cmd'])

        # attack.pyからの処理
        if(self.request['cmd'] == 'swing'):
            print("[ServoStub] cmd:", self.request['cmd'])