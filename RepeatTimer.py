from threading import Timer

# A class that will repeatedly execute by the given interval
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

'''
usage: 
timer = RepeatTimer(5, <name of function>)
timer.start()
timer.cancel()
'''