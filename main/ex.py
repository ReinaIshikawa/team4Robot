import pigpio
import time

def srf02_read(pi,h):
     # レジスタ 0x02, 0x03 の値を読み取る
   high = pi.i2c_read_word_data(h,0x02)
   low = pi.i2c_read_word_data(h,0x03)
  # print(high, low)

   low_low=int(bin(low&0b1111111),2)  # lowの下位7bitを抜き出して10進に変換 
                                      # 0-128cmの値が入る．
   low_high=int(bin(low>>15),2)  # lowを15bit右にシフトして10進に変換
                                 # 128-255cmの時に0b1になる
   high_low=int(bin(high&0b11),2)  # highの下位2bitを抜き出す
                         # 256cm:0b01, 512cm:0b10
   dist =high_low*255+low_high*128+low_low
   return dist


def srf02_mesure(pi, h):
   pi.i2c_write_device(h,[0x00,0x51])


def main():
   pi=pigpio.pi()
   t1=time.time()
   h=pi.i2c_open(1,0x70)
   srf02_mesure(pi, h)
   dist=srf02_read(pi, h)
   pi.i2c_close(h)
   print(dist)
   return dist
"""
while True:
      t=int(input())
      if
         srf02_mesure(pi, h) t!=0:
         srf02_read(pi, h)
         time.sleep(0.5)
      else:
         print("closing")
         pi.i2c_close(h)
         return 0
      t2=time.time()
      if t2-t1>=60:
         break

main()
"""
main()
