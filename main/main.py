import threading
import ex
import servo
import Motor_contorol
import Camera

def Ex():
    ex.main()
def Servo():
    servo
def motor_control():
    Motor_contorol
def camera():
    Camera.get_image()

if __name__=="__main__":

    while True:
        command=input()
        if command=="a":
            th1=threading.Thread(target=Ex,name="th1",args=())
            th1.start()
        
        if command=="b":
            th2=threading.Thread(target=Servo,name="th2",args=())
            th2.start()

        if command=="c":
            th3=threading.Thread(target=motor_control,name="th3",args=())
            th3.start()
            
        if command=="d":    
            th4=threading.Thread(target=camera,name="th4",args=())
            th4.start()
        
        if command=="e":
            exit()