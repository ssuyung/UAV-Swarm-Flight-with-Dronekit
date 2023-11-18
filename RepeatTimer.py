from threading import Timer

# A class that will repeatedly execute by the given interval
class RepeatTimer(Timer):
    '''
    usage: 
    timer = RepeatTimer(5, <name of function>, (args,))
    timer.start()
    timer.cancel()
    '''
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)



def sendMsg(vehicle, client):
    vehicle.sendInfo(client, "COORDINATES")