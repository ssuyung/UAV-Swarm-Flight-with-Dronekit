import requests
from datetime import datetime
def checkInternetConnection(vehicle,file=None):
    url = "https://www.google.com"
    timeout = 10
    try:
        request = requests.get(url, timeout=timeout)
        # print("Connected to the Internet")
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection. Aborting mission")
        if(file): file.write("At time "+datetime.now().strftime("%H%M%S")+" detected loss of connection. Landing!\n")
        vehicle.land()