import json
import requests

# https://app.abstractapi.com/users/signup?target=/api/ip-geolocation/pricing/select

def coordinates(ip):
    # Your API key, available from your account page
    YOUR_GEOLOCATION_KEY = open("key.txt","r").read()

    # IP address to test
    ip_address = ip

    response = requests.get('https://ipgeolocation.abstractapi.com/v1/?api_key=' + YOUR_GEOLOCATION_KEY + '&ip_address=' + ip_address)
    latitude = json.loads(response.content)['latitude']
    longitude = json.loads(response.content)['longitude']
    return longitude, latitude

# Test:

# lat, long = coordinates('142.251.209.14')
# print("latitude:", lat)
# print("longitude:", long)