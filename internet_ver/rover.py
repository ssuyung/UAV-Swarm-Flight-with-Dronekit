from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import sys
import math
import socket

sys.path.append("..")
from Drone import Drone
from RepeatTimer import RepeatTimer
from Internet import checkInternetConnection

# connection_string = "/dev/ttyACM0"
connection_string = "/dev/tty.usbmodem14101"

''' Connect to vehicle '''
vehicle = Drone(connection_string)
vehicle.setStateReport(3)
# vehicle.takeoff(3)

''' Setting up a checker to see if internet connection works, otherwise land the vehicle'''
checkConnectTimer = RepeatTimer(10,checkInternetConnection,args=(vehicle,))
checkConnectTimer.start()

''' Setting up client '''
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ip = "172.20.10.8"
ip = "192.168.229.226"
port = int(sys.argv[1])
client.connect((ip,port))
print("Rover Connection Established")


while(1):
    targetPoint = vehicle.receiveInfo(client)
    # if(targetPoint != None):
    #     vehicle.flyToPoint(targetPoint)
    time.sleep(1)
