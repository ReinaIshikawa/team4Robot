import threading
import time
import ex
import servo
import Motor_contorol

import Camera

def e():
    while True:
        ex.main()
def s():
    servo
def mc():
    Motor_contorol
def c():
    Camera.get_image()
if __name__=="__main__":
    
        command=input()
        if command=='a':
            th1=threading.Thread(target=e,name="th1",args=())
            th1.start()
        
        elif command=='b':
            th2=threading.Thread(target=s,name="th2",args=())
            th2.start()

        elif command=='c':
            th3=threading.Thread(target=mc,name="th3",args=())
            th3.start()
            
        elif command=='d':    
            th4=threading.Thread(target=c,name="th4",args=())
            th4.start()
        
        elif command=='d':
            exit()
