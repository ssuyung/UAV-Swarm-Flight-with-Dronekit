''' 
This test is designed for a simple check to see if follower drone actually follows the leader drone. 
We tested it by holding the leader drone in our hand and let the follower drone takeoff and follow the leader.
'''

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

SEND_INTERVAL = 1
SLEEP_LENGTH = 0.5

def sendMsg(client):
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

if(sys.argv[1] == "base"):
    print("=====BASE=====")
    ''' Setting up server '''
    #ip = "172.20.10.8"
    ip = sys.argv[2]
    port = int(sys.argv[3])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(5)
    client, address = server.accept()
    print("Base Connection established")
    
    sendMsgTimer = RepeatTimer(SEND_INTERVAL,sendMsg, args=(client,))
    sendMsgTimer.start()
    while(1):
        print("Base in while loop")
        time.sleep(1)

elif(sys.argv[1] == "rover"):
    print("=====ROVER=====")

    ''' Setting up client '''
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #ip = "172.20.10.8"
    ip = sys.argv[2]
    port = int(sys.argv[3])
    client.connect((ip,port))
    print("Rover Connection Established")
    vehicle.takeoff(3)
    
    counter=0
    numInvalidMsg = 0
    ''' 
    We only want our iterations be counted when the drone actually goes to the point, 
    so only increment counter when the received message is valid. 
    numInvalidMsg is a safety measure that makes sure if the rover forever receives outdated (invalid) message, 
    we will break from the loop and land.
    '''
    while(numInvalidMsg < 5 and counter<5):
        print("Enter Iteration",counter)
        targetPoint = vehicle.receiveInfo(client)
        
        if(targetPoint != None):
            targetPoint.alt = 3
            print("Received target:",targetPoint)
            vehicle.flyToPoint(targetPoint, 2)
            counter = counter+1
            numInvalidMsg = 0
        else:
            numInvalidMsg = numInvalidMsg + 1
        
        time.sleep(SLEEP_LENGTH)
    
    vehicle.land()


else:
    print("Please specify which drone it is")