from dronekit import connect, VehicleMode, LocationGlobalRelative
import sys
import socket
import time
sys.path.append("..")

from Drone import Drone
from Internet import checkInternetConnection
from RepeatTimer import RepeatTimer

# connection_string = "/dev/ttyACM0"
connection_string = "/dev/tty.usbmodem14101"

''' Connect to vehicle '''
vehicle = Drone(connection_string)
vehicle.setStateReport(3)

''' Setting up a checker to see if internet connection works, otherwise land the vehicle'''
checkConnectTimer = RepeatTimer(1,checkInternetConnection,args=(vehicle,))
checkConnectTimer.start()

''' Setting up server '''
# ip = "172.20.10.8"
ip = "192.168.229.147"
port = int(sys.argv[1])
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip,port))
server.listen(5)
client, address = server.accept()
print("Base Connection established - {address[0]}:{address[1]}")


while(1):
    vehicle.sendInfo(client)
    time.sleep(1)
