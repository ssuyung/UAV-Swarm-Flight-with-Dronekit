from dronekit import connect, VehicleMode, LocationGlobalRelative
import json
import time
import sys
import math
from threading import Timer
from rf_function.rf import Transmitter
from rf_function.rf import Vehicle

puslelength = 200
# Initialize the rf trasmitter        
transmitter = Transmitter(gpio=17, protocol=1, puslelength=puslelength, repeat=10)
# Start transmitting
transmitter.start()

timecode = 0
self_vehicle = Vehicle("24.546546", "120.583748", "77.20", "10.00", [timecode, timecode, timecode])
other_vehicle = Vehicle("24.546546", "120.583748", "77.20", "10.00", [timecode, timecode, timecode])

record_filename = "z_base.txt"
file = open(record_filename, 'a')
file.write("--------------------------")
file.write(record_filename)
file.write("--------------------------")
file.write("\n")
file.close()


# connection_string = "/dev/ttyACM0"
connection_string = "/dev/tty.usbmodem14101"

print("Connect to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, wait_ready=True)


# Base Drone will need to send its coordinates to Rover Drone
def sendInfo():
    timecode = (timecode + 1) % 10
    self_vehicle.update_by_uav(vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, vehicle.location.global_frame.alt)
    transmitter.send_time_height(timecode, self_vehicle)
    transmitter.send_lat(timecode, self_vehicle)
    transmitter.send_lon(timecode, self_vehicle)
    
    self_vehicle.write_to_file(record_filename)
