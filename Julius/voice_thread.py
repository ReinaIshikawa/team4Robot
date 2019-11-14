import threading
import json
import time
import socket
from library import log

#change host and port number
host = '127.0.0.1' #localhost
port = 10500   #julisuサーバーモードのポート

class VoiceThread(threading.Thread):

    def __init__(self, app, voice, exitCore):
        super(VoiceThread, self).__init__()
        self.app = app
        self.voice = voice
        self.exitCore = exitCore
        self.cnt = 0

    def run(self, request=None):
        if not request:
            return
        print('viuce_thread->voice: {}:{}'.format(self.cnt, request))
        self.cnt += 1

        # juliusのプロセスIDを取得
        pid = str(self.voice.stdout.read().decode('utf-8'))
        time.sleep(5)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        data =""
        killword = ""
        while True:
            while (1):
                if '</RECOGOUT>\n.' in data:
                    #data = data + sock.recv(1024)
                    strTemp = ""
                    for line in data.split('\n'):
                        index = line.find('WORD="')
                        if index != -1:
                            line = line[index+6:line.find('"',index+6)]
                            strTemp += str(line)
                        response={}
                        if strTemp == 'カメラ':
                            if killword != 'カメラ':
                                print ("Result: " + strTemp)
                                #カメラを立ち上げて，自動的にbreak
                                response['module'] = 'camera'
                                print ("<<<please speak>>>")
                                killword = "カメラ"

                        elif strTemp == '進め':
                            if killword != '進め':
                                print("Result: " + strTemp)
                                response['module'] = 'motor'
                                print ("<<<please speak>>>")
                                killword = "進め"

                        elif strTemp == '前':
                            if killword != "前":
                                print("Result: " + strTemp)
                                #request['module'] = 'motor'
                                response['motor_cmd'] = 'front'
                                print ("<<<please speak>>>")
                                killword = "前"

                        elif strTemp == '後ろ':
                            if killword != "後ろ":
                                print("Result: " + strTemp)
                                #request['module'] = 'motor'
                                response['motor_cmd'] = 'back'
                                print("<<<please speak>>>")
                                killword = "後ろ"

                        elif strTemp == '右':
                            if killword != "右":
                                print("Result: " + strTemp)
                                #request['module'] = 'motor'
                                response['motor_cmd'] = 'right'
                                print ("<<<please speak>>>")
                                killword = "右"

                        elif strTemp == '左':
                            if killword != "左":
                                print("Result: " + strTemp)
                                #request['module'] = 'motor'
                                response['motor_cmd'] = 'left'
                                print ("<<<please speak>>>")
                                killword = "左"

                        elif strTemp == 'とまれ':
                            if killword != "とまれ":
                                print("Result: " + strTemp)
                                respinse['motor_cmd'] = 'stop'
                                print ("<<<please speak>>>")
                                killword = "とまれ"

                        elif strTemp == 'ストップ':
                            if killword != "ストップ":
                                print("Result: " + strTemp)
                                response['motor_cmd'] = 'stop'
                                print ("<<<please speak>>>")
                                killword = "ストップ"

                        elif strTemp == '友達':
                            if killword != "友達":
                                print("Result: " + strTemp)
                                #スルー
                                print ("<<<please speak>>>")
                                killword = "友達"

                        elif strTemp == 'ついて来て':
                            if killword != "ついて来て":
                                print("Result: " + strTemp)
                                #何か返答
                                print ("<<<please speak>>>")
                                killword = "ついて来て"

                        elif strTemp == '終了':
                            if killword != "終了":
                                print("Result: " + strTemp)
                                response['module'] = 'quit'
                                self.exitCore()
                                print ("<<<please speak>>>")
                                killword = "終了"

                        else:
                            print("Result:" + strTemp)
                            print ("<<<please speak>>>")
                        data = ""

                        jsn = json.dumps({"response":response, "request":request})
                        log.communication('voice_thread:' + str(response))
                        self.app.stdin.write((jsn + '\n').encode('utf-8'))
                        self.app.stdin.flush()
                        print('voice_thread->app: {}:{}'.format(response, request))

                else:
                    data += str(sock.recv(1024).decode('utf-8'))


                # response = self.voice.stdout.readline()
                # if (response == ''):
                # 	continue
                # response = response.replace('\n', '')

                # if response == 'cancel':
                # 	continue

                # if (state == 0):
                # 	self.app.stdin.write(json.dumps({
                # 	"response": response,
                # 	}) + '\n')

                # if (state == 1):
                # 	self.exitCore()
