from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import sys
import math
import socket
from datetime import datetime

sys.path.append("..")
from Drone import Drone
from RepeatTimer import RepeatTimer
from Internet import checkInternetConnection

f = open("connectiontest.txt", "w")
f.write("START\n")

connection_strings = ["/dev/ttyACM0","/dev/tty.usbmodem14101"]
# connection_string = "/dev/tty.usbmodem14101"

''' Connect to vehicle '''
for connection_string in connection_strings:
    vehicle = Drone(connection_string)
    if(vehicle.connected): break
vehicle.setStateReport(3)

''' Setting up a checker to see if internet connection works, otherwise land the vehicle'''
checkConnectTimer = RepeatTimer(10,checkInternetConnection,args=(vehicle,f,))
checkConnectTimer.start()
print("Check Connect Timer Set")
f.write("At time "+datetime.now().strftime("%H%M%S")+" Connect Timer set.\n")

checkConnectTimer.join()
f.close()

''' 
Here you can check if it will try to land the vehicle after disconnecting wifi/Internet
'''

