from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import sys
import math
import socket

from Drone import Drone

connection_strings = ["/dev/ttyACM0","/dev/tty.usbmodem14101"]
# connection_string = "/dev/tty.usbmodem14101"

''' Connect to vehicle '''
for connection_string in connection_strings:
    vehicle = Drone(connection_string)
    if(vehicle.connected): break

vehicle.emergencyLand()