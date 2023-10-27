from dronekit import connect, VehicleMode, LocationGlobalRelative
import json
import time
import sys
import math
from threading import Timer
from RepeatTimer import RepeatTimer
from Drone import Drone

from uav import get_distance_metres, flyToPoint, watchstate
from rf_function.rf import Receiver
from rf_function.rf import Vehicle
from rf_function.rf import exithandler

# TODO: complete RoverDrone class
pulselength = 200

timestamp = None

# Initialize the rf trasmitter        
receiver = Receiver(gpio=27, protocol=1, puslelength=pulselength, repeat=3)
# Start transmitting
receiver.start()


amount_of_info = 3
timecode = [0] * amount_of_info
valid = [False] * amount_of_info
# Initialize the vehicle
#timecode = 0
self_vehicle = Vehicle("24.546546", "120.583748", "77.20", "10.00", timecode)
other_vehicle = Vehicle("24.546546", "120.583748", "77.20", "10.00", timecode)

record_filename = "x_rover.txt"
file = open(record_filename, 'a')
file.write(record_filename)
file.write("\n")
file.close()


# connection_string = "/dev/ttyACM0"
connection_string = "/dev/tty.usbmodem14101"

print("Connect to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, wait_ready=True)

stateCheck = None

# Rover Drone will need to receive Base's coordinates and keep following it (keep flyToPoint(Base's coordinates))
def ReceiveInfo():
    # recvObj = ?
    # Pre-Process the object here (check the time, rebuild the coordinates etc.)
    # flyToPoint() (we need to kill the previous thread of flyToPoint first, or there would be several threads trying to fly to different points)
    sleep_or_not = True
    if receiver.rfdevice.rx_code_timestamp != timestamp:
        #if(check_pusle_and_protocol(rfdevice) == False):
        #    continue
        timestamp = receiver.rfdevice.rx_code_timestamp
        info = receiver.rfdevice.rx_code
        str_info = str(info)
        if((str_info[0] == "1" and len(str_info) <= 10) or (str_info[0] == "2" and len(str_info) <= 10) or (str_info[0] == "3" and len(str_info) <= 9)):
            other_vehicle.update_by_rf_msg(info)
            point1 = LocationGlobalRelative(float(other_vehicle.latitude), float(other_vehicle.longitude), float(other_vehicle.height))
            point2 = LocationGlobalRelative(float(vehicle.location.global_frame.lat), float(vehicle.location.global_frame.lon), float(vehicle.location.global_frame.alt))
            print(get_distance_metres(point1, point2))
        else: sleep_or_not = False
    if(sleep_or_not): time.sleep(0.01)
