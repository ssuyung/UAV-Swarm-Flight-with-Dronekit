''' 
In this testcase we will fly two drones, base(leader) and rover(follower) at the same time, and to make sure
that they won't collide in the air, base will need to fly at a higher altitude, takeoff first, and land after rover.
'''


from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import sys
import math
import socket

sys.path.append("..")
from Drone import Drone, get_distance_metres
from RepeatTimer import RepeatTimer
from Internet import checkInternetConnection

SEND_INTERVAL = 1
SLEEP_LENGTH = 0.5
BASE_ALT = 7
ROVER_ALT = 4


connection_strings = ["/dev/ttyACM0","/dev/tty.usbmodem14101"]
# connection_string = "/dev/tty.usbmodem14101"

''' Connect to vehicle '''
for connection_string in connection_strings:
    vehicle = Drone(connection_string)
    if(vehicle.connected): break
vehicle.setStateReport(3)

''' Setting up a checker to see if internet connection works, otherwise land the vehicle'''
checkConnectTimer = RepeatTimer(10,checkInternetConnection,args=(vehicle,))
checkConnectTimer.start()
print("Check Connect Timer Set")

points = list()
diff = 0.00000898
points.append(LocationGlobalRelative(24.7882662,120.9951193,BASE_ALT))   # 操場右邊（面對司令台）跑道邊緣往中間兩公尺左右
points.append(LocationGlobalRelative(24.7882345,120.9951183,BASE_ALT))   # 操場右邊（面對司令台）跑道邊緣


if(sys.argv[1] == "base"):
    print("=====BASE=====")
    
    vehicle.takeoff(BASE_ALT)

    # Start going to the pre-determined points
    for point in points:
        # 1. go to a pre-determined coordinate
        point.alt = BASE_ALT
        vehicle.flyToPoint(point, 2)
        time.sleep(3)

    # Land the base drone
    vehicle.land()

elif(sys.argv[1] == "rover"):
    print("=====ROVER=====")

    vehicle.takeoff(ROVER_ALT)

    # Start going to the pre-determined points
    for point in points:
        # 1. go to a pre-determined coordinate
        point.alt = ROVER_ALT
        vehicle.flyToPoint(point, 2)
        time.sleep(3)

    # Landing the rover drone
    vehicle.land()


else:
    print("Please specify which drone it is")