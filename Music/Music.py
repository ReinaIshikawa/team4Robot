# やりたいこと概要用
import subprocess
import time
import Motor
import servo
import Motor_move

def Music_app(self):
    # 音楽を流す
    subprocess.call("mpg321 ファイル名",shell=True)

    # 体を動かす,サーボモータで腕を動かしつつステップを踏む(?)
    tmptime=0
    right = Motor_move(0, 20000)
    left=Motor_move(1,20000)
    Servo0 = servo_Class(Channel=0, ZeroOffset=-5)
    while tmptime<60:
        if tmptime<=30:
            right.Turn_right()
            left.Turn_right()
        else:
            right.Turn_left()
            left.Turn_left()
        if tmptime%5==0:
            Servo0.SetPos(90)
        else:
            Servo0.SetPos(45)
        tmptime+=5
