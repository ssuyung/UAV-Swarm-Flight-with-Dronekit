# from dronekit import connect, VehicleMode, LocationGlobalRelative
import dronekit
from Drone import Drone
import time

# connection_string = "/dev/ttyACM0"
connection_string = "/dev/tty.usbmodem14101"

vehicle = Drone(connection_string)
vehicle.setStateReport(1)

vehicle.takeoff(0.5)
time.sleep(2)
print("trying to land")
vehicle.land()
# vehicle.