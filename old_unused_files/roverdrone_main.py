from dronekit import connect, VehicleMode, LocationGlobalRelative
import json
import time
import sys
import math
from threading import Timer
from RepeatTimer import RepeatTimer
from Drone import Drone
from RoverDrone import RoverDrone

from uav import get_distance_metres, flyToPoint, watchstate
from rf_function.rf import Receiver
from rf_function.rf import Vehicle
from rf_function.rf import exithandler

# connection_string = "/dev/ttyACM0"
connection_string = "/dev/tty.usbmodem14101"

roverdrone = RoverDrone(connection_string)
# need to first receiver.start()