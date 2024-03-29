''' 
In this testcase we test if the takeoff and landing sequence in Test 8 is correct.
Correct sequence: Base takeoff, rover1 takeoff, rover2 takeoff, rover2 land, rover1 land, base land.
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
from RepeatTimer import RepeatTimer, sendMsg
from Internet import checkInternetConnection

SEND_INTERVAL = 1
SLEEP_LENGTH = 0.5
BASE_ALT = 10
ROVER1_ALT = 7
ROVER2_ALT = 4

if(len(sys.argv) <4): 
    print("Should have 3 arguments: argv[] = [<'base' or 'rover1' or 'rover2'>, <base's IP>, <port number>]")
    sys.exit()

if(sys.argv[1] == "base"):
    if(len(sys.argv) < 5):
        print("Should have 4 arguments: argv[] = [<'base' or 'rover1' or 'rover2'>, <base's IP>, <port number 1>, <port number 2>]")
        sys.exit()

connection_strings = ["/dev/ttyACM0","/dev/tty.usbmodem14101"]

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

    vehicle.takeoff(BASE_ALT)

    # Tell rover 1 to take off
    # client1.send("TAKEOFF".encode())
    vehicle.sendInfo(client1, "TAKEOFF")
    print("Sent TAKEOFF to rover 1")

    # Wait for "TOOKOFF" from rover
    # msg = client1.recv(100).decode()
    msg = vehicle.receiveInfo(client1)
    if(msg != "TOOKOFF"):
        print("Received incorrect message from rover 1:", msg)
        sys.exit()
    print("Received TOOKOFF from rover 1")


    # Tell rover 2 to take off
    # client2.send("TAKEOFF".encode())
    vehicle.sendInfo(client2, "TAKEOFF")
    print("Sent TAKEOFF to rover 2")

    # Wait for "TOOKOFF" from rover
    # msg = client2.recv(100).decode()
    msg = vehicle.receiveInfo(client2)
    if(msg != "TOOKOFF"):
        print("Received incorrect message from rover 2:", msg)
        sys.exit()
    print("Received TOOKOFF from rover 2")

    time.sleep(2)

    # Tell rover 2 to land
    vehicle.sendInfo(client2, "LAND")
    print("Sent LAND to rover 2")

    # Wait for "LANDED" from rover 2
    msg = vehicle.receiveInfo(client2)
    if(msg != "LANDED"):
        print("Received incorrect message from rover 2:", msg)
        sys.exit()
    print("Received LANDED from rover 2")

    # Tell rover 1 to land
    vehicle.sendInfo(client1, "LAND")
    print("Sent LAND to rover 1")

    # Wait for "LANDED" from rover 1
    msg = vehicle.receiveInfo(client1)
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
    msg = vehicle.receiveInfo(client)
    if(msg != "TAKEOFF"):
        print("Received incorrect message from base:", msg)
        sys.exit()
    print("Received TAKEOFF")

    vehicle.takeoff(ROVER_ALT)

    # Tell base that rover has tookoff
    vehicle.sendInfo(client, "TOOKOFF")
    print("Sent TOOKOFF")

    msg = vehicle.receiveInfo(client)
    if(msg != "LAND"):
        print("Received incorrect message from rover:", msg)
        sys.exit()
        
    print("Received LAND")
    # Landing the rover drone
    vehicle.land()

    # Make sure the vehicle is landed (cause land() is aync) and disarmed
    while(vehicle.vehicle.armed):
        time.sleep(1)

    time.sleep(1)
    print("Rover landed")

    # Tell base that rover has landed
    vehicle.sendInfo(client, "LANDED")
    print("Sent LANDED")



else:
    print("Please specify which drone it is")