import wiringpi as wp
import time
import struct
import Motor.py

if __name__=="__main__":
    #speed = 0
    speed = 0

    print("***** start spi test program *****")

    write=Motor(0)
    left=Motor(1)

    while True:
        for i in range(0, 10):
            #speed = speed + 2000 # 30000 位まで
            #print("hoge")
            # L6470_run(speed)
            write.Run_forward(speed)
            left.Run_forward(speed)
            #print("*** Speed %d ***" % speed)
            time.sleep(1)
        for j in range(0, 10):
            #speed = speed + 2000 # 30000 位まで
            #print("hoge")
            # L6470_run(speed)
            write.Run_back(speed)
            left.Run_back(speed)
            #print("*** Speed %d ***" % speed)
            time.sleep(1)
        for k in range(0, 10):
            #speed = speed + 2000 # 30000 位まで
            #print("hoge")
            # L6470_run(speed)
            write.Turn_write(speed)
            left.Turn_write(speed)
            #print("*** Speed %d ***" % speed)
            time.sleep(1)
        for l in range(0, 10):
            #speed = speed + 2000 # 30000 位まで
            #print("hoge")
            # L6470_run(speed)
            write.Turn_left(speed)
            write.Turn_left(speed)
            #print("*** Speed %d ***" % speed)
            time.sleep(1)
        

        write_Softstop()
        left.Softstop()
        write_Softhiz()
        left.Softthiz()
        quit()
    quit()
