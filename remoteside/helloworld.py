import requests
while True:print(requests.get("http://192.168.9.115:5000/control").content)