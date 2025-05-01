"""
main.py

This script serves as the entry point for the Dungeons and Dragons (DnD) game application.
It initializes the game by creating an instance of the DnDGame class for a specified player.

Modules:
    - game: Contains the DnDGame class which manages the game logic.

Functions:
    - open_game(name): Opens the game for the specified player.

Usage:
    Run this script to start the game.
"""
from ezTK import *
from player import get_all_data
from player_creation import create_player_window, open_player_window


def get_all_players():
    """
        Get all players from the database.
        Returns:
            players: A list of dictionaries representing all players in the database.
    """
    data = get_all_data()
    players = data['players']
    return players


def home_page():
    """
        Open the home page for the game. to get or create the player instance.
    """
    root = Win(title="Main Menu", width=300, height=200, bg='lightgray')
    Label(root, text="Main menu", font="Arial 20 bold")
    players = get_all_players()
    Button(root, text="Create Player", command=lambda: {create_player_window(), root.quit()})
    for player in players:
        Button(root, text=f"Name: {player['name']}, Level: {player['level']}, Classe: {player['classe']}, Race: {player['race']}", command=lambda:{open_player_window(player['name']), root.quit()})
    root.loop()


if __name__ == "__main__":
    open = home_page()


