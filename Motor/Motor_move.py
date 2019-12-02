#センサからの距離情報によって動きを決定する

import wiringpi as wp
import time
import struct
import Motor as Motor
import math
import ex #距離センサ

class Motor_move(Motor.Motor):
    #PID制御
    #目標までの距離を受け取り速度を出力する
    def PID(self, dis):
        KP=200
        KI=10
        KD=10
        self.diff.insert(0,self.diff(1))
        self.diff.insert(1,dis)
        self.integrald+=(self.diff(0)+self.diff(1))/2.0*self.delta
        p=KP*self.diff(1)
        i=KI*self.integrald
        d=KD*(self.diff(1)-self.diff(0))/self.delta
        if p+i+d>30000:
            return 30000
        elif p+i+d<-30000:
            return -30000
        else:
            return p+i+d

    def Angle(self,x,y):
        ox=50
        oy=50
        KP=500
        KI=10
        KD=10
        sinx=(x-ox)/math.sqrt((x-ox)*(x-ox)+(y-oy)*(y-oy))
        cosx=(x-ox)/math.sqrt((x-ox)*(x-ox)+(y-oy)*(y-oy))
        self.diff.insert(0,self.diff(1))
        self.diff.insert(1,cosx)
        self.integrald+=sinx
        p=KP*self.diff(1)
        i=KI*self.integrald
        d=KD*sinx
        ans=20*(-p-i+d)
        if p+i+d>30000:
            return 30000
        elif p+i+d<-30000:
            return -30000
        else:
            if self.id==0:
                return ans
            else:
                return - 1 * ans
