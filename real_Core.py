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
    from Motor.servo_stub import ServoStub as ServoThread
    from Camera.camera_stub import CameraStub as CameraThread
    from  Julius.voice_stub import VoiceStub as VoiceThread
    print('-------- Runing in test mode --------')
else:
    is_test = False
    from Sensor.dist_thread import DistThread as SensorThread
    from Motor.motor_thread import MotorThread
    from Motor.servo_thread import ServoThread as ServoThread
    from Julius.voice_thread import VoiceThread as VoiceThread
    from Camera.camera_thread import CameraThread as CameraThread
proc = {}

# open app prpcess
nullFile = open('/dev/null', 'w')
print("1")
proc['app'] = subprocess.Popen(
    ['python3', '-u', './app/dist_motor_app.py'],
    #['python3', '-u', './app/voice_cmd_app.py'],
    #['python3', '-u', './app/Pursuit.py'],
    # ['python3', '-u', './app/music_app.py'],
    #['python3', '-u', './app/voice_motor_app.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    # encoding='utf8'
)

def changeApp():
    print("changeApp")


# quit to change apps
def exitCore():  # voice_thread
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
    # empty file
    camera_cmd = ['python3', '-u', './Camera/Camera_empty.py']
else:
    camera_cmd = ['python3', '-u', './Camera/Camera.py']
    proc['camera'] = subprocess.Popen(
        camera_cmd,
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE
    )


time.sleep(5)
# ---- END process initialization ----


# ---- BEGIN request handler definition ----

threads = {}
threads['voice'] = VoiceThread(proc['app'], proc['voice'], exitCore)
threads['camera'] = CameraThread(proc['app'], proc['camera'], log)
threads['motor'] = MotorThread(proc['app'])
threads['servo'] = ServoThread(proc['app'])
threads['sensor'] = SensorThread(proc['app'])


# Initialize
__result = [t.start() for t in threads.values()]
print(__result)


def func_voice(request):
    threads['voice'].run(request=request)


def func_camera(request):
    threads['camera'].run(request=request)


def func_motor(request):
    threads['motor'].run(request=request)


def func_servo(request):
    threads['servo'].run(request=request)


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
    elif request['servo'] == 'servo':
        func_servo(request)
    elif request['module'] == 'sensor':
        func_sensor(request)
    elif request['module'] == 'quit':
        # TODO: call destructor
        time.sleep(3)
        exitCore()
