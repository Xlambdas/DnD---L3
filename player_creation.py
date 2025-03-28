# import tkinter as tk
import json
from ezTK import *
# import sys
# sys.path.append('../ezTK')
# import sys
# sys.path.append('../player')
from player import *


# class show_player(player):
#     def __init__(self, player):
#         super().__init__(title="Player", width=300, height=200)
#         Label(self, text=f"Name: {player['name']}")
#         Label(self, text=f"Level: {player['level']}")

def save_player(name, level):
    data = {"players": []}  # Initialize an empty data structure for players
    print("player creation - : ", data)
    # Read existing data from the JSON file
    with open('game_database.json', 'r') as f:
        data = json.load(f)

    # Generate a new ID for the player
    new_id = max(player['id'] for player in data['players']) + 1 if data['players'] else 1

    # Add the new player to the data
    data['players'].append({"id": new_id, "name": name, "level": level})

    # Write updated data back to the JSON file
    with open('game_database.json', 'w') as f:
        json.dump(data, f, indent=4)

def create_player_window():
    def submit():
        name = name_entry.value
        level = int(level_entry.value)
        save_player(name, level)
        result_label.text = f"Player '{name}' created successfully!"

    # Create the window using ezTK
    window = Win(title="test Create Player", width=300, height=200)

    # Name input
    Label(window, text="Name:")
    name_entry = Entry(window, width=20)

    # Level input
    Label(window, text="Level:")
    level_entry = Entry(window, width=20)

    # Submit button
    Button(window, text="Create Player", command=submit)

    # Result label
    result_label = Label(window, text="")

    # Run the window
    window.loop()


def open_player_window(player):
    print(f"Opening player window for {player['name']}")
    window = Win(title="test Create Player", width=300, height=200)

    # Name input
    Label(window, text=f"Name:{player['name']}")
    Label(window, text=f"Level:{player['level']}")
    Label(window, text=f"ID:{player['id']}")
    Button(window, text="Play", command=lambda: {
        print("play"),
        window.quit(),  # Close the player window
        open_game(player)
    })
    Button(window, text="Close", command=window.quit)  # Close the player window

if __name__ == "__main__":
    create_player_window()


def open_game(player):
    print(f"Opening game for {player['name']}")
    window = Win(title="Game", width=300, height=200)
    Label(window, text=f"Welcome to the game, {player['name']}!")
    Button(window, text="Close", command=window.quit)
    window.loop()