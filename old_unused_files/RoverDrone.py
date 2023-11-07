from dronekit import connect, VehicleMode, LocationGlobalRelative
import json
import time
import sys
import math
from threading import Timer
from RepeatTimer import RepeatTimer
from Drone import Drone
from rf_function.Receiver import Receiver

from uav import get_distance_metres, flyToPoint, watchstate
from rf_function.rf import Receiver
from rf_function.rf import Vehicle
from rf_function.rf import exithandler

# TODO: complete RoverDrone class
class RoverDrone(Drone):
    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.receiver = Receiver(gpio=27, protocol=1, puslelength=200, repeat=3)
    
    def startReceiver(self):
        self.receiver.start()

    def endReceiver(self):
        self.receiver.end()

    def receiveMsg(self):
        self.receiver.receiveMsg()