import wiringpi as wp
import time
import struct
#import Motor
import Motor_move as Mmove

def test():
    speed = 2000

    print("***** start spi test program *****")

    right= Mmove.Motor_move(0,speed)
    left= Mmove.Motor_move(1,speed)

    while True:
        #speed = speed + 2000 # 30000 位まで
        right.Run_forward()
        left.Run_forward()
        time.sleep(5)
        right.Softstop()
        left.Softstop()
        right.Softhiz()
        left.Softthiz()
        quit()
    quit()

test()