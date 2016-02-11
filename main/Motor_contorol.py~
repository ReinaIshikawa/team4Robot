import wiringpi as wp
import time
import struct
import Motor
import Motor_move as Mmove

if __name__=="__main__":
    speed = 0

    print("***** start spi test program *****")

    right= Mmove.Motor_move(0,speed)
    left= Mmove.Motor_move(1,speed)

    while True:
        for i in range(10):
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
