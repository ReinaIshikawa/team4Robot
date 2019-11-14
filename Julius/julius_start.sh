#!/bin/sh

julius -C ~/work/julius/dictation-kit-v4.4/word.jconf -module > /dev/null &
echo $! #プロセスIDを出力
sleep 60
