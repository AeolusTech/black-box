import time
import serial


W_buff = ["AT+CGNSSEQ=\"RMC\"\r\n",
          "AT+CGNSINF\r\n", "AT+CGNSURC=2\r\n", "AT+CGNSTST=1\r\n"]


class Waveshare:
    keeprunning = True

    def __init__(self):
        self.__increase_UART_speed__()

        time.sleep(1)

        self.ser = serial.Serial("/dev/ttyS0", 115200)

        self.ser.write(b"AT+CGNSPWR=1\r\n")
        self.ser.flushInput()

    def __del__(self):
        if self.ser != None:
            self.ser.close()

    def __increase_UART_speed__(self):
        slow_ser = serial.Serial("/dev/ttyS0", 115200)
        slow_ser.write(b"AT\r\n")
        slow_ser.flushInput()

        data = ""
        num = 0

        while slow_ser.inWaiting() > 0:
            data += slow_ser.read(slow_ser.inWaiting()).decode()
            if data != "":
                print(data)
            if num < 1:
                time.sleep(1)
                slow_ser.write(b"AT+IPR=115200\r\n")
                break

            num = num + 1
            data = ""

    def stop(self):
        self.keeprunning = False

    def run(self):
        data = ""
        num = 0
        while self.keeprunning:
            if self.ser.inWaiting() == 0:
                print("Initializing")
                time.sleep(0.5)
            else:
                while self.ser.inWaiting() > 0:
                    data += self.ser.read(self.ser.inWaiting()).decode()

                if data != "":
                    print(data)
                    if num < 4:  # the string have ok
                        print(num)
                        time.sleep(0.5)
                        self.ser.write(W_buff[num+1].encode())
                        num = num + 1
                    if num == 4:
                        time.sleep(0.5)
                        self.ser.write(W_buff[4].encode())
                    data = ""
            time.sleep(1)


if __name__ == '__main__':
    waveshare = Waveshare()
    waveshare.run()
