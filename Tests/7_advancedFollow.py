''' 
In this testcase we will fly two drones, base(leader) and rover(follower) at the same time, and to make sure
that they won't collide in the air, base will need to fly at a higher altitude, takeoff first, and land after rover.
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
from Drone import Drone, get_distance_metres
from RepeatTimer import RepeatTimer
from Internet import checkInternetConnection

SEND_INTERVAL = 1
SLEEP_LENGTH = 0.5
BASE_ALT = 6
ROVER_ALT = 3

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


if(sys.argv[1] == "base"):
    print("=====BASE=====")
    ''' Setting up server '''
    # ip = "172.20.10.8"
    ip = sys.argv[2]
    port = int(sys.argv[3])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(5)
    client, address = server.accept()
    print("Base Connection established")
    

    points = list()
    diff = 0.00000898
    points.append(LocationGlobalRelative(24.7882662,120.9951193,BASE_ALT))   # 操場右邊（面對司令台）跑道邊緣往中間兩公尺左右
    points.append(LocationGlobalRelative(24.7882345,120.9951183,BASE_ALT))   # 操場右邊（面對司令台）跑道邊緣

    vehicle.takeoff(BASE_ALT)

    # Tell rover to take off
    client.send("TAKEOFF".encode())

    # Wait for "TOOKOFF" from rover
    msg = client.recv(100).decode()
    if(msg != "TOOKOFF"):
        print("Received incorrect message from rover:", msg)
        sys.exit()

    # Start sending the coordinates
    sendMsgTimer = RepeatTimer(SEND_INTERVAL,sendMsg)
    sendMsgTimer.start()

    # Start going to the pre-determined points
    for point in points:
        # 1. go to a pre-determined coordinate
        vehicle.flyToPoint(point, 2)
        time.sleep(5)

    # Stop sending coordinates
    sendMsgTimer.cancel()

    # Tell rover to land
    client.send("LAND".encode())

    # Wait for "LANDED" from rover
    msg = client.recv(100).decode()
    if(msg != "LANDED"):
        print("Received incorrect message from rover:", msg)
        sys.exit()

    # Land the base drone
    vehicle.land()

# elif(sys.argv[1] == "rover"):
elif(sys.argv[1] == "rover"):
    print("=====ROVER=====")

    ''' Setting up client '''
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ip = "172.20.10.8"
    ip = sys.argv[2]
    port = int(sys.argv[3])
    client.connect((ip,port))
    print("Rover Connection Established")

    # Waiting for "TAKEOFF" from base
    msg = client.recv(10).decode()
    if(msg != "TAKEOFF"):
        print("Received incorrect message from rover:", msg)
        sys.exit()

    vehicle.takeoff(ROVER_ALT)

    # Tell base that rover has tookoff
    client.send("TOOKOFF".encode())
    
    
    # Follow the base drone
    while(1):
        targetPoint = vehicle.receiveInfo(client)

        if(targetPoint == 0):
            print("Received LAND")
            break
        elif(targetPoint != None):
            targetPoint.alt = ROVER_ALT
            print("Received target:",targetPoint)
            # vehicle.flyToPoint(targetPoint, 2)
            vehicle.flyToPointNonBlocking(targetPoint, 2)
            counter = counter+1
            numInvalidMsg = 0            
            time.sleep(SLEEP_LENGTH)
    
    # Landing the rover drone
    vehicle.land()

    # Make sure the vehicle is landed (cause land() is aync) then signal the rover so that they won't collide during landing
    while(vehicle.vehicle.location.global_relative_frame.alt>=1):
        time.sleep(1)

    time.sleep(1)
    print("Rover landed")

    # Tell base that rover has landed
    client.send("LANDED".encode())


else:
    print("Please specify which drone it is")