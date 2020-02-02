import threading
import client
from library import log
import cv2
import requests

def pursuit_listener1(response):
    # メインモータースレッドに距離を渡す
    # 速度は向こうで制御してくれる
    dist = response['dist']
    client.motor_dist_check(30)
    # if dist!=0:
    #     client.motor_dist_check(dist)
    # # 再帰的に(繰り返し)処理をするため
    # # runの方にwhile文で書いてもいいかも
    #     client.get_dist(pursuit_listener1)

def pursuit_listener2(response):
    # メインモータースレッドに距離を渡す
    # 速度は向こうで制御してくれ
    x = response['x']
    y = response['y']
    log.communication("[test_yamada] pursuit listener2")
    log.communication(str(x)+":"+str(y))
    if not(x>0.6 and x<0.4):
        client.motor_angle_check(x,y)
        client.get_angle(pursuit_listener2)
        #client.get_angle(pursuit_listener2)

def PythonNotify(message, *args):
    # 諸々の設定
    line_notify_api = 'https://notify-api.line.me/api/notify'
    line_notify_token = 'XXCuJEgSWFlU3iLK83hiqxQMRczqTIxT8hMqK3KcYTx' #メモしておいたアクセストークンに置換
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    # メッセージ
    payload = {'message': message}
    # 画像を含むか否か
    if len(args) == 0:
        requests.post(line_notify_api, data=payload, headers=headers)
    else:
        # 画像
        files = {"imageFile": open("example.jpg", "rb")}
        #files=arg
        requests.post(line_notify_api, data=payload, headers=headers, files=files)

def picture():
    log.communication("picture_get")
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite("example.jpg",frame)
    cv2.destroyAllWindows()
    #frame=cv2.imread('example.jpg')
    message="ok"
    PythonNotify(message, frame)


class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()
    def run(self):
        client.get_angle(pursuit_listener2)
        #print("-----")
        #log.communication("finishgetangle")
        client.motor_move("back")
        picture()
        """client.app_yamada()
        picture()"""


# 実行
thread = MainThread()
client.startListener(thread)
