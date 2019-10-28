import wiringpi as wp
import time
import struct
import Motor
import Motor_move as Mmove

if __name__=="__main__":
    speed = 2000

    print("***** start spi test program *****")

    right= Mmove.Motor_move(0,speed)
    left= Mmove.Motor_move(1,speed)

    while True:
        for i in range(10):
            #speed = speed + 2000 # 30000 位まで
            right.PID()
            left.PID()
            time.sleep(1)
        right.Softstop()
        left.Softstop()
        right.Softhiz()
        left.Softthiz()
        quit()
    quit()
