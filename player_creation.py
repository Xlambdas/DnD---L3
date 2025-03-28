# import tkinter as tk
import json
from ezTK import *
# import sys
# sys.path.append('../ezTK')
# import sys
# sys.path.append('../player')
from player import *
from classe import *
from race import *


def save_player(name, level, player_class, player_race):
    data = {"players": []}  # Initialize an empty data structure for players
    print("player creation - : ", data)
    # Read existing data from the JSON file
    with open('game_database.json', 'r') as f:
        data = json.load(f)

    # Generate a new ID for the player
    new_id = max(player['id'] for player in data['players']) + 1 if data['players'] else 1

    # Add the new player to the data
    data['players'].append({
        "id": new_id,
        "name": name,
        "level": level,
        "classe": player_class,
        "race": player_race
    })

    # Write updated data back to the JSON file
    with open('game_database.json', 'w') as f:
        json.dump(data, f, indent=4)

def create_player_window():
    def submit():
        name = name_entry.value
        level = int(level_entry.value)
        player_class = class_entry.value
        player_race = race_entry.value
        save_player(name, level, player_class, player_race)
        result_label.text = f"Player '{name}' created successfully!"

    # Create the window using ezTK
    window = Win(title="Create Player", width=300, height=300)

    # Name input
    Label(window, text="Name:")
    name_entry = Entry(window, width=20)

    # Level input
    Label(window, text="Level:")
    level_entry = Entry(window, width=20)

    # Class input
    Label(window, text="Class:")
    class_entry = Entry(window, width=20)

    # Race input
    Label(window, text="Race:")
    race_entry = Entry(window, width=20)

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
    Label(window, text=f"Class: {player['classe']}")
    Label(window, text=f"Race: {player['race']}")
    Label(window, text=f"description: {get_class_by_name(player['classe']).describe()}")
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