import datetime
# from rpi_rf import RFDevice
from rf_func import RFDevice

class Transmitter:
    def __init__(self, gpio, protocol, puslelength, repeat):
        self.gpio = gpio
        self.protocol = protocol
        self.puslelength = puslelength
        self.rfdevice = RFDevice(gpio)
        self.repeat = repeat
        self.timecode = 0
    
    def start(self):
        self.rfdevice.enable_tx()
        self.rfdevice.tx_repeat = self.repeat
    
    def end(self):
        self.rfdevice.cleanup()
    
