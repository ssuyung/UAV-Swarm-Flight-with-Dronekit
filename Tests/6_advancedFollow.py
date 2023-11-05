''' 
In this testcase we will fly two drones, base(leader) and rover(follower) at the same time, and to make sure
that they won't collide in the air, base will need to fly at a lower altitude and will land first, then signal
rover to allow rover to land.
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
BASE_ALT = 3
ROVER_ALT = 6

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
    
    sendMsgTimer = RepeatTimer(SEND_INTERVAL,sendMsg)
    sendMsgTimer.start()

    org = vehicle.vehicle.location.global_frame
    points = list()
    diff = 0.00000898
    points.append(LocationGlobalRelative(24.7882662,120.9951193,BASE_ALT))   # 操場右邊（面對司令台）跑道邊緣往中間兩公尺左右
    points.append(LocationGlobalRelative(24.7882345,120.9951183,BASE_ALT))   # 操場右邊（面對司令台）跑道邊緣

    # points.append(LocationGlobalRelative(float(org.lat)+diff, float(org.lon), BASE_ALT))
    # points.append(LocationGlobalRelative(float(org.lat), float(org.lon)+diff, BASE_ALT))
    # points.append(LocationGlobalRelative(float(org.lat)-diff, float(org.lon), BASE_ALT))
    # points.append(LocationGlobalRelative(float(org.lat), float(org.lon)-diff, BASE_ALT))
    # print(points[0], points[1], points[2], points[3])

    vehicle.takeoff(BASE_ALT)
    
    for point in points:
        # 1. go to a pre-determined coordinate
        vehicle.flyToPoint(point, 2)
        time.sleep(5)

    vehicle.land()

    # Make sure the vehicle is landed then signal the rover so that they won't collide during landing
    while(vehicle.vehicle.location.global_relative_frame.alt>=5):
        time.sleep(1)

    time.sleep(2)
    print("Base landed, closing TCP connection")
    client.close()

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
    vehicle.takeoff(ROVER_ALT)
    
    counter=0
    numInvalidMsg = 0
    ''' 
    We only want our iterations be counted when the drone actually goes to the point, 
    so only increment counter when the received message is valid. 
    numInvalidMsg is a safety measure that makes sure if the rover forever receives outdated (invalid) message, 
    we will break from the loop and land.
    '''
    while(numInvalidMsg < 5 and counter<20):
        print("Enter Iteration",counter)
        targetPoint = vehicle.receiveInfo(client)
        if(targetPoint == 0):
            print("End of TCP connection")
            break
        elif(targetPoint != None):
            targetPoint.alt = ROVER_ALT
            print("Received target:",targetPoint)
            # vehicle.flyToPoint(targetPoint, 2)
            vehicle.flyToPointNonBlocking(targetPoint, 2)
            counter = counter+1
            numInvalidMsg = 0
            time.sleep(0.5)
        else:
            numInvalidMsg = numInvalidMsg + 1
        
        time.sleep(SLEEP_LENGTH)
    
    vehicle.land()

    client.close()

else:
    print("Please specify which drone it is")