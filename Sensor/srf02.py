import pigpio
h=pi.i2c_open(BUS,SRF02_I2C_ADOR)

def srf02_read(h):
     # レジスタ 0x02, 0x03 の値を読み取る
   high = pi.i2c_read_word_data(h,0x02)
   low = pi.i2c_read_word_data(h,0x03)

   low_low=int(bin(low&0b1111111),2)  # lowの下位7bitを抜き出して10進に変換 
                                      # 0-128cmの値が入る．
   low_high=int(bin(low>>15),2)  # lowを15bit右にシフトして10進に変換
                                 # 128-255cmの時に0b1になる
   high_low=int(bin(high&0b11),2)  # highの下位2bitを抜き出す
                                   # 256cm:0b01, 512cm:0b10
   dist =high_low*255+low_high*128+low_low
   return dist