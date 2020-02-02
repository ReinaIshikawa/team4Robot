import threading
import json
import time
import socket
import pygame.mixer
from library import log

#change host and port number
host = '0.0.0.0' #localhost
port = 10500   #julisuサーバーモードのポート

class VoiceThread(threading.Thread):

    def __init__(self, app, exitCore, changeApp):
        super(VoiceThread, self).__init__()
        self.app = app
        # self.voice = voice
        self.exitCore = exitCore
        self.changeApp = changeApp
        self.cnt = 0


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
        print('voice_thread->voice: {}:{}'.format(self.cnt, request))
        self.cnt += 1

        cmd = request['cmd']
        print('voice_thread check cmd:'+cmd)
        time.sleep(2)
        # get process ID
        # pid = str(self.voice.stdout.read().decode('utf-8'))
        # print('voice_thread get pid' + pid)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print('voice_thread bind socket')
        data =""
        # killword = ""
        while(1):
            # data = data + sock.recv(1024)
            if '</RECOGOUT>\n.' in data:
                strTemp = ""
                print(data)
                for line in data.split('\n'):
                    #index = line.find('WORD="')
                    index = line.find('WORD=')
                    if index != -1:
                        #line = line[index+6:line.find('"',index+6)]
                        line = line[index+6:line.find("CLASSID")-2]
                        strTemp += str(line)
                    response={}
                    if strTemp == u'カメラ':
                        # pass
                        log.communication("voice_result: " + strTemp)
                        continue
                    elif strTemp == u'進め':
                        if cmd == "voice_to_motor":
                            log.communication("voice_result: " + strTemp)
                            response['direction'] = 'front'
                            self.send_response(response, request)
                            break

                    elif strTemp == u'前':
                        if cmd == "voice_to_motor":
                            log.communication("voice_result: " + strTemp)
                            response['direction'] = 'front'
                            self.send_response(response, request)
                            break

                    elif strTemp == u'後ろ':
                        if cmd == "voice_to_motor":
                            log.communication("voice_result: " + strTemp)
                            response['direction'] = 'back'
                            self.send_response(response, request)
                            break

                    elif strTemp == u'右':
                        if cmd == "voice_to_motor":
                            log.communication("voice_result: " + strTemp)
                            response['direction'] = 'right'

                            self.send_response(response, request)
                            break

                    elif strTemp == u'左':
                        if cmd == "voice_to_motor":
                            log.communication("voice_result: " + strTemp)
                            response['direction'] = 'left'
                            self.send_response(response, request)
                            break

                    elif strTemp == u'とまれ':
                        if cmd == "voice_to_motor":
                            log.communication("voice_result: " + strTemp)
                            response['direction'] = 'stop'
                            self.send_response(response, request)
                            break

                    elif strTemp == 'ストップ':
                        if cmd == "voice_to_motor":
                            log.communication("voice_result: " + strTemp)
                            response['direction'] = 'stop'
                            self.send_response(response, request)
                            break


                    elif strTemp == 'アニソン':
                        if cmd == "voice_to_music":
                            log.communication("voice_result: " + strTemp)
                            response['music'] = 'anime'
                            self.send_response(response, request)
                            pygame.mixer.init()
                            pygame.mixer.music.load("../team4Robot/Julius/zankoku.mp3")
                            pygame.mixer.music.play(1)
                            time.sleep(15)
                            pygame.mixer.music.stop()
                            break

                    elif strTemp == '嵐':
                        if cmd == "voice_to_music":
                            log.communication("voice_result: " + strTemp)
                            response['music'] = 'arashi'
                            self.send_response(response, request)
                            pygame.mixer.init()
                            pygame.mixer.music.load("../team4Robot/Julius/arashi.mp3")
                            pygame.mixer.music.play(1)
                            time.sleep(15)
                            pygame.mixer.music.stop()
                            break

                    elif strTemp == '友達':
                        if cmd == "talk":
                            log.communication("voice_result: " + strTemp)
                            continue

                    elif strTemp == 'ついて来て':
                        if cmd == "talk":
                            continue

                    elif strTemp == 'チェンジ':
                        continue


                    elif strTemp == '終了':
                        log.communication("voice_result: " + strTemp)
                        self.exitCore()
                        break

                    else:
                        print("skip!")

                    data = ""

            else:
                data += str(sock.recv(1024).decode('utf-8'))
                log.communication("voice_thread: " + "Not found.")

            time.sleep(3)
