#!/usr/bin/env python

from typing import no_type_check_decorator
import serial
import time
import logging

AT = {
    "device_ok": b"AT\r\n",
    "set_fast_uart": b"AT+IPR=115200\r\n",
    "set_slow_uart": b"AT+IPR=115200\r\n",
}


class MySerial(object):
    port = "/dev/ttyS0"

    def __init__(self):
        if self.__check_slow_communication__():
            self.__request_faster_uart__()

        self.fast_serial = serial.Serial(
            port=self.port, baudrate=115200, timeout=0.0)

        if not self.__check_fast_communication__():
            raise Exception('Waveshare UART not working at 115200')

    def __enter__(self):
        return self.fast_serial

    def __exit__(self, type, value, traceback):
        self.fast_serial.close()

    def __check_fast_communication__(self):
        self.fast_serial.write(AT["device_ok"])
        self.fast_serial.flushInput()
        if 'OK' not in self.read():
            return False
        return True

    def __check_slow_communication__(self):
        slow_serial = serial.Serial(port=self.port, baudrate=115200)
        slow_serial.write(AT["device_ok"])
        slow_serial.flushInput()

        try:
            if "OK" not in self.read(custom_serial=slow_serial):
                return True
        except UnicodeDecodeError:
            pass  # this usually means that the faster speed is already set

        slow_serial.close()
        return False

    def __request_faster_uart__(self):
        slow_serial = serial.Serial(port=self.port, baudrate=115200)
        slow_serial.write(AT["set_fast_uart"])
        slow_serial.flushInput()

        if "OK" not in self.read(custom_serial=slow_serial):
            raise Exception("Couldn't negotiate faster UART")

        slow_serial.close()

    def read(self, retry_count=2, timeout=0.1, custom_serial=None):
        data = ""
        interval_between_requests = timeout/retry_count

        if custom_serial is not None:
            ser = custom_serial
        else:
            ser = self.fast_serial

        for i in range(retry_count):
            while ser.in_waiting > 0:
                no_of_bytes_to_read = ser.in_waiting
                data += ser.read(no_of_bytes_to_read).decode()
            time.sleep(interval_between_requests)
        return data

    def write(self, command):
        self.fast_serial.write(command)


if __name__ == '__main__':
    try:
        mylogs = logging.getLogger(__name__)
        mylogs.setLevel(logging.DEBUG)

        file = logging.FileHandler("sample.log")
        file.setLevel(logging.INFO)
        fileformat = logging.Formatter(
            "%(asctime)s:%(levelname)s:%(message)s", datefmt="%H:%M:%S")
        file.setFormatter(fileformat)

        mylogs.addHandler(file)
        my_serial = MySerial()
    except Exception as e:
        logging.log(level=logging.ERROR, msg=repr(e))
