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
   pi1=pigpio.pi()
   t1=time.time()
   h1=pi1.i2c_open(1,0x71)
   srf02_mesure(pi1, h1)
   time.sleep(0.4)
   dist1=srf02_read(pi1, h1)
   pi1.i2c_close(h1)

   pi2=pigpio.pi()
   h2=pi2.i2c_open(1,0x73)
   srf02_mesure(pi2, h2)

   time.sleep(0.4)
   dist2=srf02_read(pi2, h2)
   pi2.i2c_close(h2)

   if abs(dist2-dist1)<30:
      return dist1

   else:
      return 0

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
