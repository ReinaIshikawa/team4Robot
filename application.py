import argparse
import requests
import cv2
import sys
#sys.path.append("./Motor")
from Motor import Motor

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
        files = {"imageFile": open(args[0], "rb")}
        requests.post(line_notify_api, data=payload, headers=headers, files=files)

def picture():
    movement()
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    #cv2.imwrite("LennaG.png",img)
    PythonNotify(message, frame)

def movement():
    device=Motor.Motor()
    deveice.Run_back()
picture()
