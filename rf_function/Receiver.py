from Transmitter import Transmitter


# TODO: Complete Receiver and put the decoding code in rf/Vehicle.update_by_rf_msg() here
class Receiver(Transmitter):
    def receive(self,gpio,protocol,puslelength,repeat):
        super().__init__(gpio,protocol,puslelength,repeat)

         