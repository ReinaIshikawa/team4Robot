import subprocess
import time
import json
import sys
#import camera_thread
#import distant_thread
#import voice_thread
#import shoe_thread
#import log
import Camera
import Motor_contorol
import ex
import servo

argv = sys.argv

if len(argv) > 1:
    is_test = argv[1] == 'test'

else:
    is_test = False

proc = {}
 
#proc['app'] = subprocess.Popen(['python3', '-u', './'],stdin = subprocess.PIPE,stdout = subprocess.PIPE)

nullFile = open('/dev/null', 'w')

"""
def changeApp(app):
    proc['app'] = subprocess.Popen(['python3', '-u', './' + app],stdin = subprocess.PIPE,stdout = subprocess.PIPE)

    for thread in threads.values():
        thread.changeApp(proc['app'])

    return proc['app']

#?
def exitCore():
    app = proc.pop('app')
    for process in proc.values():
        process.terminate()

    app.terminate()
    sys.exit()
"""

"""
if not is_test:
    proc['julius'] = subprocess.Popen(['../dvd/julius/julius-4.2.3/julius/julius', '-C', 'voice/rapiro.jconf', '-module'],stdout=nullFile)
"""
time.sleep(3)

camera_cmd = ['python3', '-u', './Camera.py']
proc['camera'] = subprocess.Popen(camera_cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE)

"""
voice_cmd = ['python', '-u', './voice/connection.py']
proc['voice'] = subprocess.Popen(voice_cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE)
"""

motor_cmd = ['python3','-u','./Motor_contorol.py']
proc['motor'] = subprocess.Popen(motor_cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE)

ex_cmd = ['python3','-u','./ex.py']
proc['ex'] = subprocess.Popen(ex_cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE)


servo_cmd = ['python', '-u', './servo.py']
proc['servo'] = subprocess.Popen(servo_cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE)

threads = {}

def func_camera(request):
    threads['camera'] = Camera.get_image()

"""
def func_voice():
    thread = voice_thread.VoiceThread(log,proc['app'],proc['voice'],changeApp,exitCore)

    thread.start()
"""
#?
def func_servo(request):
    threads['servo'] = servo.main()

"""
def func_motor(request):
    cmd = request['command']
    if cmd == 'stop':
        log.communication('motor: send ' + cmd)
        proc['motor'].stdin.write(cmd + '\n')

    elif cmd == 'move' or cmd == 'back':
        right_speed = request['left_speed']
        left_speed = request['right_speed']
        right = str(right_speed)
        left = str(left_speed)
        log.communication('motor: send ' + cmd + ' ' + right + ' ' + left)
        proc['motor'].stdin.write('move_spd ' + right + ' ' + left + '\n')

    elif cmd == 'right' or cmd == 'left':
        angle = request['angle']
        log.communication('motor: send ' + cmd + ' ' + str(angle))
        proc['motor'].stdin.write(cmd + ' ' + str(angle) + '\n')

    elif cmd == 'move_acc':
        dst = request['dst']
        log.communication('motor: send ' + cmd + ' ' + str(dst))
        proc['motor'].stdin.write('move ' + str(dst) + ' ' + str(dst) + '\n')
"""

def func_motor(request):
    threads['motor']

def func_ex(request):
    threads['ex'] = ex.main()


func_ex()
func_camera()


#?
while True:
    #get module and command from app
    raw_request = proc['app'].stdout.readline()
    try:
        request = json.loads(raw_request)

    except ValueError:
        continue

    log.communication('app: receive ' + raw_request)

    if request['module'] == 'camera':
        func_camera(request)

    elif request['module'] == 'motor':
        func_motor(request)

    elif request['module'] == 'ex':
        func_ex(request)

    elif request['module'] == 'servo':
        func_servo(request)
