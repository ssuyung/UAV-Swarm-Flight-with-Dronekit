# import time
# import sys
# import math
# import socket

# sys.path.append("..")
# from RepeatTimer import RepeatTimer

# def func(f):
#     f.write("12345\n")
#     print("func")


# f = open("test.txt", "w")
# f.write("hello")


# timer = RepeatTimer(1,func,(f,))

# timer.start()
# time.sleep(3)
# timer.cancel()

# time.sleep(1)
# f.close()

# a = 0
# x = input("Allow takeoff? y/n ")
# a = 1
# print(a)

# a = "120.2312.342349134.94124.231341232LAND12.231312"
# print(a.find("LAND"))
 
while(input("Allow takeoff? y/n\n") != 'y'): 
    pass

lat = float("24.3294320923")
lon = float("120.31490324")
alt = float("34.23490")

assert(lat <= 90 and lat >= -90)               
assert(lon <= 180 and lon >= -180)             
assert(alt < 100)     
print("hello")