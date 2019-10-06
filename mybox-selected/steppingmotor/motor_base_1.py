#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wiringpi as wp
import time
import struct

L6470_SPI_SPEED     = 1000000

def L6470_write(data, spi_id):
    data = struct.pack("B", data)
    print("b1")
    print(data)
    wp.wiringPiSPIDataRW(spi_id, data)
    print("b2")

def L6470_init(spi_id):
    # MAX_SPEED設定。
    # レジスタアドレス。
    L6470_write(0x07, spi_id)
    # 最大回転スピード値(10bit) 初期値は 0x41
    L6470_write(0x00, spi_id)
    L6470_write(0x25, spi_id)
    # KVAL_HOLD設定。
    # レジスタアドレス。
    L6470_write(0x09, spi_id)
    # モータ停止中の電圧設定(8bit)
    L6470_write(0xFF, spi_id)

    # KVAL_RUN設定。
    # レジスタアドレス。
    L6470_write(0x0A, spi_id)
    # モータ定速回転中の電圧設定(8bit)
    L6470_write(0xFF, spi_id)

    # KVAL_ACC設定。
    # レジスタアドレス。
    L6470_write(0x0B, spi_id)
    # モータ加速中の電圧設定(8bit)
    L6470_write(0xFF, spi_id)

    # KVAL_DEC設定。
    # レジスタアドレス。
    L6470_write(0x0C, spi_id)
    # モータ減速中の電圧設定(8bit) 初期値は 0x8A
    L6470_write(0x40, spi_id)
     
    # OCD_TH設定。
    # レジスタアドレス。
    L6470_write(0x13, spi_id)
    # オーバーカレントスレッショルド設定(4bit)
    L6470_write(0x0F, spi_id)
    # STALL_TH設定。
    # レジスタアドレス。
    L6470_write(0x14, spi_id)
    
    # ストール電流スレッショルド設定(4bit)
    L6470_write(0x7F, spi_id)
    
#start slopeデフォルト
     #   /// レジスタアドレス。
    L6470_write(0x0e, spi_id)
    L6470_write(0x00, spi_id)
    L6470_write(0x10, spi_id)
    L6470_write(0x29, spi_id)
    

def L6470_run(speed, spi_id):
    print('runboth {}'.format(speed))
    # 方向検出。
    if (speed < 0):
        dir = 0x50
        spd = -1 * speed
    else:
        dir = 0x51
        spd = speed

    # 送信バイトデータ生成。
    spd_h   =  (0x0F0000 & spd) >> 16
    spd_m   =  (0x00FF00 & spd) >> 8
    spd_l   =  (0x00FF & spd)

    # コマンド（レジスタアドレス）送信。
    L6470_write(dir, spi_id)
    # データ送信。
    L6470_write(spd_h, spi_id)
    L6470_write(spd_m, spi_id)
    L6470_write(spd_l, spi_id)

def L6470_run_both(speed):
    print('runboth {}'.format(speed))
    L6470_run(speed, 0)
    L6470_run(-1*speed, 1)
    
def L6470_softstop():
    print("***** SoftStop. *****")
    dir = 0xB0
    # コマンド（レジスタアドレス）送信。
    L6470_write(dir, spi_id)
    time.sleep(1)

def L6470_softhiz():
    print("***** Softhiz. *****")
    dir = 0xA8
    # コマンド（レジスタアドレス）送信。
    L6470_write(dir, spi_id)
    time.sleep(1)

if __name__=="__main__":
    #speed = 0
    speed = 0

    print("***** start spi test program *****")

    # SPI channel 0 を 1MHz で開始。
    #wp.wiringPiSetupGpio()
    if  (wp.wiringPiSPISetup(0, L6470_SPI_SPEED)<0):
        print('spi 0 setup failed')
    if  (wp.wiringPiSPISetup(1, L6470_SPI_SPEED)<0):
        print('spi 1 setup failed')
    # L6470の初期化
    print("ge")
    L6470_init(0)
    L6470_init(1)

    while True:
        for i in range(0, 20):
            #speed = speed + 2000 # 30000 位まで
            print("hoge")
            # L6470_run(speed)
            L6470_run_both(speed)
            #print("*** Speed %d ***" % speed)
            time.sleep(1)

        L6470_softstop()
        L6470_softhiz()
        quit()
    quit()
