#!/bin/sh

julius -C ~/work/julius-4.4.2/julius-kit/dictation-kit-v4.3.1-linux/word.jconf -module > /dev/null &
echo $! #プロセスIDを出力
sleep 2 #2秒間スリープ