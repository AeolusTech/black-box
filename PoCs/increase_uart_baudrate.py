#!/usr/bin/python
# Filename: text.py
import serial
import time
import timeout_decorator

ser = serial.Serial("/dev/ttyS0", 115200)


@timeout_decorator.timeout(3)
def increase_speed():
	W_buff = ["AT\r\n", "AT+IPR=460800\r\n"]
	ser.write(W_buff[0].encode())
	ser.flushInput()
	data = ""
	num = 0
	while True:
		while ser.inWaiting() > 0:
			data += ser.read(ser.inWaiting()).decode()
		if data != "":
			print(data)
			if num < 1:
				time.sleep(1)
				ser.write(W_buff[num+1].encode())

			num =num + 1
			data = ""


try:
	increase_speed()
except UnicodeDecodeError:
	print("UART already set to 460800")
	pass
except timeout_decorator.timeout_decorator.TimeoutError:
	print("UART increased to 460800")
finally:
	if ser != None:
		ser.close()
