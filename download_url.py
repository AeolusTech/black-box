#!/usr/bin/python
# Filename: text.py

import serial
import time


# following this shit https://exploreembedded.com/wiki/Setting_up_GPRS_with_SIM800L

ser = serial.Serial("/dev/ttyS0", 115200)
W_buff = ["AT\r\n",
          "AT+CFUN=1\r\n",
          "AT+CPIN?\r\n",
          "AT+CSTT=\"internet\",\"\",\"\"\r\n",
          "AT+CIICR\r\n",
          "AT+CIFSR\r\n",
          "AT+CIPSTART=\"TCP\",\"exploreembedded.com\",80\r\n",
          "AT+CIPSEND=63\r\n", ">\r\n", "GET\r\n", "exploreembedded.com/wiki/images/1/15/Hello.txt\r\n", "HTTP/1.0\r\n"
          ]
ser.write(W_buff[0].encode())
ser.flushInput()
data = ""
num = 0

try:
    while True:
        # print(ser.inWaiting())
        while ser.inWaiting() > 0:
            data += ser.read(ser.inWaiting()).decode()
        if data != "":
            print(data)
            if num < 6:
                time.sleep(1)
                ser.write(W_buff[num+1].encode())
            # if num == 3 and data.count(">") > 0:
            if num == 6:
                # print(W_buff[4])
                time.sleep(0.5)
                ser.write(W_buff[7].encode())
                time.sleep(0.5)
                ser.write(W_buff[8].encode())
                time.sleep(0.5)
                ser.write(W_buff[9].encode())
                time.sleep(0.5)
                ser.write(W_buff[10].encode())
                time.sleep(0.5)
                ser.write(W_buff[11].encode())
                # time.sleep(0.5)
                # ser.write("\x1a\r\n".encode())# 0x1a : send   0x1b : Cancel send
            num = num + 1
            data = ""
except KeyboardInterrupt:
    if ser != None:
        ser.close()
