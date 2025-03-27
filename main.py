# Fichier pour l'affichage de la fenêtre principale du jeu.

import tkinter as tk
import json
from player import *

def create_database():
    # Sample data
    value = {
        "players": [
            {"id": 1, "name": "cutiiie", "level": 1},
            {"id": 2, "name": "Bob", "level": 2}
        ]
    }

    # Write data to a JSON file
    with open('game_database.json', 'w') as f:
        json.dump(value, f, indent=4)


def get_players():
    # Read data from the JSON file
    with open('game_database.json', 'r') as f:
        data = json.load(f)

    return data['players']

# Example usage of get_players function
if __name__ == "__main__":
    # player_instance = create_player()
    players = get_players()

    for player_instance in players:
        print(player_instance)
