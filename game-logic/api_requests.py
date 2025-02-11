import requests
import os

API_KEY = os.environ.get('API_KEY')


url = "http://back-end:8000/api/games/pong/"

headers = {
    "X-API-KEY": os.environ.get('API_KEY')
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Authenticated successfully!", response.json())
else:
    print("Authentication failed:", response.status_code, response.text)