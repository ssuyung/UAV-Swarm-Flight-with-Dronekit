from dronekit import connect, VehicleMode, LocationGlobalRelative
import json
import time
import sys
import math
from threading import Timer
from RepeatTimer import RepeatTimer


class Drone(dronekit.Vehicle):
    def __init__(self, connection_string):  
        print("Connect to vehicle on: %s" % connection_string)
        self.vehicle = connect(connection_string, wait_ready=True)
        self.stateCheck=None
        self.stateReportTimer=None

    def preArmCheck(self):
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

    def takeoff(self, aTargetAltitude, goP1, goP2):
        """
        Arms vehicle and fly to aTargetAltitude.
        """

        # print("Basic pre-arm checks")
        # # Don't try to arm until autopilot is ready

        # while not vehicle.is_armable:
        #     if stateCheck == "land":
        #         print("exit vechicle armable check loop...")
        #         return
        #     else:
        #         print(" Waiting for vehicle to initialise...")

        #     time.sleep(1)
        
        # print("Arming motors")
        # # Copter should arm in GUIDED mode
        # vehicle.mode = VehicleMode("GUIDED")
        # vehicle.armed = True

        # # Confirm vehicle armed before attempting to take off
        # while not vehicle.armed:
        #     if stateCheck == "land":
        #         print("exit vechicle armed check loop...")
        #         return
        #     else:
        #         vehicle.mode = VehicleMode("GUIDED")
        #         vehicle.armed = True
        #         print(" Waiting for arming...")
        #     time.sleep(1)

        self.pre_arm_check()

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

    # TODO: turn the argument to a LocationGlobalRelative object
    def flyToPoint(self,lat,lon,alt):
        point1 = LocationGlobalRelative(float(lat), float(lon), float(alt))
        print("Target Point: ({:12.8f},{:12.8f},{:5.2f})".format(float(lat),float(lon),float(alt)))

        targetDistance = get_distance_metres(self.vehicle.location.global_relative_frame, point1)
        print("Target distance: ",str(targetDistance))

        self.vehicle.simple_goto(point1)
        print("Executed simple_goto()")

        while self.vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
            remainingDistance=get_distance_metres(self.vehicle.location.global_relative_frame, point1)
            print("Distance to target: ", remainingDistance)
            if remainingDistance<=1: #Just below target, in case of undershoot.
                print("Reached target")
                break
            elif self.stateCheck == "land":
                print("exit distance check loop...")
                return

            time.sleep(1)

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
    
    def setStateReport(self, freq):
        self.stateReportTimer = RepeatTimer(5, self.getState)
        self.stateReportTimer.start()
    
    def cancelStateReport(self):
        if(self.stateReportTimer):
            self.stateReportTimer.cancel()
 





def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles.
    """
    dlat = float(aLocation2.lat) - float(aLocation1.lat)
    dlong = float(aLocation2.lon) - float(aLocation1.lon)
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

