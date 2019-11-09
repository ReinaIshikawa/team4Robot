import threading
import time
import ex
import servo
import Motor_contorol
global command
import Camera

def e():
    while True:
        ex.main()
def s():
    servo.main()
def mc():
    Motor_contorol
def c():
    Camera.get_image()
def command(co):
    while True:
        co[0]=input()
        
if __name__=="__main__":
    #th=threading.Thread(target=command,name="th",args=(command,))
  #  th.start()
    while True:
        
        command=input()
        if command=='srf02':
            th1=threading.Thread(target=e,name="th1",args=())
            th1.start()
        
        elif command=='servo':
            th2=threading.Thread(target=s,name="th2",args=())
            th2.start()

        elif command=='motor_control':
            th3=threading.Thread(target=mc,name="th3",args=())
            th3.start()
            
        elif command=='camera':    
            th4=threading.Thread(target=c,name="th4",args=())
            th4.start()
        
        elif command=='e':
            threading.Event().set()
            break
    print("a")
