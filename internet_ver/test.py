import requests
url = "http://www.kite.com"
url = "https://www.google.com"
timeout = 1
try:
	request = requests.get(url, timeout=timeout)
	print("Connected to the Internet")
except (requests.ConnectionError, requests.Timeout) as exception:
	print("No internet connection.")