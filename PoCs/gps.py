#!/usr/bin/python
# Filename: text.py

import asyncio
import serial_asyncio

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






GGA_LAT_INDEX = 2
GGA_NORTH_SOUTH_HEMISPEHERE = 3
GGA_LONG_INDEX = 4
GGA_EAST_WEST_HEMISPEHERE = 5



def parse_and_return_lat_long(data):
    '''
    Response example:
    1,0,19800106000115.093,,,,0.00,0.0,0,,,,,,0,0,,,,,
    '''

    split_data = data.split(',')
    lat_nmea_string = split_data[GGA_LAT_INDEX]
    is_south = split_data[GGA_NORTH_SOUTH_HEMISPEHERE] == 'S'


    long_nmea_string = split_data[GGA_LONG_INDEX]
    is_west = split_data[GGA_EAST_WEST_HEMISPEHERE] == 'W'


    latitude = None
    longitude = None

    if long_nmea_string and lat_nmea_string:
        latitude = NmeaToDecimal_lat(lat_nmea_string, is_south)
        longitude = NmeaToDecimal_long(long_nmea_string, is_west)

    return latitude, longitude


def NmeaToDecimal_lat(lat_string, is_south):
    '''
    https://stackoverflow.com/questions/36254363/how-to-convert-latitude-and-longitude-of-nmea-format-data-to-decimal
    '''
    lat_degrees = int(lat_string[0:2])
    lat_minutes = float(lat_string[2:])

    latitude = lat_degrees + lat_minutes/60.0

    if is_south:
        return -1.0 * latitude
    return latitude


def NmeaToDecimal_long(long_string, is_west):
    long_degrees = int(long_string[0:3])
    long_minutes = float(long_string[3:])
    longitude = long_degrees + long_minutes/60.0
    if is_west:
        return -1.0 * longitude
    return longitude





port = "/dev/ttyS0"
baud = 115200

messages = [
b"AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"\r\n",       # Set bearer parameter
b"AT+SAPBR=3,1,\"APN\",\"internet\"\r\n",       # Set bearer context
b"AT+SAPBR=1,1\r\n",                            # Active bearer context
b"AT+SAPBR=2,1\r\n",							# Read bearer parameter
b"AT+CNTPCID=1\r\n",                            # Set GPRS Bearer Profile's ID
b"AT+CNTP=\"0.pl.pool.ntp.org\",8\r\n",         # set NTP server and time zone. they said that 32/4=8 which is Beijing (GMT+8)
b"AT+CNTP?\r\n",                                # read NTP server and timezone
b"AT+CNTP\r\n",                                 # synchronize time
b"AT+CCLK?\r\n",                                # read local time
b"AT+CGNSSAV=3,3\r\n",                          # set HTTP download mode
b"AT+HTTPINIT\r\n",                          # init HTTP service
b"AT+HTTPPARA=\"CID\",1\r\n",                          # set parameters for HTTP transmission
b"AT+HTTPPARA=\"URL\",\"http://wepodownload.mediatek.com/EPO_GPS_3_1.DAT\"\r\n",
b"AT+HTTPACTION =\"CID\",1\r\n",                          # get session start. Should have 200 in the response
b"AT+HTTPTERM\r\n",                          # terminate HTTP session
b"AT+CGNSCHK=3,1\r\n",                          # check EPO size
b"AT+CGNSPWR=1\r\n",                          # turn on GPS
b"AT+CGNSAID=31,1,1\r\n",                          # send EPO to GPS
b"AT+CGNSINF\r\n"                          # read GPS location
]

sleeps = [
2,
3,
20,
5,
5,
5,
5,
5,
5,
5,
5,
5,
5,
5,
5,
5,
5,
5,
5
]



assert len(messages) == len(sleeps)


async def main():
    asyncState = type('', (), {})()
    asyncState.acknowledged = True
    asyncState.receiving_finished = True
    asyncState.counter = 0

    reader, writer = await serial_asyncio.open_serial_connection(url=port, baudrate=115200)
    print('Reader and writer created')
    sent = send(writer, asyncState)
    received = recv(reader, asyncState)
    await asyncio.gather(sent, received)


async def send(w, asyncState):
    while True:
        if asyncState.receiving_finished:
            if asyncState.acknowledged:
                asyncState.acknowledged = False

            counter = asyncState.counter
            msg = messages[counter]
            single_sleep = sleeps[counter]

            w.write(msg)
            asyncState.receiving_finished = False
            if counter >= len(messages):
                break
            print(f'sent{counter}: {msg.decode().rstrip()}')
            await asyncio.sleep(single_sleep)
    w.write(b'DONE\n')
    print('Done sending')


async def recv(r, asyncState):
    while True:
        msg = await r.readuntil(b'\n')
        msg_rstripped = msg.rstrip()

        if msg_rstripped == b'DONE':
            print('Done receiving')
            break
        print(f'received{asyncState.counter}: {msg_rstripped.decode()}')
        if b'OK' in msg_rstripped or b'ERROR' in msg_rstripped:
            asyncState.receiving_finished = True
            if b'OK' in msg_rstripped:
                asyncState.acknowledged = True
                asyncState.counter = asyncState.counter + 1



loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()