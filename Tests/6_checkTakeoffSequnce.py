''' 
In this testcase we test if the takeoff and landing sequence in Test 7 is correct.
Correct sequence: Base takeoff, rover takeoff, rover land, base land.
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
BASE_ALT = 7
ROVER_ALT = 4

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
    
    vehicle.takeoff(BASE_ALT)

    # # Tell rover to take off
    # client.send("TAKEOFF".encode())

    # # Wait for "TOOKOFF" from rover
    # msg = client.recv(100).decode()
    # if(msg != "TOOKOFF"):
    #     print("Received incorrect message from rover:", msg)
    #     sys.exit()
    vehicle.sendInfo(client, "TAKEOFF")

    msg = vehicle.receiveInfo(client)
    if(msg != "TOOKOFF"):
        print("Received incorrect message from rover:", msg)
        sys.exit()

    time.sleep(1)

    # # Tell rover to land
    # client.send("LAND".encode())

    # # Wait for "LANDED" from rover
    # msg = client.recv(100).decode()
    # if(msg != "LANDED"):
    #     print("Received incorrect message from rover:", msg)
    #     sys.exit()
    vehicle.sendInfo(client, "LAND")
    msg = vehicle.receiveInfo(client)
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

    # # Waiting for "TAKEOFF" from base
    # msg = client.recv(10).decode()
    msg = vehicle.receiveInfo(client)
    if(msg != "TAKEOFF"):
        print("Received incorrect message from rover:", msg)
        sys.exit()

    vehicle.takeoff(ROVER_ALT)

    # Tell base that rover has tookoff
    # client.send("TOOKOFF".encode())
    vehicle.sendInfo(client, "TOOKOFF")
    
    msg = vehicle.receiveInfo(client)
    if(msg != "LAND"):
        print("Received incorrect message from rover:", msg)
        sys.exit()

    # Landing the rover drone
    vehicle.land()

    # Make sure the vehicle is landed (cause land() is aync) then signal the rover so that they won't collide during landing
    while(vehicle.vehicle.armed):
        time.sleep(1)

    time.sleep(1)
    print("Rover landed")

    # Tell base that rover has landed
    # client.send("LANDED".encode())
    vehicle.sendInfo(client, "LANDED")


else:
    print("Please specify which drone it is")