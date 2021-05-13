#!/usr/bin/python
# Filename: text.py
import serial
import time
ser = serial.Serial("/dev/ttyS0", 115200)
W_buff = ["AT\r\n", "AT+IPR=460800\r\n"] #, "AT+IPR?\r\n"]
ser.write(W_buff[0].encode())
ser.flushInput()
data = ""
num = 0

try:
	while True:
		#print(ser.inWaiting())
		while ser.inWaiting() > 0:
			data += ser.read(ser.inWaiting()).decode()
		if data != "":
			print(data)
			#if data.count("O") > 0 and data.count("K") > 0 and num < 3:	# the string have ok
			if num < 1:
				time.sleep(1)
				ser.write(W_buff[num+1].encode())

			num =num +1
			data = ""
except KeyboardInterrupt:
	if ser != None:
		ser.close()
