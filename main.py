# Fichier pour l'affichage de la fenêtre principale du jeu.

import os
import json
from ezTK import *
# from player import create_player
# from player_creation import create_player_window, open_player_window


class DnDGame:
    def __init__(self):
        self.root = Win(title="Main Menu", width=300, height=200, bg='lightgray')
        Label(self.root, text="Main menu", font="Arial 20 bold")
        # print("class mainMenu - test view player : ", self.display_players())
        Button(self.root, text="Create new Player")#, command=create_player_window)
        players = self.display_players()
        for player in players:
            Button(self.root, text=f"Name: {player['name']}, Level: {player['level']}, Classe: {player['classe']}, Race: {player['race']}",
                command=lambda p=player: open_player_window(p))
        self.root.loop()

    def get_players(self):
        with open('players_database.json', 'r') as f:
            data = json.load(f)
        return data['players']
    
    def display_players(self):
        players = self.get_players()
        print("class mainMenu - display_players : ", players)
        return players
    
    def get_my_player(self, num: int):
        players = self.get_players()
        for player in players:
            if player['id'] == num:
                print("class mainMenu - get_my_player : ", player)
                return player
        return None



def create_database():
    # Sample data
    value = {
        "players": [
            {"id": 1, "name": "cutiiie", "level": 1, "class": "Warrior", "race": "Elf"},
            {"id": 2, "name": "Bob", "level": 2, "class": "Mage", "race": "Human"}
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


if __name__ == "__main__":
    open = DnDGame() # Open the game main menu
    # player_instance = create_player()
    # players = get_players()

    # for player_instance in players:
    #     print(player_instance)

    # # Create the main menu window using ezTK
    # root = Win(title="Main Menu", width=300, height=200, bg='lightgray')

    # # Button to open the player creation page
    # Button(root, text="Create Player", command=create_player_window)

    # # Run the main menu
    # root.loop()


def get_all_data(filename='players_database.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    return data