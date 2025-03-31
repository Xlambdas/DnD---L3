# Fichier pour l'affichage de la fenêtre principale du jeu.

import os
import json
from ezTK import *
# from other files :

# from player import create_player
from player_creation import create_player_window, open_player_window
from player import get_player, Player


class DnDGame:
    def __init__(self):
        self.root = None
        # self.root = Win(title="Main Menu", width=300, height=200, bg='lightgray')
        # Label(self.root, text="Main menu", font="Arial 20 bold")
        # # print("class mainMenu - test view player : ", self.display_players())
        # Button(self.root, text="Create new Player", command=create_player_window, bg='lightblue')
        # players = self.display_players()
        # for player in players:
        #     Button(self.root, text=f"Name: {player['name']}, Level: {player['level']}, Classe: {player['classe']}, Race: {player['race']}",command=lambda p=player['name']: open_player_window(p))
        # self.root.loop()

    def get_players(self):
        with open('players_database.json', 'r') as f:
            data = json.load(f)
        return data['players']
    
    def display_players(self):
        players = self.get_players()
        # print("class mainMenu - display_players : ", players)
        return players
    
    def get_my_player(self, num: int):
        players = self.get_players()
        for player in players:
            if player['id'] == num:
                # print("class mainMenu - get_my_player : ", player)
                return player
        return None



def home_page():
    """
        Open the home page for the game. to get or create the player instance.
    """
    root = Win(title="Main Menu", width=300, height=200, bg='lightgray')
    Label(root, text="Main menu", font="Arial 20 bold")
    players = DnDGame().display_players()
    Button(root, text="Create Player", command=create_player_window)
    for player in players:
        Button(root, text=f"Name: {player['name']}, Level: {player['level']}, Classe: {player['classe']}, Race: {player['race']}", command=lambda p=player['name']: open_player_window(p))

    root.loop()



if __name__ == "__main__":
    open = home_page()

    # # Run the main menu
    # root.loop()


