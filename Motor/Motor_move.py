#センサからの距離情報によって動きを決定する

import wiringpi as wp
import time
import struct
from .Motor import Motor
#import Motor
import math

class Motor_move(Motor):
    def __init__(self,spi_id,spd):
        super().__init__(spi_id,spd)
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
        spd=p+i+d
        if p+i+d>30000:
            # spd=-30000
            spd=30000
        elif p+i+d<-30000:
            # spd=30000
            spd=-30000
        if self.id == 1:
            spd = -spd

        self.Run_setting(spd,self.id)

        
    def Angle(self,x,y):
        ox=320
        oy=240
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
        if x<0:
            self.Softstop()
        elif x>200:
            spd=2000
            self.Run_setting(spd,self.id)
            time.sleep(1)
            self.Softstop()
        elif x<400:
            spd=-2000
            self.Run_setting(spd,self.id)
            time.sleep(1)
            self.Softstop()
        else:
            self.Softstop()
        time.sleep(1)
