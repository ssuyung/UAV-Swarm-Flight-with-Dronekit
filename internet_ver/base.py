from dronekit import connect, VehicleMode, LocationGlobalRelative
import json
import time
import sys
import math
import socket
from threading import Timer
sys.path.append("..")

from rf_function.rf import Transmitter
from rf_function.rf import Vehicle\

ip = "172.20.10.8"
port = int(sys.argv[1])
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip,port))
server.listen(5)
client, address = server.accept()
print("Connection established - {address[0]}:{address[1]}")

timecode = 0
self_vehicle = Vehicle("24.546546", "120.583748", "77.20", "10.00", [timecode, timecode, timecode])
other_vehicle = Vehicle("24.546546", "120.583748", "77.20", "10.00", [timecode, timecode, timecode])

record_filename = "z_base.txt"
file = open(record_filename, 'a')
file.write("--------------------------")
file.write(record_filename)
file.write("--------------------------")
file.write("\n")
file.close()


# connection_string = "/dev/ttyACM0"
connection_string = "/dev/tty.usbmodem14101"

print("Connect to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, wait_ready=True)


stateCheck = None

# A class that will repeatedly execute by the given interval
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

def watchstate():
    stateobj = {
        "Mode" : vehicle.mode.name,
        "BatteryVoltage" :vehicle.battery.voltage, 
        "BatteryCurrent" :vehicle.battery.current,
        "BatteryLevel":vehicle.battery.level,
        "IsArmable" : vehicle.is_armable,
        "armed" : vehicle.armed,
        "airspeed": vehicle.airspeed,
        "SystemStatus" : vehicle.system_status.state,
        "GlobalLat" : vehicle.location.global_frame.lat,
        "GlobalLon" : vehicle.location.global_frame.lon,
        "SeaLevelAltitude" : vehicle.location.global_frame.alt,
        "RelativeAlt" : vehicle.location.global_relative_frame.alt,
        "localAlt":vehicle.location.local_frame.down
    }
    if(vehicle.home_location!=None):
        stateobj["homeLocationAlt"]=vehicle.home_location.alt
        stateobj["homeLocationLat"]=vehicle.home_location.lat
        stateobj["homeLocationLon"]=vehicle.home_location.lon

    # sendobj = json.dumps(stateobj) # code from previous year's work, not used for now
    print(stateobj)
    # Timer(5.0,watchstate).start() # calling the next thread to continue outputting the states, 
                                    # but this implementation leads to an infinite amount of threads,
                                    # which causes weird errors, so we now use repeattimer instead

timer = RepeatTimer(5, watchstate)
timer.start()

# Base Drone will need to send its coordinates to Rover Drone
def sendInfo():
    timecode = (timecode + 1) % 10
    
    self_vehicle.update_by_uav(vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, vehicle.location.global_frame.alt)
    height_float = float(self_vehicle.height)
    formatted_height = f"{height_float:05.2f}"
    time_float = float(self_vehicle.time)
    formatted_time = f"{time_float % 10:04.2f}"
    TCP_msg = "V" + str("{:.6f}".format(float(self_vehicle.latitude))) + str("{:.5f}".format(float(self_vehicle.longitude))) \
            +  str(formatted_height) + str(formatted_time)
    client.send(TCP_msg.encode())
    
    self_vehicle.write_to_file(record_filename)
    
    self_vehicle.write_to_file(record_filename)


infoTimer = RepeatTimer(1, sendInfo)
infoTimer.start()





def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles.
    """
    dlat = float(aLocation2.lat) - float(aLocation1.lat)
    dlong = float(aLocation2.lon) - float(aLocation1.lon)
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5



def takeoff(aTargetAltitude, goP1, goP2):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready

    while not vehicle.is_armable:
        if stateCheck == "land":
            print("exit vechicle armable check loop...")
            return
        else:
            print(" Waiting for vehicle to initialise...")

        time.sleep(1)
    
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        if stateCheck == "land":
            print("exit vechicle armed check loop...")
            return
        else:
            vehicle.mode = VehicleMode("GUIDED")
            vehicle.armed = True
            print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    print("Ascending to altitude: "+str(aTargetAltitude))
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude
    
    
    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).

    while True:
        print("Altitude: ", vehicle.location.global_relative_frame.alt)
        print("Ascending to altitude: "+str(aTargetAltitude))

        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        elif stateCheck == "land":
            print("exit altitude check loop...")
            return
        
        time.sleep(1)


    # print("Set default/target airspeed to 3")
    vehicle.airspeed = 1


    # fly to point1
    # point1 = LocationGlobalRelative(float(goP1['lat']), float(goP1['lon']), 10)
    # print("Target Point 1:"+str(point1))

    # targetDistance = get_distance_metres(vehicle.location.global_relative_frame, point1)
    # print("Target distance: "+str(targetDistance))

    # vehicle.simple_goto(point1)
    # print("Executed simple_goto(P1)")

    # while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
    #     remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, point1)
    #     print("Distance to target: ", remainingDistance)
    #     if remainingDistance<=1: #Just below target, in case of undershoot.
    #         print("Reached target")
    #         break
    #     elif stateCheck == "land":
    #         print("exit distance check loop...")
    #         return

    #     time.sleep(1)
    flyToPoint(goP1['lat'], goP1['lon'], 10)

    # print("rp1 slp3")
    # time.sleep(3)

    # fly to point2
    # point2 = LocationGlobalRelative(float(goP2['lat']), float(goP2['lon']), 10)
    # print("Target Point 2:"+str(point2))

    # targetDistance = get_distance_metres(vehicle.location.global_relative_frame, point2)
    # print("Target distance: "+str(targetDistance))

    # vehicle.simple_goto(point2)
    # print("Executed simple_goto(2)")

    # while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
    #     remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, point2)
    #     print("Distance to target: ", remainingDistance)
    #     if remainingDistance<=1: #Just below target, in case of undershoot.
    #         print("Reached target")
    #         break
    #     elif stateCheck == "land":
    #         print("exit distance check loop...")
    #         return

    #     time.sleep(1)
    flyToPoint(goP2['lat'], goP2['lon'], 10)

    # print("rp2 slp3")
    # time.sleep(3)


    if stateCheck == "land":
        print("return ...")
        return

    print("Returning to Launch")
    vehicle.mode = VehicleMode("RTL")

    # fly to takoff location
    print("Exiting takeoff()")


# one point to one point
def flyToPoint(lat,lon, alt):
    # point = LocationGlobalRelative(float(lat), float(lon), 10)
    # print(point)

    # targetDistance = get_distance_metres(vehicle.location.global_relative_frame, point)
    # print(targetDistance)

    # vehicle.simple_goto(point)
    # print("simple_goto")

    # while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
    #     remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, point2)
    #     print("Distance to target: ", remainingDistance)
    #     if remainingDistance<=targetDistance*0.01: #Just below target, in case of undershoot.
    #         print("Reached target")
    #         break
    #     elif stateCheck == "land":
    #         print("exit distance check loop...")
    #         return

    #     time.sleep(1)
     # fly to point1
    point1 = LocationGlobalRelative(float(lat), float(lon), float(alt))
    print("Target Point: ({:12.8f},{:12.8f},{:5.2f})".format(float(lat),float(lon),float(alt)))
    # print("Target Point: "+str(point1))

    targetDistance = get_distance_metres(vehicle.location.global_relative_frame, point1)
    print("Target distance: ",str(targetDistance))

    vehicle.simple_goto(point1)
    print("Executed simple_goto(P1)")

    while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
        remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, point1)
        print("Distance to target: ", remainingDistance)
        if remainingDistance<=1: #Just below target, in case of undershoot.
            print("Reached target")
            break
        elif stateCheck == "land":
            print("exit distance check loop...")
            return

        time.sleep(1)
    # print("rp slp3")
    # time.sleep(3)
    # Timer(1.0,flytopoint,[nlat,nlon]).start()




print("while loop")
test_alt = 0.5

while 1:
    print("loop...")
    line = sys.stdin.readline().strip()
    print(line)

    # PT (24.7948542,120.9922114),(1,2)
    # the format should be exactly: "PT (lat1,lon1),(lat2,lon2)"
    if line[0:2] == "PT":
        print("is PT")
        breakc = 0
        secS = 0
        p1 = {}
        p2 = {}

        for i in range(4,len(line)):
            if line[i] == ',':
                p1['lat'] = line[4:i]
                breakc = i + 1
            elif line[i] == ')':
                p1['lon'] = line[breakc:i]
                secS = i + 3
                break

        for i in range(secS,len(line)):
            if line[i] == ',':
                p2['lat'] = line[secS:i]
                breakc = i + 1
            elif line[i] == ')':
                p2['lon'] = line[breakc:i]
                secS = i + 3
                break
        
        # print("end calculate")
        # print("P1: "+p1['lat'] + " " + p1['lon'])
        # print("P2: "+p2['lat'] + " " + p2['lon'])

        stateCheck = None
        Timer(1.0, takeoff, [test_alt,p1,p2]).start()

    elif line == "land":
        print("Received LAND")
        stateCheck = "land"
        while(vehicle.mode != VehicleMode("LAND")):
            print("Trying to set vehicle mode to LAND")
            vehicle.mode = VehicleMode("LAND")
        print("Landing")

    elif line == "state":
        watchstate()
        
    elif line == "start":
        print("Starting state report")
        timer = RepeatTimer(1, watchstate)
        timer.start()

    elif line == "stop":
        print("Stopping state report")
        timer.cancel()
# vehicle.close()