# UAV-Group-Flight-with-Dronekit
## Overview
This project aimed to let multiple drones fly in a swarm automatically without human intervention by letting the drones communicate with one another. Further details as follows:
- Dronekit-Python library to operate the drone
- Raspberry Pi to run our code and to operate the Pixhawk flight control module
- TCP for inter-drone communication
- A protocol to ensure no collision during takeoff and landing

In this project, one or more follower drones will follow a leader drone. The follower drones were also called 'Rover' while the leader drone was called 'Base', so don't get confused with the terms. 

## Results
Three-Drone Test: https://youtu.be/NcuFfFzCNVQ  
Two-Drone Test: https://youtu.be/KIwTaWVTxkw

to be updated

## Protocol
to be updated

## Installation
First, install the Dronekit-Python library with instructions in the [Quickstart](https://dronekit-python.readthedocs.io/en/latest/guide/quick_start.html) page.

Then, clone our repo and the examples are in [/Tests](/Tests). Directly run them with `python3 <filename.py>`.

## Files
### Safety Measure: Emergency Landing
If any bug occurs that leads to a hang in the air or an unknown behavior, run [land.py](land.py) to immediately land the vehicle!
### Packages
- Drone.py: A class that contains basically all the needed functions to operate a drone.
- Internet.py: Contains a function that will check the internet connection, and if the connection to google.com is lost, it will land the drone immediately. This feature exists because we communicate with the Raspberry Pi's on the drones via SSH, hence if the internet connection with the Raspberry Pi is lost, the drone is out of control, so we need to land the drone should this happen.
- RepeatTime.py: Contains a class that will create a thread which will periodically execute a designated function. It is used to periodically return the status of the drone (Drone.setStateReport) and check the internet connection (Internet.py)
- Protocol.py: A class to allow the TCP communication between a Base and a Rover.

### Examples & Tests
The files in the [Tests](/Tests) directory are the on-site tests we conducted before executing the final swarm flight mission to check every feature. The final missions are [7_advancedFollow.py](https://github.com/ssuyung/UAV-Swarm-Flight-with-Dronekit/blob/main/Tests/7_advancedFollow.py) for a two-drone scenario and [8_twoRoverFollow.py](https://github.com/ssuyung/UAV-Swarm-Flight-with-Dronekit/blob/main/Tests/8_twoRoverFollow.py) for a three-drone senario. More drones are applicable and can be implemented in similar ways. The following lists the pre-mission tests, which can be ignored if one considers them unnecessary:
1. setStateReport: Set up the State Report that periodically returns the status of the drone.
2. checkConnectionTimer: Set up a Connection Checking Timer so that if the connection to google.com is lost, it will automatically land the drone. 
3. takeoffAndLand: Let the drone to takeoff and land to see if it is physically able to fly.
4. TCPTransmission: Test the communication between a pair of Base and Rover.
5. simpleFollow: Fly the Base in our hand and see if the Rover will actually follow.
6. checkTakeoffSequence: Test if the drones will takeoff and land according to our protocol. Test 6-1 is for three-drone scenario and test 6 is for two-drone scenario.


## References
Some code for the operation of the drones in Drone.py are from Dronekit-Python [examples](https://dronekit-python.readthedocs.io/en/latest/examples/index.html).

## Authors
This project was implemented by LI Yenku and YEH Ssuyung. 
