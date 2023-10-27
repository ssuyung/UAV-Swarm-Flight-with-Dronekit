from Transmitter import Transmitter
from datetime import datetime

class Sender(Transmitter):
    # TODO: check repeat argument value
    def __init__(self, gpio, protocol, puslelength, repeat):
         super().__init__(gpio,protocol,puslelength,repeat)

    def send_info(self,vehicle):
        '''
        Calls class methods to send all the information 
        '''
        self.timecode = (self.timecode + 1) % 10
        self.send_time_height(self.timecode, vehicle)
        self.send_lat(self.timecode, vehicle)
        self.send_lon(self.timecode, vehicle)

    def send_lat(self, vehicle):
        '''
        Sends the latitude of the vehicle
        '''
        string = str(1) + str(self.timecode) + str("{:.6f}".format(float(vehicle.location.global_frame.lat)))
        code = int(string.replace('.', ''))
        self.rfdevice.tx_code(code, self.protocol, self.puslelength)
    
    def send_lon(self, vehicle):
        '''
        Sends the longitude of the vehicle
        '''
        string = str(2) + str(self.timecode) + str("{:.5f}".format(float(vehicle.location.global_frame.lon)))
        code = int(string.replace('.', ''))
        self.rfdevice.tx_code(code, self.protocol, self.puslelength)

    def send_time_height(self, vehicle):
        '''
        Sends the time and height of the vehicle
        '''
        height_float = float(vehicle.location.global_frame.alt)
        formatted_height = f"{height_float:05.2f}"
        current_time = datetime.now().strftime("%H%M%S")    # This will turn the time into 24H format, something like 210835 (21:08:35)
        print("Current time:", current_time)
        # TODO: Check time format
        time_float = float(current_time)
        formatted_time = f"{time_float % 10:04.2f}"
        print("Formatted time:", formatted_time)
        string = str(3) + str(self.timecode) + str(formatted_height) + str(formatted_time)
        code = int(string.replace('.', ''))
        self.rfdevice.tx_code(code, self.protocol, self.puslelength)

sender = Sender(gpio=17, protocol=1, puslelength=200, repeat=10)
sender.send_time_height(0,None)