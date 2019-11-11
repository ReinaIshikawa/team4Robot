import wiringpi as wp
import time
import struct
from Motor import Motor
from Motor_move import Motor_move
#import ex

if __name__=="__main__":
    speed = 2000

    print("***** start demo program *****")

    right=Motor_move(0,speed)
    left=Motor_move(1,speed)

    while True:
        for k in range(4):
            if k==0:
                for i in range(10):
                    right.Run_forward()
                    left.Run_forward()
                    time.sleep(1)
            elif k==1:
                for i in range(10):
                    right.Turn_right()
                    left.Turn_right()
                    time.sleep(1)
            elif k==2:
                for i in range(10):
                    right.Turn_left()
                    left.Turn_left()
                    time.sleep(1)
            else:
                for i in range(10):
                    right.Run_back()
                    left.Run_back()
                    time.sleep(1)
            time.sleep(1)
        self.Softstop()
        self.Softthiz()