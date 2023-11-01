import requests

def checkInternetConnection(vehicle):
    url = "https://www.google.com"
    timeout = 10
    try:
        request = requests.get(url, timeout=timeout)
        # print("Connected to the Internet")
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection. Aborting mission")
        vehicle.land()