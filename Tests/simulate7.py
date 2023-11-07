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
import random

sys.path.append("..")
from Drone import Drone, get_distance_metres
from RepeatTimer import RepeatTimer
from Internet import checkInternetConnection

SEND_INTERVAL = 1
SLEEP_LENGTH = 0.5
BASE_ALT = 6
ROVER_ALT = 3

def sendMsg(client):
    lat = 24.2132313123
    lon = 120.213234326
    alt = 7.7
    current_time = "0723"
    assert(lat/100 < 1 and lat/10 >= 1)               # Assumes in Taiwan, where lat = 24.???
    assert(lon/1000 < 1 and lon/100 >= 1)             # Assumes in Taiwan, where lon = 120.???
    assert(alt/100 < 1)                               # Assumes altitude below 100, if higher the message format requires adaptation
    TCP_msg = str("{:011.8f}".format(lat)) + str("{:012.8f}".format(lon)) + str("{:06.2f}".format(alt)) + str(current_time)
    client.send(TCP_msg.encode())
    print("Sent:",TCP_msg)

def recvMsg(client):
    msg = client.recv(1024)
    str_msg = msg.decode()
    if(str_msg.find("LAND") != -1):
        return 0

    
    print("Received:",str_msg)
    lat = float(str_msg[0:11])
    lon = float(str_msg[11:23])
    alt = float(str_msg[23:29])
    recvTime = int(str_msg[31:33])
    assert(lat/100 < 1 and lat/10 >= 1)               # Assumes in Taiwan, where lat = 24.???
    assert(lon/1000 < 1 and lon/100 >= 1)             # Assumes in Taiwan, where lon = 120.???
    assert(alt/100 < 1)                               # Assumes height below 100, if higher the message format requires adaptation

    p1 = LocationGlobalRelative(lat,lon,alt)

    # currentTime = int(datetime.now().strftime("%S"))
    ''' If the received data was delayed for less than ___ seconds'''
    if(random.random() >= 0.7):
        return p1
    else:
        print("Rover received an outdated message")
        # print(currentTime,recvTime)
        return None
    
if(len(sys.argv) <4): 
    print("Should have 3 arguments: argv[] = [<'base' or 'rover'>, <base's IP>, <port number>]")
    sys.exit()

connection_strings = ["/dev/ttyACM0","/dev/tty.usbmodem14101"]
# connection_string = "/dev/tty.usbmodem14101"

''' Connect to vehicle '''
# for connection_string in connection_strings:
#     vehicle = Drone(connection_string)
#     if(vehicle.connected): break
# vehicle.setStateReport(3)

''' Setting up a checker to see if internet connection works, otherwise land the vehicle'''
# checkConnectTimer = RepeatTimer(10,checkInternetConnection,args=(vehicle,))
# checkConnectTimer.start()
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

    # vehicle.takeoff(BASE_ALT)
    print("Taking off")
    time.sleep(4)
    print("Tookoff")

    # Tell rover to take off
    client.send("TAKEOFF".encode())   
    print("Sent TAKEOFF to rover")


    # Wait for "TOOKOFF" from rover
    msg = client.recv(100).decode()
    if(msg != "TOOKOFF"):
        print("Received incorrect message from rover:", msg)
        sys.exit()
    print("Received TOOKOFF")
    
    # Start sending the coordinates
    sendMsgTimer = RepeatTimer(SEND_INTERVAL,sendMsg,args=(client,))
    sendMsgTimer.start()

    # Start going to the pre-determined points
    for point in points:
        # 1. go to a pre-determined coordinate
        # vehicle.flyToPoint(point, 2)

        print("Flying to a point")
        time.sleep(5)
        print("flew to a point")

        time.sleep(5)

    # Stop sending coordinates
    sendMsgTimer.cancel()

    # Tell rover to land
    client.send("LAND".encode())
    print("Sent LAND to rover")

    # Wait for "LANDED" from rover
    msg = client.recv(100).decode()
    if(msg != "LANDED"):
        print("Received incorrect message from rover:", msg)
        sys.exit()
    print("Received LANDED from rover")

    # Land the base drone
    # vehicle.land()
    print("Landing")
    time.sleep(5)
    print("Landed")

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
    print("Received TAKEOFF")

    # vehicle.takeoff(ROVER_ALT) 
    print("Taking off")
    time.sleep(4)
    print("Tookoff")

    # Tell base that rover has tookoff
    client.send("TOOKOFF".encode())
    print("Sent TOOKOFF to base")

    
    
    # Follow the base drone
    while(1):
        targetPoint = recvMsg(client)

        if(targetPoint == 0):
            print("Received LAND")
            break
        elif(targetPoint != None):
            targetPoint.alt = ROVER_ALT
            print("Received target:",targetPoint)
            print("Flying to target")
            # vehicle.flyToPoint(targetPoint, 2)
            # vehicle.flyToPointNonBlocking(targetPoint, 2)
            time.sleep(SLEEP_LENGTH)
    
    # Landing the rover drone
    # vehicle.land()
    

    # Make sure the vehicle is landed (cause land() is aync) then signal the rover so that they won't collide during landing
    # while(vehicle.vehicle.location.global_relative_frame.alt>=1):
    #     time.sleep(1)

    print("Landing")
    time.sleep(5)
    print("Rover landed")

    # Tell base that rover has landed
    client.send("LANDED".encode())
    print("Sent LANDED to base")


else:
    print("Please specify which drone it is")