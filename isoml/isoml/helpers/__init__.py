import threading
import datetime
import configparser
import os

# Based on tornado.ioloop.IOLoop.instance() approach.
# See https://github.com/facebook/tornado
class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
        return cls.__singleton_instance


class Config(SingletonMixin):
    def __init__(self) -> None:
        super().__init__()
        self.config = configparser.ConfigParser()
        self.config.read('/etc/isoml.conf')
    
    def get_new_output_filename_with_timestamp(self):
        iso_timestamp = get_utc_time_iso()
        output_path = self.config['isoml']['output_path']
        plane_name = self.config['plane_info']['name']
        return os.path.join(output_path, plane_name + '_' + iso_timestamp + '.csv')
  
    def get_isoml_frequency(self):
        return int(self.config['isoml']['Frequency'])


def get_utc_time_iso():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
