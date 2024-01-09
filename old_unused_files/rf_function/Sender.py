from Transmitter import Transmitter
from datetime import datetime
import math

# TODO: put encoder (and decoder in Receiver) in a single function to increase readability
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
        Sends the latitude of the vehicle. 
        The message should be an integer of at most 10-digit by RF API definition. 
        Only the digits AFTER the decimal point of the latitude will be sent due to this restriction.
        120.9922114 => 99221140
        Example output: 1033240000
        '''
        latitude = float(vehicle.location.global_frame.lat)
        # latitude = 12.33240
        truncated_latitude = self.truncate(latitude,8)
        padded_latitude = "{:.8f}".format(truncated_latitude)   # Pad the latitude until reaches 8-digit after decimal point
        formatted_latitude = str(padded_latitude)[-8:]
        string = str(1) + str(self.timecode) + formatted_latitude
        code = int(string.replace('.', ''))
        # print("Lat code:",code)
        self.rfdevice.tx_code(code, self.protocol, self.puslelength)
    
    def send_lon(self, vehicle):
        '''
        Sends the longitude of the vehicle.
        The message should be an integer of at most 10-digit by RF API definition.
        Only the digits AFTER the decimal point of the latitude will be sent due to this restriction.
        24.7948542 => 79485420
        Example output: 2045600780
        '''
        longitude = float(vehicle.location.global_frame.lon)
        # longitude = 123.4560078
        truncated_lon = self.truncate(longitude,8)
        padded_lon = "{:.8f}".format(truncated_lon)   # Pad the longitude until reaches 8-digit after decimal point
        formatted_lon = str(padded_lon)[-8:]
        string = str(2) + str(self.timecode) + formatted_lon
        code = int(string.replace('.', ''))
        # print("Lon code:",code)
        self.rfdevice.tx_code(code, self.protocol, self.puslelength)

    def send_time_height(self, vehicle):
        '''
        Sends the time and height of the vehicle
        The message should be an integer of at most 10-digit by RF API definition
        Only the following information will be sent due to this restriction:
            Time takes up 3 digits (the last digit of minute and two digits of second)
            Height takes up 5 digits (123.552 meters => 12355; 23.2342 => 02323)
        Example output: 3002322857
        '''
        height_float = float(vehicle.location.global_frame.alt)
        # height_float = 23.223
        formatted_height = f"{height_float:06.2f}".replace('.','')
        # print("Formatted height:", formatted_height)
        
        current_time = datetime.now().strftime("%M%S")    # This will turn the time into minute and second format, something like 0835 (08:35)
        formatted_time = current_time[-3:]                # Only the last digit of minute and the seconds needed, so 0835 => 835
        code = str(3) + str(self.timecode) + formatted_height + formatted_time
        # print("Height & Time code:",code)
        self.rfdevice.tx_code(code, self.protocol, self.puslelength)

    def truncate(self,f, n):
        '''
        Truncates a float to n'th digit after decimal point without rounding(truncate(123.45678, 4) => 123.4567)
        '''
        return math.floor(f * 10 ** n) / 10 ** n
    
# sender = Sender(gpio=17, protocol=1, puslelength=200, repeat=10)
# sender.send_lat(None)
# sender.send_lon(None)
# sender.send_time_height(None)