# Subprocessの実行ファイル

import subprocess
import time
import json
import sys
from library import log
# from Sensor import dist_stub
# from Camera import camera_thread
# from Motor import motor_thread
# from Motor import servo_thread
# from Julius import voice_thread
# from Sensor import dist_thread


argv = sys.argv
if len(argv) > 1:
    is_test = argv[1] == 'test'
    from Sensor.dist_stub import SensorStub as SensorThread
    from Motor.motor_stub import MotorStub as MotorThread
    from  Voice.voice_thread import VoiceThread as VoiceThread
    print('Runing in test mode')
else:
    is_test = False
    from Sensor.dist_thread import DistThread as SensorThread
    from Motor.motor_thread import MotorThread
    from  Voice.voice_thread import VoiceThread as VoiceThread

proc = {}

# request = {
# 	'module':'sensor',
# 	'cmd':'check_dist'
# }
# #json.dumpsはpipeにstdin.writeしているのと同じこと．
# print (json.dumps(request))


# アプリの実行と終了
nullFile = open('/dev/null', 'w')

proc['app'] = subprocess.Popen(
    #['python3', '-u', './app/dist_motor_app.py'],
    ['python3', '-u', './app/voice_cmd_app.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    # encoding='utf8'
)

def changeApp():
    print("changeApp")


def exitCore():  # voice_threadで使用
    app = proc.pop('app')
    for process in proc.values():
        process.terminate()
    app.terminate()
    sys.exit()

if not is_test:
    # proc['julius'] = subprocess.Popen(
    # 	['~/work/julius/julius-4.4.2/julius/julius', '-C', '~/work/julius-4.4.2/julius-kit/dictation-kit-v4.4.2-linux/word.jconf', '-module'],
    # 	stdout=nullFile
    # )

    proc['voice'] = subprocess.Popen(
    	["./Julius/julius_start.sh"],
    	stdout=subprocess.PIPE,
    	shell=True
    )

# #Camera
# if is_test:#単純にカメラを立ち上げる
# 	camera_cmd = ['python3', '-u', './Camera/Camera.py']
# else:#カメラで画像認識をしたりする
# 	camera_cmd = ['python3', '-u', './Camera/camera_thread.py']#とりあえず一緒
# proc['camera'] = subprocess.Popen(
# 	camera_cmd,
# 	stdin = subprocess.PIPE,
# 	stdout = subprocess.PIPE
# )


# Main Motor
if is_test:
    # 自動で前後左右動く
    motor = ['python3', '-u', './Motor/motor_stub.py']
else:
    # 音声入力に応じて実行させたりする
    motor = ['python3', '-u', './Motor/motor_thread.py']
"""
proc['motor'] = subprocess.Popen(
    motor,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    # encoding='utf8'
)
"""

# #Servo Motor
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
    # 自動で距離を測って出力
    sensor = ['python3', '-u', './Sensor/dist_stub.py']
else:
    # motorとかと連動
    sensor = ['python3', '-u', './Sensor/dist_thread.py']
"""
proc['sensor'] = subprocess.Popen(
    sensor,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    # encoding='utf8'
)
"""
# ---- END thread initialization ----


# ---- BEGIN request handler definition ----

threads = {}
threads['sensor'] = SensorThread(proc['app'])
threads['motor'] = MotorThread(proc['app'])
threads['voice'] = VoiceThread(proc['app'], exitCore)

# Initialize
__result = [t.start() for t in threads.values()]
print(__result)


def func_voice(request):
    threads['voice'].run(request=request)

# def func_camera(request):
# 	threads['camera'] = camera_thread.CameraThread(
# 		request,
# 		proc['camera']
# 	)
# 	threads['camera'].start()


def func_motor(request):
    threads['motor'].run(request=request)


def func_sensor(request):
    threads['sensor'].run(request=request)


# ---- END request handler definition ----
# アプリケーション作成時に，proc[app]に書き込まれたものを読み込んで実行
cnt = 0
while True:
    proc['app'].stdout.flush()
    raw_request = proc['app'].stdout.readline().decode("utf-8")
    try:
        request = json.loads(raw_request)
        print('[{}] REQUEST:{}'.format(cnt, request))
        cnt += 1
    except ValueError:
        print('[{}] VALUE ERROR')
        continue

    # センサーから毎秒距離を取得する
    # 音声からは毎秒コマンドを
    # →Motorに送る

    # センサーからは数字のみを渡す
    # sensor_rep = json.loads(proc['sensor'].stdout.readline())
    # request['dist'] = sensor_rep['dist']
    # voiceからはいろんなコマンドが送られる
    # →requestと同じ辞書形式で(コピーを渡してそこに書き込み,)jsonに書き込み
    # voice_rep = json.loads(proc['voice'].stdout.readline())
    # request['motor_cmd'] = voice_rep['motor_cmd']
    # motorに送る
    # proc['motor'].stdout.write(json.dumps(request))

    if request['module'] == 'camera':
        continue
        # func_camera(request)
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
