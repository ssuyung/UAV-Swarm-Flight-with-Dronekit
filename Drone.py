from dronekit import connect, VehicleMode, LocationGlobalRelative
import dronekit
import json
import time
import sys
import math
from threading import Timer
from RepeatTimer import RepeatTimer
from datetime import datetime

# Within Accepted Delay (in sec) the received data will be considered valid
ACCEPTED_DELAY = 3 

class Drone(dronekit.Vehicle):
    # (24.78910480,120.99512870) 交大操場入口再往前一點
    def __init__(self, connection_string):  
        print("Connecting to vehicle on: %s" % connection_string)
        self.connected = True
        try:
            self.vehicle = connect(connection_string, wait_ready=True)
        except Exception as e:
            print(e)
            self.connected = False

        
        self.stateCheck=None
        self.stateReportTimer=None
    
    def preArmCheck(self):
        self.vehicle.manualArm = True
        print("Basic pre-arm checks")
        # Don't try to arm until autopilot is ready
        while not self.vehicle.is_armable:
            if self.stateCheck == "land":
                print("exit vechicle armable check loop...")
                return
            else:
                print(" Waiting for vehicle to initialise...")

            time.sleep(1)
        
        print("Arming motors")
        # Copter should arm in GUIDED mode
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True

        # Confirm vehicle armed before attempting to take off
        while not self.vehicle.armed:
            if self.stateCheck == "land":
                print("exit vechicle armed check loop...")
                return
            else:
                self.vehicle.mode = VehicleMode("GUIDED")
                self.vehicle.armed = True
                print(" Waiting for arming...")
            time.sleep(1)

        # Let the propeller spin for a while to warm up so as to increase stability during takeoff
        time.sleep(2)

    def takeoff(self, aTargetAltitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """

        # Waiting for manual confirmation for takeoff
        if(input("Allow takeoff? y/n\n") != "y"):
            pass

        self.preArmCheck()

        print("Taking off!")
        print("Ascending to altitude: "+str(aTargetAltitude))
        self.vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude
        
        
        # Wait until the vehicle reaches a safe height before processing the goto
        #  (otherwise the command after Vehicle.simple_takeoff will execute
        #   immediately).

        while True:
            print("Altitude: ", self.vehicle.location.global_relative_frame.alt)
            print("Ascending to altitude: "+str(aTargetAltitude))

            # Break and return from function just below target altitude.
            if self.vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                print("Reached target altitude")
                break
            elif self.stateCheck == "land":
                print("exit altitude check loop...")
                return
            
            time.sleep(1)

        # fly to takoff location
        print("Exiting takeoff()")

    def flyToPoint(self,targetPoint, speed):
        # point1 = LocationGlobalRelative(float(lat), float(lon), float(alt))
        self.vehicle.airspeed = speed

        print("Target Point: ({:12.8f},{:12.8f},{:5.2f})".format(targetPoint.lat,targetPoint.lon,targetPoint.alt))

        targetDistance = get_distance_metres(self.vehicle.location.global_relative_frame, targetPoint)
        print("Target distance: ",str(targetDistance))

        self.vehicle.simple_goto(targetPoint)
        print("Executed simple_goto()")

        while self.vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
            remainingDistance=get_distance_metres(self.vehicle.location.global_relative_frame, targetPoint)
            print("Distance to target: ", remainingDistance)
            if remainingDistance<=1: #Just below target, in case of undershoot.
                print("Reached target")
                break
            elif self.stateCheck == "land":
                print("exit distance check loop...")
                return

            time.sleep(1)

    def flyToPointNonBlocking(self,targetPoint, speed):
        '''
        Non-blocking flyToPoint, so returning from this function does NOT guarantee the vehicle has reached the target.
        '''
        # point1 = LocationGlobalRelative(float(lat), float(lon), float(alt))
        self.vehicle.airspeed = speed

        print("Target Point: ({:12.8f},{:12.8f},{:5.2f})".format(targetPoint.lat,targetPoint.lon,targetPoint.alt))

        targetDistance = get_distance_metres(self.vehicle.location.global_relative_frame, targetPoint)
        print("Target distance: ",str(targetDistance))

        self.vehicle.simple_goto(targetPoint)
        print("Executed simple_goto()")

    def land(self):
        # Waiting for manual confirmation for landing
        if(input("Allow landing? y/n\n") != "y"):
            pass

        self.stateCheck = "land"
        print("Trying to set vehicle mode to LAND...")
        while(self.vehicle.mode != VehicleMode("LAND")):
            self.vehicle.mode = VehicleMode("LAND")
        print("Landing")
    
    def emergencyLand(self):
        '''
        This function doesn't ask if the user allows landing, but directly lands vehicle.
        In non-emergent cases, use land() instead.
        '''
        self.stateCheck = "land"
        print("Trying to set vehicle mode to LAND...")
        while(self.vehicle.mode != VehicleMode("LAND")):
            self.vehicle.mode = VehicleMode("LAND")
        print("Landing")

    def getState(self):
        stateobj = {
            "Mode" : self.vehicle.mode.name,
            "BatteryVoltage" :self.vehicle.battery.voltage, 
            "BatteryCurrent" :self.vehicle.battery.current,
            "BatteryLevel":self.vehicle.battery.level,
            "IsArmable" : self.vehicle.is_armable,
            "armed" : self.vehicle.armed,
            "airspeed": self.vehicle.airspeed,
            "SystemStatus" : self.vehicle.system_status.state,
            "GlobalLat" : self.vehicle.location.global_frame.lat,
            "GlobalLon" : self.vehicle.location.global_frame.lon,
            "SeaLevelAltitude" : self.vehicle.location.global_frame.alt,
            "RelativeAlt" : self.vehicle.location.global_relative_frame.alt,
            "localAlt":self.vehicle.location.local_frame.down
        }
        if(self.vehicle.home_location!=None):
            stateobj["homeLocationAlt"]=self.vehicle.home_location.alt
            stateobj["homeLocationLat"]=self.vehicle.home_location.lat
            stateobj["homeLocationLon"]=self.vehicle.home_location.lon

        print(stateobj)
    
    def setStateReport(self, interval):
        if(self.stateReportTimer and self.stateReportTimer.is_alive()):
            print("There's already a State Report Timer")
            return -1
        
        self.stateReportTimer = RepeatTimer(interval, self.getState)
        self.stateReportTimer.start()
        print("State Report Set")
        return 0
    
    def cancelStateReport(self):
        if(self.stateReportTimer):
            self.stateReportTimer.cancel()
            self.stateReportTimer = None
            print("State Report Cancelled")
        else:
            print("There is no State Report Timer Running")

    # Base Drone will need to send its coordinates to Rover Drone
    def sendInfo(self,client):
        
        lat = float(self.vehicle.location.global_frame.lat)
        lon = float(self.vehicle.location.global_frame.lon)
        alt = float(self.vehicle.location.global_frame.alt)
        # formatted_height = f"{height_float:06.2f}"
        current_time = datetime.now().strftime("%M%S")    # This will turn the time into minute and second format, something like 0835 (08:35)
        assert(lat <= 90 and lat >= -90)              
        assert(lon <= 180 and lon >= -180)      
        assert(alt < 100)                    # Assumes altitude below 100, if higher the message format requires adaptation
        TCP_msg = str("{:011.8f}".format(lat)) + str("{:012.8f}".format(lon)) + str("{:06.2f}".format(alt)) + str(current_time)
        client.send(TCP_msg.encode())
        print("Sent:",TCP_msg)

    # Rover Drone will need to receive Base's coordinates and keep following it (keep flyToPoint(Base's coordinates))
    def receiveInfo(self, client):
        
        msg = client.recv(1024)
        str_msg = msg.decode()
        if(str_msg.find("LAND") != -1):
            return 0

        print("Received:",str_msg)
        lat = float(str_msg[0:11])
        lon = float(str_msg[11:23])
        alt = float(str_msg[23:29])
        recvTime = int(str_msg[31:33])
        assert(lat <= 90 and lat >= -90)               
        assert(lon <= 180 and lon >= -180)             
        assert(alt < 100)                   # Assumes altitude below 100, if higher the message format requires adaptation

        p1 = LocationGlobalRelative(lat,lon,alt)
        
        print("Distance to the received point:",get_distance_metres(p1,self.vehicle.location.global_frame))

        currentTime = int(datetime.now().strftime("%S"))
        ''' If the received data was delayed for less than ___ seconds'''
        if(timeIsValid(curTime=currentTime,recvTime=recvTime)):
            return p1
        else:
            print("Rover received an outdated message")
            print(currentTime,recvTime)
            return None     

def timeIsValid(recvTime, curTime):
    if(curTime >= recvTime):
        if(curTime-recvTime < ACCEPTED_DELAY): return True
        else: return False
    else:
        if(curTime+60 -recvTime < ACCEPTED_DELAY): return True
        else: return False

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles.
    """
    # 0.00000898 difference => 1 meter
    dlat = float(aLocation2.lat) - float(aLocation1.lat)
    dlong = float(aLocation2.lon) - float(aLocation1.lon)
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

