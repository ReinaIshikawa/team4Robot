from pigpio import pi
x_pi = pi("192.168.0.51")

if not x_pi.connected:
    print('Unable to connect to RPi')
else:
    h = x_pi.i2c_open(1,0x70)
    x_pi.i2c_close(h)
    print(h)
    if h > 30:
        x = h - 1
        while x >= 0:
            x_pi.i2c_close(x)
            x = x - 1
        print(str(h) + ' pigpio handles closed')
    x_pi.stop()
