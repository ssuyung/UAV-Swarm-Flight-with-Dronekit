from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import sys
import math
import socket
sys.path.append("..")
from SimDrone import Drone
from RepeatTimer import RepeatTimer, sendMsg

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
    
    vehicle = Drone("/dev/tty.usbmodem14101")
    # for i in range(4):
    #     vehicle.sendInfo(client,"COORDINATES")
    #     time.sleep(1)

    sendMsgTimer = RepeatTimer(1,sendMsg, args=(vehicle, client,))
    sendMsgTimer.start()

    vehicle.sendInfo(client, "TAKEOFF")
    time.sleep(1)

    msg = vehicle.receiveInfo(client)
    if(msg != "TOOKOFF"):
        print("ERROR: Expect TOOKOFF but received", msg)
        sys.exit(1)

    vehicle.sendInfo(client, "LAND")
    msg = vehicle.receiveInfo(client)
    if(msg != "LANDED"):
        print("ERROR: Expect LANDED but received", msg)
        sys.exit(1)

    time.sleep(1)

    # client.close()

elif(sys.argv[1] == "rover"):
    print("=====ROVER=====")

    ''' Setting up client '''
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ip = "172.20.10.8"
    ip = sys.argv[2]
    port = int(sys.argv[3])
    client.connect((ip,port))
    print("Rover Connection Established")

    vehicle = Drone("/dev/tty.usbmodem14101")
    while(1):
        msg = vehicle.receiveInfo(client)
        print(msg)
        time.sleep(0.4)

    # for i in range(4):
    #     msg = vehicle.receiveInfo(client)
    #     # print(type(msg)==LocationGlobalRelative)
    #     time.sleep(0.8)

    # msg = vehicle.receiveInfo(client)
    # if(msg != "TAKEOFF"):
    #     print("ERROR: Expect TAKEOFF but received", msg)
    #     sys.exit(1)
    # # vehicle.takeoff(5)
    # vehicle.sendInfo(client,"TOOKOFF")
    # time.sleep(1)

    # msg = vehicle.receiveInfo(client)
    # if(msg != "LAND"):
    #     print("ERROR: Expect LAND but received", msg)
    #     sys.exit(1)
    # # vehicle.takeoff(5)
    # vehicle.sendInfo(client,"LANDED")

    client.close()

        
    


else:
    print("Please specify which drone it is")