#!/usr/bin/python
# Filename: text.py
import serial
import time
ser = serial.Serial("/dev/ttyS0", 460800)
W_buff = ["AT\r\n", "AT+CMGF=1\r\n", "AT+CSCA=\"+48790998250\"\r\n",
          "AT+CMGS=\"512213012\"\r\n", "Jak latasz tym samolotem ty luju, kurwa?!"]
ser.write(W_buff[0].encode())
ser.flushInput()
data = ""
num = 0

try:
    while True:
        print("Waiting!")
        # print(ser.inWaiting())
        while ser.inWaiting() > 0:
            data += ser.read(ser.inWaiting()).decode()
        if data != "":
            print(data)
            # if data.count("O") > 0 and data.count("K") > 0 and num < 3:	# the string have ok
            if num < 3:
                time.sleep(1)
                ser.write(W_buff[num+1].encode())
            # if num == 3 and data.count(">") > 0:
            if num == 3:
                # print(W_buff[4])
                time.sleep(0.5)
                ser.write(W_buff[4].encode())
                # 0x1a : send   0x1b : Cancel send
                ser.write("\x1a\r\n".encode())
            num = num + 1
            data = ""
except KeyboardInterrupt:
    if ser != None:
        ser.close()
