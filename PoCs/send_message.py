#!/usr/bin/python
# Filename: text.py
from webbrowser import get
import serial
import time
import smbus
import psutil

bus = smbus.SMBus(1) # 1 indicates /dev/i2c-1


ser = serial.Serial("/dev/ttyS0", 115200)

W_buff = [
"AT\r\n", "AT+CMGF=1\r\n",
"AT+CSCA=\"+48790998250\"\r\n",
"AT+CMGS=\"512213012\"\r\n"
]
ser.write(W_buff[0].encode())
ser.flushInput()
data = ""
num = 0


def get_time() -> str:
    return time.ctime(time.time())

def get_IP() -> str:
    return 'IP: ' + '192.168.0.107'

def get_current_position() -> str:
    return 'GNSS' + '50.093008,19.992256'

def get_i2c_status() ->str:
    detected_devices = []

    for device in range(128):
        try:
            bus.read_byte(device)
            detected_devices.append(hex(device))
        except: # exception if read_byte fails
            pass
    return 'i2c: ' + ', '.join(detected_devices)

def get_cpu_load() -> str:
    return 'cpu: ' + str(psutil.cpu_percent())

def get_memory_stats() -> str:
    return 'mem: ' + str(psutil.virtual_memory().percent)

def get_status_message() -> str:
    data = [get_time(), get_IP(), get_i2c_status(), get_cpu_load(), get_memory_stats()]
    return '\n'.join(data)


try:
    while True:
#        print("Waiting!")
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
                ser.write(get_status_message().encode())
                # 0x1a : send   0x1b : Cancel send
                ser.write("\x1a\r\n".encode())
            num = num + 1
            data = ""
except KeyboardInterrupt:
    if ser != None:
        ser.close()
