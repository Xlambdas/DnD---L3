"""
main.py

This script serves as the entry point for the Dungeons and Dragons (DnD) game application.
It initializes the game by creating an instance of the DnDGame class for a specified player.

Modules:
    - game: Contains the DnDGame class which manages the game logic.

Functions:
    - open_game(name): Opens the game for the specified player.

Usage:
    Run this script to start the game for a player.
"""
from game import DNDGame

def open_game(name):
    """
        Open the game for the selected player.
    """
    print(f"Opening game for {name}")
    game = DNDGame(name)


if __name__ == "__main__":
    open_game("fg")
