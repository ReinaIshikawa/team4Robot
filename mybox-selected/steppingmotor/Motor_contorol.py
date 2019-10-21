import wiringpi as wp
import time
import struct
from Motor import Motor
import ex

if __name__=="__main__":
    speed = 0

    print("***** start spi test program *****")

    right=Motor_move(0,speed)
    left=Motor_move(1,speed)

    while True:
        for i in range 10:
            #speed = speed + 2000 # 30000 位まで
            right.motormove()
            left.motormove()
            time.sleep(1)
        right_Softstop()
        left.Softstop()
        right_Softhiz()
        left.Softthiz()
        quit()
    quit()
