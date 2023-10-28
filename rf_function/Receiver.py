from Transmitter import Transmitter
import time

# TODO: Complete Receiver and put the decoding code in rf/Vehicle.update_by_rf_msg() here
class Receiver(Transmitter):
    def receive(self,gpio,protocol,puslelength,repeat):
        super().__init__(gpio,protocol,puslelength,repeat)
        # TODO: initialize timecode[] variable

    def receiveMsg(self):
        # If timestamp is the same, it means the current message has been read and processed by us
        if self.rfdevice.rx_code_timestamp != timestamp:
            #if(check_pusle_and_protocol(rfdevice) == False):
            #    continue
            timestamp = self.rfdevice.rx_code_timestamp
            msg = self.rfdevice.rx_code
            self.processMsg(msg)
        # if(sleep_or_not): time.sleep(0.01)
    
    def processMsg(self,msg):
        '''
        Args: msg is the original object from rfdevice, no need to turn it to string beforehand.
        Process the msg. type_of_msg: 1 = latitude, 2 = longitude, 3 = time & height 
        (The message is sent with type int, so we can't use 0 as type, or it will be ignored, like 013213 = 13213)
        '''
        # TODO: Complete the timecode check feature
        
        str_msg = str(msg)
        if(not self.msgIsValid(str_msg)):
           print("The received info is not valid")
           return -1

        type_of_msg = int(str_msg[0])
        new_timecode = int(str_msg[1])
        #print("type_of_info: ", type_of_info)
        if(type_of_msg==1):
            lat = self.parseMsg(type_of_msg,str_msg[-8:])
            print("Lat:",lat)
        elif(type_of_msg==2):
            lon = self.parseMsg(type_of_msg,str_msg[-8:])
            print("Lon:",lon)
        elif(type_of_msg==3):
            height, rcvTime = self.parseMsg(type_of_msg,str_msg[-8:])
            print("Height:",height,"Time:",rcvTime)

        # if(check_type(type_of_info) == True):
        #     if(self.timecode[type_of_info-1] != new_timecode):
        #         self.timecode[type_of_info] = new_timecode
        #         file_write("--------START---------")
        #         file_write(str((datetime.datetime.now())))
        #         file_write("Timecode: [" + str(self.timecode[2]) + ", " + str(self.timecode[0]) + ", " + str(self.timecode[1]) + "]")
        #         if(type_of_info == 0):
        #             self.latitude = info_detail(type_of_info, new_info)
        #             file_write("lat: " + str(self.latitude))
        #         elif(type_of_info == 1):
        #             self.longitude = info_detail(type_of_info, new_info)
        #             file_write("lon: " + str(self.longitude))
        #         elif(type_of_info == 2):
        #             self.height, self.time = info_detail(type_of_info, new_info)
        #             file_write("height: " + str(self.height))
        #             file_write("time: " + str(self.time))
        #         file_write("---------END----------")
                
                
        # elif(check_type(type_of_info) == True):
        #     self.timecode[type_of_info] = new_timecode
        #     print("-------VALID----------")
        #     print("Timecode: ", self.timecode)
        #     if(type_of_info == 0):
        #         self.latitude = info_detail(type_of_info, new_info)
        #         print("lat: ", self.latitude)
        #     elif(type_of_info == 1):
        #         self.longitude = info_detail(type_of_info, new_info)
        #         print("lon: ", self.longitude)
        #     elif(type_of_info == 2):
        #         self.height, self.time = info_detail(type_of_info, new_info)
        #         print("time: ", self.time)
        #         print("height: ", self.height)

    def msgIsValid(self, msg):
        '''
        Args: msg is the string format of the original info
        Checks the type and the length of the info
        '''
        msgType = int(msg[0])
        if(msgType > 3 or msgType < 1 or len(msg) > 10):
            return False
        else:
            return True

    def check_type(self, type_of_info):
        if(type_of_info <=2 and type_of_info >= 0):
            return True
        return False

    def parseMsg(self, type_of_msg, msg):
        '''
        Args: type_of_msg is an int: 1 = latitude, 2 = longitude, 3 = height & time. msg is a string of length 8.
        Return: A string of the parsed message
        '''
        if(type_of_msg == 1):
            # Latitude
            return "120." + msg # Restore the original latitude
        elif(type_of_msg == 2):
            # Longitude
            return "24." + msg  # Restore the original longitude
        elif(type_of_msg == 3):
            # Height(5 digit) & Time(3 digit)
            height = msg[:3] + "." + msg[3:5] # Restore the original height
            rcvTime = msg[-3:]
            return height, rcvTime
        

# Test code:
receiver = Receiver(gpio=17, protocol=1, puslelength=200, repeat=10)
receiver.processMsg(1033240000)
receiver.processMsg(2045600780)
receiver.processMsg(3002322857)