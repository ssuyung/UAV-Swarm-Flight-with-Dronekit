from Transmitter import Transmitter
import time

# TODO: Complete Receiver and put the decoding code in rf/Vehicle.update_by_rf_msg() here
class Receiver(Transmitter):
    def receive(self,gpio,protocol,puslelength,repeat):
        super().__init__(gpio,protocol,puslelength,repeat)

    def receiveInfo(self):
        sleep_or_not = True
        if self.rfdevice.rx_code_timestamp != timestamp:
            #if(check_pusle_and_protocol(rfdevice) == False):
            #    continue
            timestamp = self.rfdevice.rx_code_timestamp
            info = self.rfdevice.rx_code
            str_info = str(info)
            if((str_info[0] == "1" and len(str_info) <= 10) or (str_info[0] == "2" and len(str_info) <= 10) or (str_info[0] == "3" and len(str_info) <= 9)):
                self.processInfo(info)
            else: sleep_or_not = False
        # if(sleep_or_not): time.sleep(0.01)
    
    def processInfo(self,info):
        str_info = str(info)
        if(len(str_info) < 8): return
        type_of_info = int(str_info[0]) - 1
        new_timecode = int(str_info[1])
        new_info = int(str_info[2:])
        #print("type_of_info: ", type_of_info)
        if(check_type(type_of_info) == True and valid[type_of_info] == True):
            if(self.timecode[type_of_info] != new_timecode):
                self.timecode[type_of_info] = new_timecode
                file_write("--------START---------")
                file_write(str((datetime.datetime.now())))
                file_write("Timecode: [" + str(self.timecode[2]) + ", " + str(self.timecode[0]) + ", " + str(self.timecode[1]) + "]")
                if(type_of_info == 0):
                    self.latitude = info_detail(type_of_info, new_info)
                    file_write("lat: " + str(self.latitude))
                elif(type_of_info == 1):
                    self.longitude = info_detail(type_of_info, new_info)
                    file_write("lon: " + str(self.longitude))
                elif(type_of_info == 2):
                    self.height, self.time = info_detail(type_of_info, new_info)
                    file_write("height: " + str(self.height))
                    file_write("time: " + str(self.time))
                file_write("---------END----------")
                
                
        elif(check_type(type_of_info) == True):
            self.timecode[type_of_info] = new_timecode
            valid[type_of_info] = True
            print("-------VALID----------")
            print("Timecode: ", self.timecode)
            if(type_of_info == 0):
                self.latitude = info_detail(type_of_info, new_info)
                print("lat: ", self.latitude)
            elif(type_of_info == 1):
                self.longitude = info_detail(type_of_info, new_info)
                print("lon: ", self.longitude)
            elif(type_of_info == 2):
                self.height, self.time = info_detail(type_of_info, new_info)
                print("time: ", self.time)
                print("height: ", self.height)