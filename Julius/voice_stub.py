import time
import threading
import sys
import json


class VoiceStub(threading.Thread):
    def __init__(self, app,exitCore, changeApp):
        super(VoiceStub, self).__init__()
        self.app = app
        # self.voice = voice
        self.exitCore = exitCore
        self.changeApp = changeApp
        self.num = 0
        self.lst = ['カメラ', 'アニソン', '洋楽', '嵐', '前', '後ろ', '進め', '右', '左', 'とまれ', 'ついて来て', 'チェンジ', '終了', ]

    def send_response(self, response, request):
        jsn = json.dumps({"response":response, "request":request})
        # log.communication('voice_thread:' + str(response))
        print('voice_thread response:' + str(response))
        self.app.stdin.write((jsn + '\n').encode('utf-8'))
        self.app.stdin.flush()
        print('voice_thread->app: {}:{}'.format(response, request))

    def run(self, request=None):
        if not request:
            return
        print('voice_thread->voice: {}'.format(self.lst[self.num]))
        #while(1):
        response={}
        if self.num == 0:
            print('pass')
            # pass
        elif self.num == 1:
            response['music'] = 'anison'
        elif self.num == 2:
            response['music'] = 'yougaku'
        elif self.num == 3:
            response['music'] = 'arashi'
        elif self.num == 4:
            response['direction'] = 'front'
        elif self.num == 5:
            response['direction'] = 'back'
        elif self.num == 6:
            response['direction'] = 'right'
        elif self.num == 7:
            response['direction'] = 'left'
        elif self.num == 8:
            response['direction'] = 'front'
        elif self.num == 9:
            response['direction'] = 'stop'
        elif self.num == 10:
            print("pass")
        elif self.num == 11:# うまくいかない
            self.changeApp()
        elif self.num == 12:
            self.exitCore()
        self.send_response(response, request)
        self.num += 1
        if self.num == 11:# 終了はとりあえずなし(動作は確認済み)
            self.num = 0
        time.sleep(2)
