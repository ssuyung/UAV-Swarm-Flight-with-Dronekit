'''
This is a simmulator drone to test programs
'''

from dronekit import connect, VehicleMode, LocationGlobalRelative
import dronekit
import json
import time
import sys
import math
from threading import Timer
from RepeatTimer import RepeatTimer
from datetime import datetime
from Protocol import Protocol

# Within Accepted Delay (in sec) the received data will be considered valid
ACCEPTED_DELAY = 3 
class FakeDrone():
    def __init(self):
        self.armed = False
class Drone(dronekit.Vehicle):
    def __init__(self, connection_string):  
        print("Connecting to vehicle on: %s" % connection_string)
        self.vehicle = FakeDrone()
        self.connected = True
        self.stateCheck=None
        self.stateReportTimer=None
        self.protocol = Protocol()
    
    def preArmCheck(self):
        print("Basic pre-arm checks")
        time.sleep(1)
        
        print("Arming motors")
        time.sleep(2)
        self.vehicle.armed = True

    def takeoff(self, aTargetAltitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """

        # Waiting for manual confirmation for takeoff
        while(input("\033[93m {}\033[00m".format("Allow takeoff? y/n\n")) != "y"):
            pass

        self.preArmCheck()

        print("Taking off!")
        print("Ascending to altitude: "+str(aTargetAltitude))
        
        time.sleep(2)
        print("Reached target altitude")
        print("Exiting takeoff()")

    def flyToPoint(self,targetPoint, speed):
        print("Target Point: ({:12.8f},{:12.8f},{:5.2f})".format(targetPoint.lat,targetPoint.lon,targetPoint.alt))

        print("Executed simple_goto()")

        time.sleep(1)
        print("Reached target")

    def flyToPointNonBlocking(self,targetPoint, speed):
        '''
        Non-blocking flyToPoint, so returning from this function does NOT guarantee the vehicle has reached the target.
        '''

        print("Target Point: ({:12.8f},{:12.8f},{:5.2f})".format(targetPoint.lat,targetPoint.lon,targetPoint.alt))

        # self.vehicle.simple_goto(targetPoint)
        print("Executed simple_goto()")

    def land(self):
        # Waiting for manual confirmation for landing
        while(input("\033[93m {}\033[00m".format("Allow landing? y/n\n")) != "y"):
            pass

        self.stateCheck = "land"
        print("Trying to set vehicle mode to LAND...")
        time.sleep(1)
        print("Landing")
        self.vehicle.armed = False
    
    def emergencyLand(self):
        '''
        This function doesn't ask if the user allows landing, but directly lands vehicle.
        In non-emergent cases, use land() instead.
        '''
        self.stateCheck = "land"
        print("Trying to set vehicle mode to LAND...")
        time.sleep(1)
        print("Landing")
        self.vehicle.armed = False

    def getState(self):
        stateobj = {
            "TestObject": 1
        }

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

    def sendInfo(self,client, msgName):
        if msgName == "COORDINATES":
            lat = 24.52457821
            lon = 120.213213175
            alt = 5.0
            current_time = datetime.now().strftime("%M%S")          # This will turn the time into minute and second format, something like 0835 (08:35)
            # assert(lat <= 90 and lat >= -90)              
            # assert(lon <= 180 and lon >= -180)      
            # assert(alt < 100)                    # Assumes altitude below 100, if higher the message format requires adaptation
            TCP_msg = "0"+ str("{:011.8f}".format(lat)) + str("{:012.8f}".format(lon)) + str("{:06.2f}".format(alt)) + str(current_time)
            client.send(TCP_msg.encode())
            print("Sent:",TCP_msg)
        elif msgName == "TAKEOFF":
            TCP_msg = "1"
            client.send(TCP_msg.encode())
            print("Sent:",TCP_msg)
        elif msgName == "TOOKOFF":
            TCP_msg = "2"
            client.send(TCP_msg.encode())
            print("Sent:",TCP_msg)
        elif msgName == "LAND":
            TCP_msg = "3"
            client.send(TCP_msg.encode())
            print("Sent:",TCP_msg)
        elif msgName == "LANDED":
            TCP_msg = "4"
            client.send(TCP_msg.encode())
            print("Sent:",TCP_msg)
        else:
            print("ERROR: Wrong Message Name:", msgName)
    # Rover Drone will need to receive Base's coordinates and keep following it (keep flyToPoint(Base's coordinates))
    def receiveInfo(self, client):
        val = self.protocol.recvMsg(client)
        if(val == None):
            print("Protocol Received None")
            return None
        if(len(val) == 1):
            msgName = val[0]
            print("Received Message", msgName)
            return msgName
        else:
            lat, lon, alt, recvTime = val
            print(lat, lon, alt, recvTime)
            p1 = LocationGlobalRelative(lat,lon,alt)
            
            # print("Current Time:", int(datetime.now().strftime("%S")))
            currentTime = int(datetime.now().strftime("%S"))
        
            ''' If the received data was delayed for less than ___ seconds'''
            if(timeIsValid(curTime=currentTime,recvTime=recvTime)):
                # print("Distance to the received point:",get_distance_metres(p1,self.vehicle.location.global_frame))
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

