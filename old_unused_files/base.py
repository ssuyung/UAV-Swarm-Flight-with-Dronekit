from dronekit import connect, VehicleMode, LocationGlobalRelative
import sys
import socket
import time
sys.path.append("..")

from Drone import Drone
from Internet import checkInternetConnection
from RepeatTimer import RepeatTimer


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

''' Setting up server '''
# ip = "172.20.10.8"
ip = "192.168.229.226"
port = int(sys.argv[1])
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip,port))
server.listen(5)
client, address = server.accept()
print("Base Connection established - {address[0]}:{address[1]}")

def sendMsg():
    vehicle.sendInfo(client)

sendMsgTimer = RepeatTimer(1,sendMsg)
sendMsgTimer.start()

while(1):
    print("working")
    time.sleep(1)

''' Base's mission '''
