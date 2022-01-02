#!/usr/bin/python
# Filename: text.py
import serial
import threading
import time


# GPS response data
#
# $GNGGA,235953.093,,,,,0,0,,,M,,M,,*57
# $GPGSA,A,1,,,,,,,,,,,,,,,*1E
# $GLGSA,A,1,,,,,,,,,,,,,,,*02
# $GPGSV,1,1,00*79
# $GLGSV,1,1,00*65
# $GNRMC,235953.093,V,,,,,0.00,0.00,050180,,,N*5E
# $GNVTG,0.00,T,,M,0.00,N,0.00,K,N*2C


# The address field starts with “$” followed by the talker ID and a sentence identifier. The used talker IDs are:
#  GP for GPS only solutions
#  GL for GLONASS only solutions
#  GN for multi GNSS solutions
#
# Additional:
#  GA for GALILEO only solutions

# The used sentence identifiers are:
#  GGA – Global Positioning System Fix Data
#  VTG – Course over Ground and Ground Speed
#  GSA – GNSS DOP and Active Satellites
#  GSV – GNSS Satellites in View
#  RMC – Recommended Minimum Specific GNSS Data


class GPS(threading.Thread):
	ser = serial.Serial("/dev/ttyS0",115200)
	
	RMC_LAT_INDEX = 61
	RMC_LONG_INDEX = 62

	W_buff = ["AT+CGNSPWR=0\r\n", # power off GNSS
		  "AT+CGNSPWR=1\r\n", # power on GNSS
		  "AT+CGNSSEQ=\"RMC\"\r\n", # define the last NMEA sentence that parsed
		  # NMEA - National Marine Electronics Association
		  # RMC - Recommended Minimum Specific GNSS Data
          "AT+CGNSINF\r\n", # read GNSS navigation information
		  "AT+CGNSURC=2\r\n", # set Unsolicited Result Code reporting every 2 GNSS fix 
		  "AT+CGNSTST=1\r\n" # send NMEA data to AT UART
		]
	
	data_len = len(W_buff) - 1
	data = ""
	num = 0
	lat = 0
	long = 0


	def __init__(self):
		threading.Thread.__init__(self)
		self.ser.write(self.W_buff[0].encode())
		self.ser.flushInput()
		
	def run(self):
		try:
			while True:
				if self.ser.inWaiting() == 0:
					# print ("Initializing")
					time.sleep(0.5)
				else:
					while self.ser.inWaiting() > 0:
						self.data += self.ser.read(self.ser.inWaiting()).decode()
					if self.data != "":
						print(self.data)
						if  self.num < self.data_len:
							# print(self.num)
							time.sleep(0.5)
							self.ser.write(self.W_buff[self.num+1].encode())
						if self.num == self.data_len:
							time.sleep(0.5)
							self.ser.write(self.W_buff[self.data_len].encode())
						if self.num > self.data_len:
							if 'GNRMC' in self.data:
								self.lat, self.long = self.parse_and_return_lat_long(self.data)
						self.data = ""
						self.num = self.num +1
		finally:
			if self.ser != None:
				self.ser.close()


	def parse_and_return_lat_long(self, data):
		'''
		Response example:
		1,0,19800106000115.093,,,,0.00,0.0,0,,,,,,0,0,,,,,
		'''
		split_data = data.split(',')
		lat = split_data[self.RMC_LAT_INDEX]
		long = split_data[self.RMC_LONG_INDEX]
		return lat, long

	def get_labels(self):
		return ['lat', 'long']

	def get_data(self):
		return [self.lat, self.long]
