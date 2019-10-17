import wiringpi as wp
import time
import struct
from Motor import Motor

if __name__=="__main__":
    speed = 0

    print("***** start spi test program *****")

    right=Motor(0)
    left=Motor(1)

    while True:
        for i in range(0, 10):
            #speed = speed + 2000 # 30000 位まで
            right.Run_forward(speed)
            left.Run_forward(speed)
            time.sleep(1)
        for j in range(0, 10):
            #speed = speed + 2000 # 30000 位まで
            right.Run_back(speed)
            left.Run_back(speed)
            time.sleep(1)
        for k in range(0, 10):
            #speed = speed + 2000 # 30000 位まで
            right.Turn_right(speed)
            left.Turn_right(speed)
            time.sleep(1)
        for l in range(0, 10):
            #speed = speed + 2000 # 30000 位まで
            right.Turn_left(speed)
            right.Turn_left(speed)
            time.sleep(1)
        right_Softstop()
        left.Softstop()
        right_Softhiz()
        left.Softthiz()
        quit()
    quit()
