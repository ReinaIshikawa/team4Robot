# main file

import subprocess
import time
import json
import sys
from library import log


log.communication('Start')
argv = sys.argv
if len(argv) > 1:
    is_test = argv[1] == 'test'
    from Sensor.dist_stub import SensorStub as SensorThread
    from Motor.motor_stub import MotorStub as MotorThread
    # from  Julius.voice_thread import VoiceThread as VoiceThread
    # from Camera.MultiThread import MultiThread as MultiThread
    # from Camera.camera_thread import CameraThread as CameraThread
    print('Runing in test mode')
else:
    is_test = False
    from Sensor.dist_thread import DistThread as SensorThread
    from Motor.motor_thread import MotorThread
    from Julius.voice_thread import VoiceThread as VoiceThread
    from Camera.MultiThread import MultiThread as MultiThread
    from Camera.camera_thread import CameraThread as CameraThread
proc = {}

# open app prpcess
nullFile = open('/dev/null', 'w')
print("1")
proc['app'] = subprocess.Popen(
    #['python3', '-u', './app/dist_motor_app.py'],
    #['python3', '-u', './app/voice_cmd_app.py'],
    #['python3', '-u', './app/Pursuit.py'],
    #['python3', '-u', './app/music_app.py'],
    ['python3', '-u', './app/voice_motor_app.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    # encoding='utf8'
)

def changeApp():
    print("changeApp")


# quit to change apps
def exitCore():  # voice_threadで使用
    app = proc.pop('app')
    for process in proc.values():
        process.terminate()
    app.terminate()
    sys.exit()


# voice
if not is_test:
    proc['voice'] = subprocess.Popen(
        #["./Julius/julius_start.sh"],
        ['julius', '-C', '~/work/julius/dictation-kit-v4.4/word.jconf', '-module'],
        stdout = subprocess.PIPE,
        stdin = subprocess.PIPE,
        shell=True
    )
    
# Camera
if is_test:
    camera_cmd = ['python3', '-u', './Camera/camera_proc.py']
else:
    camera_cmd = ['python3', '-u', './Camera/Camera.py']
    proc['camera'] = subprocess.Popen(
        camera_cmd,
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE
    )

# log.communication('app: {}, camera: {}'.format(proc['app'], proc['camera']))

# Main Motor
if is_test:
    # stub
    motor = ['python3', '-u', './Motor/motor_stub.py']
else:
    motor = ['python3', '-u', './Motor/motor_thread.py']
"""
proc['motor'] = subprocess.Popen(
    motor,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    # encoding='utf8'
)
"""

# Servo Motor
# if is_test:#自動でくるくる動く
# 	servo_cmd = ['python3', '-u', './Motor/servo.py']
# else:#指示を受けて動く
# 	servo_cmd = ['python3', '-u', './Motor/servo_thread.py']
# proc['servo'] = subprocess.Popen(
# 	servo_cmd,
# 	stdin = subprocess.PIPE,
# 	stdout = subprocess.PIPE
# )

# Distance Sensor
if is_test:
    # return rundom distance
    sensor = ['python3', '-u', './Sensor/dist_stub.py']
else:
    sensor = ['python3', '-u', './Sensor/dist_thread.py']
"""
proc['sensor'] = subprocess.Popen(
    sensor,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    # encoding='utf8'
)
"""
time.sleep(5)
# ---- END process initialization ----


# ---- BEGIN request handler definition ----

threads = {}
threads['sensor'] = SensorThread(proc['app'])
threads['motor'] = MotorThread(proc['app'])
threads['voice'] = VoiceThread(proc['app'], proc['voice'], exitCore)
threads['camera'] = CameraThread(proc['app'], proc['camera'], log)
# Initialize
__result = [t.start() for t in threads.values()]
print(__result)


def func_voice(request):
    threads['voice'].run(request=request)

    
def func_camera(request):
    threads['camera'].run(request=request)

    
def func_motor(request):
    threads['motor'].run(request=request)


def func_sensor(request):
    threads['sensor'].run(request=request)

# ---- END request handler definition ----

# ---- read app orders ----
cnt = 0
log.communication('Init complete')
while True:
    log.communication('While')
    proc['app'].stdout.flush()
    log.communication('pre req:')
    raw_request = proc['app'].stdout.readline().decode("utf-8")
    try:
        request = json.loads(raw_request)
        log.communication('[{}] REQUEST:{}'.format(cnt, request))
        cnt += 1
    except ValueError:
        log.communication('[{}] VALUE ERROR')
        continue

    print("5")

    if request['module'] == 'camera':
        func_camera(request)
    elif request['module'] == 'voice':
        func_voice(request)
    elif request['module'] == 'motor':
        func_motor(request)
    elif request['module'] == 'sensor':
        func_sensor(request)
    elif request['module'] == 'quit':
        # TODO: call destructor
        time.sleep(3)
        exitCore()
