import logging
import serial
import serial.threaded
import threading

try:
    import queue
except ImportError:
    import Queue as queue


class ATException(Exception):
    pass


class ATProtocol(serial.threaded.LineReader):

    TERMINATOR = b'\r\n'

    def __init__(self):
        super(ATProtocol, self).__init__()
        self.alive = True
        self.responses = queue.Queue()
        self.events = queue.Queue()
        self._event_thread = threading.Thread(target=self._run_event)
        self._event_thread.daemon = True
        self._event_thread.name = 'at-event'
        self._event_thread.start()
        self.lock = threading.Lock()

    def stop(self):
        """
        Stop the event processing thread, abort pending commands, if any.
        """
        self.alive = False
        self.events.put(None)
        self.responses.put('<exit>')

    def _run_event(self):
        """
        Process events in a separate thread so that input thread is not
        blocked.
        """
        while self.alive:
            try:
                self.handle_event(self.events.get())
            except:
                logging.exception('_run_event')

    def handle_line(self, line):
        """
        Handle input from serial port, check for events.
        """
        print(line)
        if line.startswith('+'):
            self.events.put(line)
        else:
            self.responses.put(line)

    def handle_event(self, event):
        """
        Spontaneous message received.
        """
        print('event received:', event)

    def command(self, command, response='OK', timeout=5):
        """
        Set an AT command and wait for the response.
        """
        with self.lock:  # ensure that just one thread is sending commands at once
            self.write_line(command)
            lines = []
            while True:
                try:
                    line = self.responses.get(timeout=timeout)
                    #~ print("%s -> %r" % (command, line))
                    if line == response:
                        print(lines)
                        return lines
                    else:
                        lines.append(line)
                except queue.Empty:
                    raise ATException('AT command timeout ({!r})'.format(command))


