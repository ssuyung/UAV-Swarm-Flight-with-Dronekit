''' 
In this testcase we will fly two drones, base(leader) and rover(follower) at the same time, and to make sure
that they won't collide in the air, base will need to fly at a higher altitude, takeoff first, and land after rover.
'''

'''
argv[] = [<"base" or "rover">, <base's IP>, <port number (for rover 1)>, <port number 2(for rover 2, only base required)>]
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
BASE_ALT = 10
ROVER1_ALT = 7
ROVER2_ALT = 4

def sendMsg(client):
    vehicle.sendInfo(client)

if(len(sys.argv) <4): 
    print("Should have 3 arguments: argv[] = [<'base' or 'rover1' or 'rover2'>, <base's IP>, <port number>]")
    sys.exit()

if(sys.argv[1] == "base"):
    if(len(sys.argv) < 5):
        print("Should have 4 arguments: argv[] = [<'base' or 'rover1' or 'rover2'>, <base's IP>, <port number 1>, <port number 2>]")
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
    ip = sys.argv[2]
    port1 = int(sys.argv[3])
    server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server1.bind((ip,port1))
    server1.listen(5)
    
    
    port2 = int(sys.argv[4])
    server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server2.bind((ip,port2))
    server2.listen(5)

    client1, address1 = server1.accept()
    print("Base Connection 1 established")

    client2, address2 = server2.accept()
    print("Base Connection 2 established")

    points = list()
    diff = 0.00000898
    # points.append(LocationGlobalRelative(24.7882662,120.9951193,BASE_ALT))   # 操場右邊（面對司令台）跑道邊緣往中間兩公尺左右
    # points.append(LocationGlobalRelative(24.7882345,120.9951183,BASE_ALT))   # 操場右邊（面對司令台）跑道邊緣
    points.append(LocationGlobalRelative(24.7891883,120.9949769,BASE_ALT))
    points.append(LocationGlobalRelative(24.7891822,120.9951456,BASE_ALT))

    vehicle.takeoff(BASE_ALT)

    # Tell rover 1 to take off
    client1.send("TAKEOFF".encode())
    print("Sent TAKEOFF to rover 1")

    # Wait for "TOOKOFF" from rover
    msg = client1.recv(100).decode()
    if(msg != "TOOKOFF"):
        print("Received incorrect message from rover 1:", msg)
        sys.exit()
    print("Received TOOKOFF from rover 1")


    # Tell rover 2 to take off
    client2.send("TAKEOFF".encode())
    print("Sent TAKEOFF to rover 1")

    # Wait for "TOOKOFF" from rover
    msg = client2.recv(100).decode()
    if(msg != "TOOKOFF"):
        print("Received incorrect message from rover 2:", msg)
        sys.exit()
    print("Received TOOKOFF from rover 2")

    time.sleep(2)

    # Tell rover 2 to land
    client2.send("LAND".encode())
    print("Sent LAND to rover 2")

    # Wait for "LANDED" from rover 2
    msg = client2.recv(100).decode()
    if(msg != "LANDED"):
        print("Received incorrect message from rover 2:", msg)
        sys.exit()
    print("Received LANDED from rover 2")

    # Tell rover 1 to land
    client1.send("LAND".encode())
    print("Sent LAND to rover 1")

    # Wait for "LANDED" from rover 1
    msg = client1.recv(100).decode()
    if(msg != "LANDED"):
        print("Received incorrect message from rover 1:", msg)
        sys.exit()
    print("Received LANDED from rover 1")

    # Land the base drone
    vehicle.land()

elif(sys.argv[1][0:5] == "rover"):
    if(sys.argv[1][-1] == "1"):
        print("=====ROVER 1=====")
        ROVER_ALT = ROVER1_ALT
    elif(sys.argv[1][-1] == "2"):
        print("=====ROVER 2=====")
        ROVER_ALT = ROVER2_ALT
    else:
        print("Incorrect Sequence Number of Rover")

    ''' Setting up client '''
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = sys.argv[2]
    port = int(sys.argv[3])
    client.connect((ip,port))
    print("Rover Connection Established")

    # Waiting for "TAKEOFF" from base
    msg = client.recv(10).decode()
    if(msg != "TAKEOFF"):
        print("Received incorrect message from base:", msg)
        sys.exit()
    print("Received TAKEOFF")

    vehicle.takeoff(ROVER_ALT)

    # Tell base that rover has tookoff
    client.send("TOOKOFF".encode())
    print("Sent TOOKOFF")

    targetPoint = vehicle.receiveInfo(client)
    if(targetPoint == 0):
        print("Received LAND")
    else:
        print("Received incorrect message from rover:", msg)
        sys.exit()
        
    # Landing the rover drone
    vehicle.land()

    # Make sure the vehicle is landed (cause land() is aync) and disarmed
    while(vehicle.vehicle.armed):
        time.sleep(1)

    time.sleep(1)
    print("Rover landed")

    # Tell base that rover has landed
    client.send("LANDED".encode())
    print("Sent LANDED")



else:
    print("Please specify which drone it is")