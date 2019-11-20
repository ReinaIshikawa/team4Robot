import json
import threading

#全ての動作の上に君臨するスクリプト
#applicationから呼び出され，pipe.stdinを通してsubprocessに命令をだす

#requestを送ったsubprocess(module)それぞれに対するcallback関数のリスト
listeners = {
	'camera': [],
	'sensor': [],
	'voice': []
}

class CallbackThread(threading.Thread):
	def __init__(self, callback, response):
		super(CallbackThread, self).__init__()
		self.callback = callback
		self.response = response
	def run(self):
		self.callback(self.response)

def startListener(thread):
	thread.start()
	while True:
		#標準入力を読み込み続ける
		#subprpcessから何か返答があれば標準入力として帰ってくる
		#(input()もstdinと同じこと _stubファイルはinputで適当な値を入力するようにしている)
		data = json.loads(input())
		request = data['request']
		response = data['response']
		#実行したやつのmodule名
		module = request['module']
		#リスナーのkeyがmodule, valueはcallback
		if len(listeners[module]) > 0:
			thread = CallbackThread(listeners[module][0], response)
			thread.start()
			#各モジュールリストに入ったcallback関数をpopし実行していく
			listeners[module].pop(0)

#appのスレッドをstartしてrun() を実行すると呼ばれる関数たち
#subprocessに対してrequestを送る
#送ったらsubprocessで何らかの処理がされる
#subprocessからresponseが帰ってくるもの(sensor類. 測定値など)と，帰ってこないもの(motor類．動かすだけ)がある
#帰ってこないものはそのまま
#帰ってくるものは，responseに対してどんな応答をするのかを書いたcallback(関数)を引数として渡す
#Listenerでresponseを受け取り，callback関数を実行する仕組みになっている

#sensorに距離を返させる
def get_dist(callback):
	request = {
		'module':'sensor',
		'cmd':'check_dist'
	}
	#json.dumpsはpipeにstdin.writeしているのと同じこと．
	print json.dumps(request)
	#lisnersの'sensor'のリストにcallback関数(アプリケーションファイルに書かれている)を追加する
	listeners['sensor'].append(callback)

#main motorを動かす
#1. 障害物との距離を渡し，速度を変更させる(制御は向こう)
#コールバックなし
def motor_dist_check(dist, callback):
	request = {
		'module':'motor',
		'cmd':'check_dist',
		'dist':dist
	}
	print json.dumps(request)

#2. 座標を渡し，角度を変更させる
def motor_angle_check(x, y, callback):
	request = {
		'module':'motor',
		'cmd':'check_angle',
		'x': x,
		'y': y
	}
	print json.dumps(request)
	#callbacckはとりあえずなし

#3. コマンドとして前後左右を指定し愚直に移動させる
def motor_move(direction, callback):
	request = {
		'module':'motor',
		'cmd': 'move',
		'direction': direction
	}
	print json.dumps(request)
	#callbacckはとりあえずなし