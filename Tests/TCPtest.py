
import time
import sys
import math
import socket

sys.path.append("..")







if(sys.argv[1] == "base"):
    print("=====BASE=====")
    ''' Setting up server '''
    # ip = "172.20.10.8"
    ip = sys.argv[2]
    port = int(sys.argv[3])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(5)
    client, address = server.accept()
    print("Base Connection established")
    
    counter = 0
    
    TCP_msg = str(counter)
    client.send(TCP_msg.encode())
    counter = counter + 1
    time.sleep(2)

    while(1):
        msg = client.recv(10)
        if not msg:
            print("Base leaving")
            break
        print(msg.decode())
    client.close()

elif(sys.argv[1] == "rover"):
    print("=====ROVER=====")

    ''' Setting up client '''
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ip = "172.20.10.8"
    ip = sys.argv[2]
    port = int(sys.argv[3])
    client.connect((ip,port))
    print("Rover Connection Established")
    # client.send("this is rover".encode())
    msg = client.recv(20)
    if(msg):
        str_msg = msg.decode()
        print("Received:",str_msg)
    else:
        print("end of connection")

    time.sleep(1)
    client.send("end".encode())

    client.close()

        
    


else:
    print("Please specify which drone it is")