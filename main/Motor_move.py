#センサからの距離情報によって動きを決定する

import wiringpi as wp
import time
import struct
import Motor as Motor
import math
import ex #距離センサ

class Motor_move(Motor.Motor):
    dis=ex.main() #距離センサ
    #self.rad=
    #PID制御
    #目標までの距離を受け取り速度を出力する
    def PID(self):
        KP=200
        KI=10
        KD=10
        self.diff.insert(0,self.diff(1))
        self.diff.insert(1,self.dis)
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

    
    def Angle(self):
        KP=3
        KI=1
        KD=1
        self.angl=math.sin(self.rad)
        self.integrala+=math.cos(self.rad)*self.delta
        p=KP*self.angl
        i=KI*self.integrala
        d=KD*(-math.cos(self.rad))/self.delta
        setsp=p+i+d
        if self.id==1:
            setsp*=-1
        if setsp>30000:
            return 30000
        elif setsp<-30000:
            return -30000
        else:
            return setsp
        


        
