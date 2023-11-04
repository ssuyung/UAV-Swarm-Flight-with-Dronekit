'''
argv[] = [<"base" or "rover">, <base's IP>, <port number>]
'''
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import sys
import math
import socket

sys.path.append("..")
from Drone import Drone
from RepeatTimer import RepeatTimer
from Internet import checkInternetConnection

from get_ip import get_ip_address_and_base_or_rover

def sendMsg():
    vehicle.sendInfo(client)

if(len(sys.argv) <4): 
    print("Should have 3 arguments: argv[] = [<'base' or 'rover'>, <base's IP>, <port number>]")
    sys.exit()

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

ip, base_or_rover = get_ip_address_and_base_or_rover()

if(base_or_rover == "base"):
    print("=====BASE=====")
    ''' Setting up server '''
    #ip = "172.20.10.8"
    #ip = sys.argv[2]
    port = int(sys.argv[1])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(5)
    client, address = server.accept()
    print("Base Connection established")
    
    sendMsgTimer = RepeatTimer(1,sendMsg)
    sendMsgTimer.start()
    while(1):
        print("Base in while loop")
        time.sleep(1)

elif(base_or_rover == "rover"):
    print("=====ROVER=====")

    ''' Setting up client '''
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #ip = "172.20.10.8"
    #ip = sys.argv[2]
    port = int(sys.argv[1])
    client.connect((ip,port))
    print("Rover Connection Established")
    
    counter=0
    while(counter<5):
        print("Enter Iteration",counter)
        targetPoint = vehicle.receiveInfo(client)
        
        if(targetPoint != None):
            targetPoint.alt = 3
            print("Received target:",targetPoint)
        counter = counter+1
        time.sleep(0.7)
    


else:
    print("Please specify which drone it is")