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
                self_vehicle.update_by_rf_msg(info)
            else: sleep_or_not = False
        # if(sleep_or_not): time.sleep(0.01)
    
    def processInfo(self):
        