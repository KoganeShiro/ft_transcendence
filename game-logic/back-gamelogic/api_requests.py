import requests
import os

API_KEY = os.environ.get('API_KEY')


url = "http://back-end:8000/api/games/pong/"
url2 = "http://back-end:8000/api/profile/gkubina/"
url3 = "http://back-end:8000/api/stats_increment/gkubina/"

headers = {
    "X-API-KEY": os.environ.get('API_KEY')
}


def game_data():
    return {
        "player1_score": 10,
        "player2_score": 5,
      #  "rank_player1_begin": 10,
      #  "rank_player2_begin": 10,
        "rank_player1_change": -10,
        "rank_player2_change": 10,
        "type": "solo",
        "player1": 1,  # Assuming user ID 1
        "player2": 2,  # Assuming user ID 2
        "winner": 3,
        "loser": 2
    }


def prog_data():
    return {
        "stat_pong_solo_rank": -10,
        "stat_pong_solo_progress": -10
    }



response = requests.get(url2, headers=headers)

print ("ID of the user: ", response.json().get('id'))

# response = requests.get(url, headers=headers)

if response.status_code >= 200:
    print("Return: ", response.status_code , response.json())

gamedata = game_data()
gamedata["player1"] = response.json().get('id')
print (gamedata)

response = requests.post(url, headers=headers, json=gamedata)


# response = requests.get(url, headers=headers)

if response.status_code >= 200:
    print("Return: ", response.status_code , response.json())

response = requests.patch(url3, headers=headers, json=prog_data())


# response = requests.get(url, headers=headers)

if response.status_code >= 200:
    print("Return: ", response.status_code , response.json())



