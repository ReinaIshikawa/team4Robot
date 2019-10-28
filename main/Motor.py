#!/usr/bin/env python
# -*- coding: utf-8 -*-
#コンストラクタでspeedとspi_idを指定

import wiringpi as wp
import time
import struct
class Motor():
    
    def Write(self,data, spi_id):
        data = struct.pack("B", data)
        print("b1")
        print(data)
        wp.wiringPiSPIDataRW(spi_id, data)
        print("b2")
    

    def __init__(self,spi_id,spd):
        self.diff=[0 for _ in range (2)]
        self.angl=0
        self.integrald=0
        self.integrala=0
        self.delta=0.001 #時間差
        self.speed=spd
        self.id=spi_id
        L6470_SPI_SPEED     = 1000000
        print("***** start spi test program *****")
        if  (wp.wiringPiSPISetup(spi_id, L6470_SPI_SPEED)<0):
            print('spi'+spi_id+ 'setup failed')
        # MAX_SPEED設定。
        # レジスタアドレス。
        self.Write(0x07, spi_id)
        # 最大回転スピード値(10bit) 初期値は 0x41
        self.Write(0x00, spi_id)
        self.Write(0x25, spi_id)
        # KVAL_HOLD設定。
        # レジスタアドレス。
        self.Write(0x09, spi_id)
        # モータ停止中の電圧設定(8bit)
        self.Write(0xFF, spi_id)

        # KVAL_RUN設定。
        # レジスタアドレス。
        self.Write(0x0A, spi_id)
        # モータ定速回転中の電圧設定(8bit)
        self.Write(0xFF, spi_id)

        # KVAL_ACC設定。
        # レジスタアドレス。
        self.Write(0x0B, spi_id)
        # モータ加速中の電圧設定(8bit)
        self.Write(0xFF, spi_id)

        # KVAL_DEC設定。
        # レジスタアドレス。
        self.Write(0x0C, spi_id)
        # モータ減速中の電圧設定(8bit) 初期値は 0x8A
        self.Write(0x40, spi_id)
        
        # OCD_TH設定。
        # レジスタアドレス。
        self.Write(0x13, spi_id)
        # オーバーカレントスレッショルド設定(4bit)
        self.Write(0x0F, spi_id)
        # STALL_TH設定。
        # レジスタアドレス。
        self.Write(0x14, spi_id)
        
        # ストール電流スレッショルド設定(4bit)
        self.Write(0x7F, spi_id)
        
    #start slopeデフォルト
        #   /// レジスタアドレス。
        self.Write(0x0e, spi_id)
        self.Write(0x00, spi_id)
        self.Write(0x10, spi_id)
        self.Write(0x29, spi_id)
        

    def Run_setting(self,tmpspd,spi_id):
        #print('runboth {}'.format(tmpspd))
        # 方向検出。
        if (tmpspd < 0):
            dir = 0x50
            setspd = -1 * tmpspd
        else:
            dir = 0x51
            setspd = tmpspd

        # 送信バイトデータ生成。
        spd_h   =  (0x0F0000 & setspd) >> 16
        spd_m   =  (0x00FF00 & setspd) >> 8
        spd_l   =  (0x00FF & setspd)

        # コマンド（レジスタアドレス）送信。
        self.Write(dir, spi_id)
        # データ送信。
        self.Write(spd_h, spi_id)
        self.Write(spd_m, spi_id)
        self.Write(spd_l, spi_id)

    def Run_forward(self):
        print('runboth {}'.format(self.speed))
        if self.id==0:
            self.Run_setting(self.speed,0)
        else:
            tmpspd=(-1)*self.speed
            self.Run_setting(tmpspd, 1)

    def Run_back(self):
        print('runboth {}'.format(self.speed))
        if self.id==0:
            tmpspd=(-1)*self.speed
            self.Run_setting(tmpspd, 0)
        else:
            self.Run_setting(self.speed, 1)

    def Turn_right(self):
        print('runboth {}'.format(self.speed))
        if self.id==0:
            self.Run_setting(self.speed, 0)
        else:
            self.Run_setting(0, 1)    

    def Turn_left(self):
        print('runboth {}'.format(self.speed))
        if self.id==0:
            self.Run_setting(0, 0)
        else:
            tmpspd=(-1)*self.speed
            self.Run_setting(tmpspd, 1)

    def Softstop(self):
        print("***** SoftStop. *****")
        dir = 0xB0
        # コマンド（レジスタアドレス）送信。
        self.Write(dir, spi_id)
        time.sleep(1)

    def Softhiz(self):
        print("***** Softhiz. *****")
        dir = 0xA8
        # コマンド（レジスタアドレス）送信。
        self.Write(dir, spi_id)
        time.sleep(1)
    