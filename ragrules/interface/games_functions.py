import json
import os


# Load the JSON data
def load_games():
    games = []
    with open('./ragrules/interface/datas/board_games.json') as f:
        for line in f:
            games.append(json.loads(line))
    return games

# Function to search for games
def search_games(games, query):
    return [game for game in games if query.lower() in game['name'].lower()]
