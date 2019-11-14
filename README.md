# team4Robot
##ディレクトリ構成
|フォルダ		|用途     |
|:----------|:--------|
|Camera		|OpneCV, Movidius画像認識を行う|
|Julius		|作成した辞書を元に音声認識を行う|
|Motor		|メインモーター及びサーボモーターの制御を行う|
|Sensor		|測距センサーを用いて距離を記録・出力する|

##実行方法
### - テスト実行
$python3 Core.py test
⇨スレッドが立ち上がる(全部同時に実行される)
- motor_demo.py
- servo.py
- Camera.py
- dist.py　


### - アプリケーション実行
$python3 Core.py 
⇨ 音声認識スレッド voice_thread.py の実行
  + 辞書 requestのmoduleキーの値に応じてfunctionが呼び出され，そこからスレッドを立ち上げていく
- motor_thread.py
- servo_thread.py
- camera_thread.py
- dist_thread.py

##Core.py
* コマンドラインでtest引数を渡した時，SubProcessで単純にスレッドを立ち上げる
* テスト引数を渡さなかったら，まずはjuliusの実行ファイル(シェルファイル)が実行され,
voice_thread.pyが実行.

音声認識やアプリケーションに応じて，requestの'module'や'cmd'の値を書き換え，他のスレッドとやりとりする
(popen.stdin.writeの方がいいかもしれない)
