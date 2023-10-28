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

interval = 1   # interval for the sendInfo(), in second


basedrone = BaseDrone(connection_string)

while(1):
    basedrone.sendInfo()
    time.sleep(interval)   # Delay for (interval) second