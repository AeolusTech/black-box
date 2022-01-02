#!/usr/bin/python
# Filename: text.py
import serial
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


ser = serial.Serial("/dev/ttyS0",115200)

W_buff = ["AT+CGNSPWR=0\r\n", # power off GNSS
		  "AT+CGNSPWR=1\r\n", # power on GNSS
		  "AT+CGNSSEQ=\"RMC\"\r\n", # define the last NMEA sentence that parsed
		  # NMEA - National Marine Electronics Association
		  # RMC - Recommended Minimum Specific GNSS Data
          "AT+CGNSINF\r\n", # read GNSS navigation information
		  "AT+CGNSURC=2\r\n", # set Unsolicited Result Code reporting every 2 GNSS fix 
		  "AT+CGNSTST=1\r\n" # send NMEA data to AT UART
		]

RMC_LAT_INDEX = 61
RMC_LONG_INDEX = 62


data_len = len(W_buff) - 1

ser.write(W_buff[0].encode())
ser.flushInput()
data = ""
num = 0

def parse_and_return_lat_long(data):
	'''
	Response example:
	1,0,19800106000115.093,,,,0.00,0.0,0,,,,,,0,0,,,,,
	'''
	split_data = data.split(',')
	lat = split_data[RMC_LAT_INDEX]
	long = split_data[RMC_LONG_INDEX]
	return lat, long
	


try:
	while True:
		if ser.inWaiting() == 0:
			# print ("Initializing")
			time.sleep(0.5)
		else:
			while ser.inWaiting() > 0:
				data += ser.read(ser.inWaiting()).decode()
			if data != "":
				print(data)
				if  num < data_len:
					print(num)
					time.sleep(0.5)
					ser.write(W_buff[num+1].encode())
				if num == data_len:
					time.sleep(0.5)
					ser.write(W_buff[data_len].encode())
				if num > data_len:
					# os.system('clear')
					if 'GNRMC' in data:
						lat, long = parse_and_return_lat_long(data)
						print(lat, long)
					# print(parse_and_return_lat_long(data))
				data = ""
				num =num +1
except keyboardInterrupt:
	if ser != None:
		ser.close()
		