# test
if __name__ == '__main__':
    import time

    class SIM868(ATProtocol):
        """
        Example communication with SIM868 BT module.
        Some commands do not respond with OK but with a '+...' line. This is
        implemented via command_with_event_response and handle_event, because
        '+...' lines are also used for real events.
        """

        def __init__(self):
            super(SIM868, self).__init__()
            self.event_responses = queue.Queue()
            self._awaiting_response_for = None

        def connection_made(self, transport):
            super(SIM868, self).connection_made(transport)
            # our adapter enables the module with RTS=low
            self.transport.serial.rts = False
            time.sleep(0.3)
            self.transport.serial.reset_input_buffer()

        def handle_event(self, event):
            """Handle events and command responses starting with '+...'"""
            if event.startswith('+SAPBR') and self._awaiting_response_for.startswith('AT+SAPBR'):
                ip = event[13:13 + 15].rstrip('"')
                self.event_responses.put(ip)
            elif event.startswith('+CCLK') and self._awaiting_response_for.startswith('AT+CCLK?'):
                local_date = event.rstrip('"').lstrip('"')
                self.event_responses.put(local_date)
            elif event.startswith('+CGNSINF') and self._awaiting_response_for.startswith('AT+CGNSINF?'):
                nmea_string = event.lstrip('CGNSINF: ').split(',')
                LAT_POS = 3
                LONG_POS = 4
                lat_long_position = str(nmea_string[LAT_POS], nmea_string[LONG_POS])
                self.event_responses.put(lat_long_position)
            else:
                logging.warning('unhandled event: {!r}'.format(event))

        def command_with_event_response(self, command):
            """Send a command that responds with '+...' line"""
            with self.lock:  # ensure that just one thread is sending commands at once
                self._awaiting_response_for = command
                self.transport.write(command.encode('utf-8') + b'\r\n')
                response = self.event_responses.get()
                self._awaiting_response_for = None
                return response

        # - - - sequence


        def set_bearer_parameter(self):
            self.command("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"", response="OK")

        def set_bearer_context(self):
            self.command("AT+SAPBR=3,1,\"APN\",\"internet\"", response="OK")

        def activate_bearer_context(self):
            self.command("AT+SAPBR=1,1", response="OK", timeout=20)

        def read_bearer_parameter(self) -> str:
            return self.command_with_event_response("AT+SAPBR=2,1")

        def set_gprs_bearer_profile_id(self):
            self.command("AT+CNTPCID=1", response="OK")

        def set_NTP_server_and_timezone(self):
            '''
            e.g. 32/4=8 which is Beijing (GMT+8)
            Poland is 8 -> 8/4 = 2 (GMT+2)

            Open question - summer time???
            '''
            self.command("AT+CNTP=\"0.pl.pool.ntp.org\",8", response="OK")

        def check_NTP_server_and_timezone(self):
            '''
            Honestly, I believe this step can be omitted. It's just a safety check
            '''
            self.command("AT+CNTP?", response="OK")

        def synchronize_time(self):
            self.command("AT+CNTP", response="OK")

        def read_local_time(self):
            return self.command_with_event_response("AT+CCLK?")

        def set_HTTP_download_mode(self):
            self.command("AT+CGNSSAV=3,3", response="OK")

        def init_HTTP_service(self):
            self.command("AT+HTTPINIT", response="OK")

        def set_parameters_for_HTPP_transmission(self):
            self.command("AT+HTTPPARA=\"CID\",1", response="OK")

        def set_URL_for_HTTP_transmission(self):
            self.command("AT+HTTPPARA=\"URL\",\"http://wepodownload.mediatek.com/EPO_GPS_3_1.DAT\"", response="OK")

        def get_session_started(self):
            '''
            Question: maybe it's worth to check for 200 status???
            '''
            self.command("AT+HTTPACTION=0", response="OK", timeout=20)

        def terminate_HTTP_sesion(self):
            self.command("AT+HTTPTERM", response="OK")

        def check_EPO_size(self):
            self.command("AT+CGNSCHK=3,1", response="OK")

        def turn_on_GPS(self):
            self.command("AT+CGNSPWR=1", response="OK")

        def send_EPO_to_GPS(self):
            self.command("AT+CGNSAID=31,1,1", response="OK")

        def get_wgs84_position(self) -> str:
            return self.command_with_event_response("AT+CGNSINF")


    port = "/dev/ttyS0"
    baud = 115200
    ser = serial.serial_for_url(port, baudrate=baud, timeout=1)

    with serial.threaded.ReaderThread(ser, SIM868) as waveshare_module:
        waveshare_module.set_bearer_parameter()
        time.sleep(1)
        waveshare_module.set_bearer_context()
        time.sleep(4)
        waveshare_module.activate_bearer_context()
        time.sleep(1)
        print(f'bearer param with IP: {waveshare_module.read_bearer_parameter()}')
        time.sleep(1)
        waveshare_module.set_gprs_bearer_profile_id()
        time.sleep(1)
        waveshare_module.set_NTP_server_and_timezone()
        time.sleep(1)
        waveshare_module.check_NTP_server_and_timezone()
        time.sleep(1)
        waveshare_module.synchronize_time()
        time.sleep(1)
        print(f'local time: {waveshare_module.read_local_time()}')
        time.sleep(1)
        waveshare_module.set_HTTP_download_mode()
        time.sleep(1)
        waveshare_module.init_HTTP_service()
        time.sleep(1)
        waveshare_module.set_parameters_for_HTPP_transmission()
        time.sleep(1)
        waveshare_module.set_URL_for_HTTP_transmission()
        time.sleep(1)
        waveshare_module.get_session_started()
        time.sleep(1)
        waveshare_module.terminate_HTTP_sesion()
        time.sleep(1)
        waveshare_module.check_EPO_size()
        time.sleep(1)
        waveshare_module.turn_on_GPS()
        time.sleep(1)
        waveshare_module.send_EPO_to_GPS()

        print(f'NMEA string: {waveshare_module.get_wgs84_position()}')