import time
import threading


class VoiceStub(threading.Thread):
    def __init__(self, app):
        super(VoiceStub, self).__init__()
        self.app = app
        self.num = 0
        self.lst = ['カメラ', '前', '後ろ', '進め', '右', '左', 'とまれ', 'ついて来て', '終了']
    
    def run(self, request=None):
        if not request:
            return
        print('voice_thread->voice: {}'.format(self.lst[num]))
        self.num += 1
        if self.num == 9:
            self.num = 0
            