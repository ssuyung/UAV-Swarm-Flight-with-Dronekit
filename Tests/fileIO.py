import time
import sys
import math
import socket

sys.path.append("..")
from RepeatTimer import RepeatTimer

def func(f):
    f.write("12345\n")
    print("func")


f = open("test.txt", "w")
f.write("hello")


timer = RepeatTimer(1,func,(f,))

timer.start()
time.sleep(3)
timer.cancel()

time.sleep(1)
f.close()