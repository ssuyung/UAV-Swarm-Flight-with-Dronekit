from dronekit import connect, VehicleMode, LocationGlobalRelative
import json
import time
import sys
import math
from threading import Timer
from rf_function.rf import Transmitter
from rf_function.rf import Vehicle
from BaseDrone import BaseDrone

# connection_string = "/dev/ttyACM0"
connection_string = "/dev/tty.usbmodem14101"

frequency = 1   # Frequency for the sendInfo()


basedrone = BaseDrone(connection_string)

while(1):
    basedrone.sendInfo()
    time.sleep(frequency)   # Delay for 1 second