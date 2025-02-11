import os
import requests
import pytest
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Base URL of the backend API
BASE_URL = "http://back-end:8000/api/games/pong/"

# API Key from environment variable
HEADERS = {
    "X-API-KEY": os.getenv("API_KEY"),
    "Content-Type": "application/json"
}

def log_request_response(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        logger.debug(f"Request URL: {response.request.url}")
        logger.debug(f"Request Headers: {response.request.headers}")
        logger.debug(f"Request Body: {response.request.body}")
        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Body: {response.json()}")
        return response
    return wrapper

requests.post = log_request_response(requests.post)

@pytest.fixture
def game_data():
    return {
        "player1_score": 10,
        "player2_score": 5,
        "rank_player1_begin": 10,
        "rank_player2_begin": 10,
        "rank_player1_change": 10,
        "rank_player2_change": -10,
        "type": "friendly",
        "player1": 1,  # Assuming user ID 1
        "player2": 2,  # Assuming user ID 2
        "winner": 1,
        "loser": 2
    }

# Test POST request to create a new game
@pytest.mark.dependency()
def test_create_game(game_data):
    logger.debug(f"Game data: {game_data}")
    response = requests.post(BASE_URL, json=game_data, headers=HEADERS)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    assert "id" in response.json(), "Response does not contain 'id'"
    game_id = response.json()["id"]
    logger.debug(f"Game ID: {game_id}")
    return game_id

@pytest.fixture
def test_get_game(created_game_id):
    game_id = created_game_id  # Retrieve game ID from POST test

# Test GET request to retrieve game details
@pytest.mark.dependency(depends=["test_create_game"])
def test_get_game():
    game_id = test_create_game(None)  # Retrieve game ID from POST test
    response = requests.get(f"{BASE_URL}{game_id}/", headers=HEADERS)
    logger.debug(f"Request URL: {BASE_URL}{game_id}/")
    logger.debug(f"Request Headers: {HEADERS}")
    logger.debug(f"Response Status Code: {response.status_code}")
    logger.debug(f"Response Body: {response.json()}")
def test_update_game(created_game_id):
    game_id = created_game_id  # Retrieve game ID from POST test

# Test PATCH request to update game scores
@pytest.mark.dependency(depends=["test_create_game"])
def test_update_game():
    game_id = test_create_game(None)  # Retrieve game ID from POST test
    update_data = {"player1_score": 15, "player2_score": 10}
    response = requests.patch(f"{BASE_URL}{game_id}/", json=update_data, headers=HEADERS)
    logger.debug(f"Request URL: {BASE_URL}{game_id}/")
    logger.debug(f"Request Headers: {HEADERS}")
    logger.debug(f"Request Body: {update_data}")
    logger.debug(f"Response Status Code: {response.status_code}")
    logger.debug(f"Response Body: {response.json()}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json()["player1_score"] == 15
    assert response.json()["player2_score"] == 10
