#センサからの距離情報によって動きを決定する

import wiringpi as wp
import time
import struct
from .Motor import Motor
import math
<<<<<<< HEAD
from Camera import MultiStickSSD as ms
=======
from Camera import MultiStickSSD 

>>>>>>> df79f3f879ab2a19b5c6a9cdb69e2cb2bd1ce6b0

class Motor_move(Motor):
    #PID制御
    #目標までの距離を受け取り速度を出力す
    diffnew=0
    
    def PID(self, dis):
        KP=200
        KI=10
        KD=10
        self.diffold=self.diffnew
        self.diffnew=dis
        self.integrald+=(self.diffold+self.diffnew)/2.0*self.delta
        p=KP*self.diffnew
        i=KI*self.integrald
        d=KD*(self.diffnew-self.diffold)/self.delta
        if p+i+d>30000:
            return 30000
        elif p+i+d<-30000:
            return -30000
        else:
            return p+i+d

    def Angle(self):
        ox=640
        oy=320
        dis=MultiStickSSD()
        x=dis(1)
        y=dis(2)
        KP=500
        KI=10
        KD=10
        sinx=(x-ox)/math.sqrt((x-ox)*(x-ox)+(y-oy)*(y-oy))
        cosx=(x-ox)/math.sqrt((x-ox)*(x-ox)+(y-oy)*(y-oy))
        self.diffold=self.diffnew
        self.diffnew=cosx
        self.integrald+=sinx
        p=KP*self.diffnew
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

right= Motor_move(0,20000)
left= Motor_move(1,20000)
while True:
    tmpl=ms.Multistick()
    if tmpl[0]!=0:
        right.Angle(tmpl[0],tmpl[1])
        left.Angle(tmpl[0],tmpl[1])
