#センサからの距離情報によって動きを決定する

import wiringpi as wp
import time
import struct
import Motor as Motor
import ex #距離センサ

class Motor_move(Motor.Motor):
    dis=ex.main() #距離センサ
    #def motormove(self):
     #  if self.dis>safe:
     #       self.Run_forward()
     #   else :
     #       self.Run_back()
    
    #PID制御
    #目標までの距離を受け取り速度を出力する
    def PID(self):
        KP=0.3
        KI=0.1
        KD=0.1
        self.diff.insert(0,self.diff(1))
        self.diff.insert(1,self.dis)
        self.integral+=(self.diff(0)+self.diff(1))/2.0*self.delta
        p=KP*self.diff(1)
        i=KI*self.integral
        d=KD*(self.diff(1)-self.diff(0))/self.delta
        print("ohayou")
        if p+i+d>30000:
            return 30000
        elif p+i+d<-30000:
            return -30000
        else:
            return p+i+d
        
