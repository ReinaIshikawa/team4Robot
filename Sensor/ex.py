import pigpio
import time

def srf02_read(pi,h):
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
   print(high)
   print(low)
 #  pi.i2c_close(h)
   return dist

def main():
   pi=pigpio.pi()
   t1=time.time()
   h=pi.i2c_open(1,0x70)
   while True:
      print("a")
    #  h=pi.i2c_open(1,0x70)
      print(srf02_read(pi,h))
      t=int(input())
      if t!=1:
         pi.i2c_close(h)
         h=pi.i2c_open(1,0x70)
      else:
         pi.i2c_close(h)
      time.sleep(0.5)
      t2=time.time()
      if t2-t1>=60:
        break

main()
