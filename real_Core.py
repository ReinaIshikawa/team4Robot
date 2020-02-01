# main file
import subprocess
import time
import json
import sys
from library import log


log.communication('Start')
argv = sys.argv
app_num = 0
if len(argv) > 1 and argv[1]=='test':
    is_test = True
    from Sensor.dist_stub import SensorStub as SensorThread
    from Motor.motor_stub import MotorStub as MotorThread
    from Motor.servo_stub import ServoStub as ServoThread
    from Camera.camera_stub import CameraStub as CameraThread
    from  Julius.voice_stub import VoiceStub as VoiceThread
    print('-------- Runing in test mode --------')
else:
    is_test = False
    app_num = int(argv[1])
    from Sensor.dist_thread import DistThread as SensorThread
    from Motor.motor_thread import MotorThread
    from Motor.servo_thread import ServoThread as ServoThread
    from Julius.voice_thread import VoiceThread as VoiceThread
    from Camera.camera_thread import CameraThread as CameraThread
proc = {}

if len(argv) > 2:
    app_num = int(argv[2])
    print("app_num", app_num)
app_cmd= [['python3', '-u', './app/dist_motor_app.py'],# 0
['python3', '-u', './app/voice_motor_app.py'],# 1
['python3', '-u', './app/Pursuit.py'],# 2
['python3', '-u', './app/music_app.py'],# 3
['python3', '-u', './app/attack.py'],#4
['python3', '-u', './app/application_yamada.py']]# 5

print("1")

# open app prpcess
def startApp():
    nullFile = open('/dev/null', 'w')
    proc['app'] = subprocess.Popen(
        app_cmd[app_num],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        # encoding='utf8'
    )

startApp()

def changeApp():
    global app_num
    app = proc.pop('app')
    for process in proc.values():
        process.terminate()
    app.terminate()
    app_num = app_num + 1
    if(app_num < len(app_cmd)):
        startApp()
        print("changeApp")


# quit to change apps
def exitCore():  # voice_thread
    app = proc.pop('app')
    for process in proc.values():
        process.terminate()
    app.terminate()
    sys.exit()


# voice
if is_test:
    voice_cmd = ['python3', '-u', './Julius/Voice_empty.py']
    proc['voice'] = subprocess.Popen(
        #["./Julius/julius_start.sh"],
        voice_cmd,
        stdout = subprocess.PIPE,
        stdin = subprocess.PIPE,
        # shell=True
    )
if not is_test:
    pass
    # voice_cmd = ['julius', '-C', '~/work/julius/dictation-kit-v4.4/word.jconf', '-input mic', '-module']
    # proc['voice'] = subprocess.Popen(voice_cmd)

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
threads['voice'] = VoiceThread(proc['app'], exitCore, changeApp)
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
    print("------------",request,"-----------")
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
    # log.communication('While')
    proc['app'].stdout.flush()
    # log.communication('pre req:')
    raw_request = proc['app'].stdout.readline().decode("utf-8")
    try:
        request = json.loads(raw_request)
        log.communication('[{}] REQUEST:{}'.format(cnt, request))
        cnt += 1
    except ValueError:
        # log.communication('[{}] VALUE ERROR')
        continue
    if request['module'] == 'camera':
        func_camera(request)
    elif request['module'] == 'voice':
        func_voice(request)
    elif request['module'] == 'motor':
        func_motor(request)
    elif request['module'] == 'servo':
        func_servo(request)
    elif request['module'] == 'sensor':
        func_sensor(request)
    elif request['module'] == 'quit':
        # TODO: call destructor
        time.sleep(2)
        exitCore()
