from dronekit import connect, VehicleMode, LocationGlobalRelative
import json
import time
import sys
import math
from threading import Timer
from rf_function.rf import Transmitter
from rf_function.rf import Vehicle
from rf_function.Sender import Sender
from Drone import Drone


class BaseDrone(Drone):
    # Base Drone will need to send its coordinates to Rover Drone
    def __init__(self, connection_string):
        super().__init(connection_string)
        self.sender = Sender(gpio=17, protocol=1, puslelength=200, repeat=10)

    def sendInfo(self):
        self.sender.send_info(self)
        # self.sender.timecode = (self.sender.timecode + 1) % 10
        # self_vehicle.update_by_uav(vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, vehicle.location.global_frame.alt)
        # self.sender.send_time_height(self.sender.timecode, self)
        # self.sender.send_lat(self.sender.timecode, self)
        # self.sender.send_lon(self.sender.timecode, self)
        
        # self_vehicle.write_to_file(record_filename)
