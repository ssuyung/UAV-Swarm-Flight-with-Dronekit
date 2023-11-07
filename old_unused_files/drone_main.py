# from dronekit import connect, VehicleMode, LocationGlobalRelative
import dronekit
from Drone import Drone
import time

# connection_string = "/dev/ttyACM0"
connection_string = "/dev/tty.usbmodem14101"

vehicle = Drone(connection_string)

vehicle.setStateReport(1)
# vehicle.setStateReport(4)   # This should output message saying that there's already a state report
# vehicle.cancelStateReport()
# vehicle.cancelStateReport() # This should output message saying that there's no state report timer

point = dronekit.LocationGlobalRelative(24.7948542,120.9922114,1.5)
vehicle.flyToPoint(point)
# vehicle.takeoff(0.5)
# time.sleep(2)
# vehicle.land()