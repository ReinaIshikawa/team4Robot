import fcntl
import smbus
import time
import "usr/incude/linux/i2c-dev"

def censor_function():
	buf = []
	try:
		path =  "/dev/i2c-1"
		with open (path, "wb") as fd1:
		with open (path, "wb") as fd2:

		if (fcntl.ioctl(fd1, I2C_SLAVE, (0xE0 >> 1)) < 0):
			raise IoctlErr("Error on slave address 0xE0\n")
		if (fcntl.ioctl(fd2, I2C_SLAVE, (0xE2 >> 1)) < 0):
			raise IoctlErr("Error on slave address 0xE2\n")

		i2c = smbus.SMBus(1)

		# 1 つめのセンサに対して
		# read from 0xE0
		# コマンドレジスタ0に 0x51:Real Ranging Mode - Result in centimeters を送ることによって測距が始まる

		buf[0] = 0x00
		buf[1] = 0x51

		if ((write_i2c_block_data(fd1, buf, 2)) != 2):
			raise Exception("0xE0 Error send the read command\n")
		time.sleep(0.066)




	except IOError:
		print ('"%s" cannot be opened.' % path)
	except OSError:
		print("Cannot excecute ioctl command")
	except IoctlErr as exc:
		print(exc)
	except Exception as other:
		print(other)
