import time
import threading


class VoiceStub(threading.Thread):
    def __init__(self, app):
        super(VoiceStub, self).__init__()
        self.app = app
        self.num = 0
        self.lst = ['カメラ', '前', '後ろ', '進め', '右', '左', 'とまれ', 'ついて来て', '終了']

    def send_response(self, response, request):
        jsn = json.dumps({"response":response, "request":request})
        log.communication('voice_thread:' + str(response))
        print('voice_thread:' + str(response))
        self.app.stdin.write((jsn + '\n').encode('utf-8'))
        self.app.stdin.flush()
        print('voice_thread->app: {}:{}'.format(response, request))

    def run(self, request=None):
        if not request:
            return
        print('voice_thread->voice: {}'.format(self.lst[num]))
        while(1):
            response={}
            if self.num == 0:
                print('pass')
                # pass
            elif self.num == 1:
                response['direction'] = 'front'
                self.send_response(response, request)
            elif self.num == 2:
                response['direction'] = 'back'
                self.send_response(response, request)
            elif self.num == 3:
                response['direction'] = 'right'
                self.send_response(response, request)
            elif self.num == 4:
                response['direction'] = 'left'
                self.send_response(response, request)
            elif self.num == 5:
                response['direction'] = 'front'
                self.send_response(response, request)
            elif self.num == 5:
                response['direction'] = 'stop'
                self.send_response(response, request)
            elif self.num == 7:
                self.exitCore()
            self.num += 1
            if self.num == 9:
                self.num = 0
            time.sleep(5)