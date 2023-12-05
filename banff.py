import requests
import http.client
import json
import os


client_id = os.getenv('CBC_CLIENT_ID')
client_secret=os.getenv('CBC_CLIENT_SECRET')

banff = {'latitude': 51.18, 'longitude': -115.57, 'intellicastId': 'CAXX0023', 'displayName': 'Banff', 'wxStationIcao': 'CYBW', 'postalCodes': []}
url = "https://as.cbcrc.ca/connect/token"
client_id = "cbc-fast.cbcrc.ca"
client_secret = "5dc05330-887b-4e57-ab53-927465fbbd7c"
audience = "https://as.cbcrc.ca/connect/authorize"


data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "audience": audience
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

try:
   client_id = os.environ["CBC_CLIENT_ID"]
except KeyError:
    client_id = "Token not available!"
    # or raise an error if it's not available so that the workflow fails

try:
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        for cities in access_token: 
            print()
        print("Access Token:", access_token)
    else:
        print(f"Token Request Failed with Status Code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print("An error occurred:", e)

hourly_forecast = " https://cbcrc.azure-api.net/it/Weather-Consolidator/api/v2/en/metric/hourly-forecast/"

# Define headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}


try:
    response = requests.get("https://cbcrc.azure-api.net/it/Weather-Consolidator/api/v2/en/metric/hourly-forecast/CAXX0023?numberofhours=12", headers=headers)
    if response.status_code == 200:
        api_data = response.json()
        print("API Response:", api_data)
    else:
        print(f"API Request Failed with Status Code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print("An error occurred:", e)

with open("banff.json", "w") as f:
    f.write(json.dumps(api_data))
