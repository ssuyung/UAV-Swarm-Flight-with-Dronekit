import argparse
import logging
import time
import datetime
from rpi_rf import RFDevice
amount_of_info = 3
timecode = [0] * amount_of_info
valid = [False] * amount_of_info
def check_pusle_and_protocol(rfdevice):
    protocol = 1
    pulselength = 200
    interval = 10
    if(rfdevice.rx_pulselength  > pulselength + interval or rfdevice.rx_pulselength  < pulselength - interval):
        return False
    if(rfdevice.rx_proto != protocol):
        return False
    return True

def check_type(type_of_info):
    if(type_of_info <=2 and type_of_info >= 0):
        return True
    return False

def info_detail(type_of_info, info):
    if(type_of_info == 0):
        return str(info / 1000000)
    elif(type_of_info == 1):
        return str(info / 100000)
    elif(type_of_info == 2):
        tmp1 = info % 1000
        tmp2 = (info - tmp1) / 100000
        return str(tmp2), str(tmp1 / 100)
 
class Vehicle:
    def __init__(self, latitude, longitude, height, time, timecode):
        self.latitude = latitude
        self.longitude = longitude
        self.height = height
        self.time = time
        self.timecode = timecode
    
    def update_by_uav(self, new_latitude, new_longitude, new_height, new_time,timecode):
        self.latitude = new_latitude
        self.longitude = new_longitude
        self.height = new_height
        self.time = new_time
        self.timecode = timecode

    def update_by_rf_msg(self, info):
        str_info = str(info)
        if(len(str_info) < 8): return
        type_of_info = int(str_info[0]) - 1
        new_timecode = int(str_info[1])
        new_info = int(str_info[2:])
        #print("type_of_info: ", type_of_info)
        if(check_type(type_of_info) == True and valid[type_of_info] == True):
            if(self.timecode[type_of_info] != new_timecode):
                self.timecode[type_of_info] = new_timecode
                file_write("--------START---------")
                file_write(str((datetime.datetime.now())))
                file_write("Timecode: [" + str(self.timecode[2]) + ", " + str(self.timecode[0]) + ", " + str(self.timecode[1]) + "]")
                if(type_of_info == 0):
                    self.latitude = info_detail(type_of_info, new_info)
                    file_write("lat: " + str(self.latitude))
                elif(type_of_info == 1):
                    self.longitude = info_detail(type_of_info, new_info)
                    file_write("lon: " + str(self.longitude))
                elif(type_of_info == 2):
                    self.height, self.time = info_detail(type_of_info, new_info)
                    file_write("height: " + str(self.height))
                    file_write("time: " + str(self.time))
                file_write("---------END----------")
                
                
        elif(check_type(type_of_info) == True):
            self.timecode[type_of_info] = new_timecode
            valid[type_of_info] = True
            print("-------VALID----------")
            print("Timecode: ", self.timecode)
            if(type_of_info == 0):
                self.latitude = info_detail(type_of_info, new_info)
                print("lat: ", self.latitude)
            elif(type_of_info == 1):
                self.longitude = info_detail(type_of_info, new_info)
                print("lon: ", self.longitude)
            elif(type_of_info == 2):
                self.height, self.time = info_detail(type_of_info, new_info)
                print("time: ", self.time)
                print("height: ", self.height)
    
    def update_by_hand(self, timecode):
        self.timecode = timecode
        float_lat = float(self.latitude)
        float_lon = float(self.longitude)
        float_height = float(self.height)
        float_time = float(self.time)
        float_lat = float_lat + 0.01
        float_lon = float_lon + 0.01
        float_height = float_height - 0.1
        float_time = float_time + 0.1
        self.latitude = str(float_lat)
        self.longitude = str(float_lon)
        self.height = str(float_height)
        self.time = str(float_time)
        
    def update_by_TCP(self, msg):
        print(msg)
        
    def write_to_file(self, record_filename):
        file = open(record_filename, 'a')
        file.write("--------START---------")
        file.write("\n")
        file.write(str((datetime.datetime.now())))
        file.write("\n")
        file.write(str(self.timecode))
        file.write("\n")
        file.write(str(self.time))
        file.write("\n")
        file.write(str(self.latitude))
        file.write("\n")
        file.write(str(self.longitude))
        file.write("\n")
        file.write(str(self.height))
        file.write("\n")
        file.write("---------END----------")
        file.write("\n")
        file.close()

class Transmitter:
    def __init__(self, gpio, protocol, puslelength, repeat):
        self.gpio = gpio
        self.protocol = protocol
        self.puslelength = puslelength
        self.rfdevice = RFDevice(gpio)
        self.repeat = repeat
    
    def send_lat(self, timecode, vehicle):
        string = str(1) + str(timecode) + str("{:.6f}".format(float(vehicle.latitude)))
        code = int(string.replace('.', ''))
        self.rfdevice.tx_code(code, self.protocol, self.puslelength)
    
    def send_lon(self, timecode, vehicle):
        string = str(2) + str(timecode) + str("{:.5f}".format(float(vehicle.longitude)))
        code = int(string.replace('.', ''))
        self.rfdevice.tx_code(code, self.protocol, self.puslelength)

    def send_time_height(self, timecode, vehicle):
        height_float = float(vehicle.height)
        formatted_height = f"{height_float:05.2f}"
        time_float = float(vehicle.time)
        formatted_time = f"{time_float % 10:04.2f}"
        string = str(3) + str(timecode) + str(formatted_height) + str(formatted_time)
        code = int(string.replace('.', ''))
        self.rfdevice.tx_code(code, self.protocol, self.puslelength)
    
    def start(self):
        self.rfdevice.enable_tx()
        self.rfdevice.tx_repeat = self.repeat
    
    def end(self):
        self.rfdevice.cleanup()
    

class Receiver:
    def __init__(self, gpio, protocol, puslelength, repeat):
        self.gpio = gpio
        self.protocol = protocol
        self.puslelength = puslelength
        self.rfdevice = RFDevice(gpio)
        self.repeat = repeat
    
    def start(self):
        self.rfdevice.enable_rx()
    
    def end(self):
        self.rfdevice.cleanup()


def file_write(string):
    record_filename = "x_rover.txt"
    file = open(record_filename, 'a')
    file.write(string)
    file.write("\n")
    file.close()

# pylint: disable=unused-argument
def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)