import json
import os
from ezTK import *

# from other files :
from classe import get_all_classe_name
from race import get_all_data
from main import open_game


def open_player_window(name):
    """
        Open the player window for the selected player.
    """
    data = get_all_data()
    players_info = data['players']
    player = next((p for p in players_info if p['name'] == name), None)
    if not player:
        return print(f"Player '{name}' not found.")
    print("file : player_creation - player_info : ", player['name'])

    window = Win(title="Player Info", width=300, height=200)
    Label(window, text=f"Welcome to the game, {name}!", font=("Arial", 16), bg="lightblue")
    Label(window, text=f"Name: {player['name']} \n Classe: {player['classe']} \n {player['race']} \n xp: {player['xp']}")
    Button(window, text="Play", command=lambda: {open_game(name)})
    window.loop()

def create_player_window():
    """
        Create a new player using a GUI. You need to enter a name and select a class.
        The race is set to "Human" by default.
        The player is then created and saved in the database.
    """
    def submit():
        print("create player window - submit")
        name = name_entry.get()
        data = get_all_data()
        data_players = data['players']
        if not classe_entry.curselection():
            alert = Win(title="Alert", width=300, height=100)
            Label(alert, text="Please select a class in the list.", font=("Arial", 12), bg="lightyellow")
            alert.loop()
            return
        for player in data_players:
            # print("player test for : ", player)
            if player['name'] == name:
                alert = Win(title="Alert", width=300, height=100)
                Label(alert, text="This name already exists. Please choose another one.", font=("Arial", 12), bg="lightyellow")
                alert.loop()
                return
        if not name:
            alert = Win(title="Alert", width=300, height=100)
            Label(alert, text="Please enter a valid name.", font=("Arial", 12), bg="lightyellow")
            alert.loop()
            return

        player_classe = classe_entry.get(classe_entry.curselection())
        data_players.append({"name": name, "level": 1, "classe": player_classe, "race": 'Human', "health": 100, "mana": 100, "inventory": [], "xp": 0})
        data ["players"]= data_players
        with open('players_database.json', 'w') as f:
            json.dump(data, f, indent=4)
            print(f"Player {name} added successfully!")
        open_game(name)


    # Create the window for the player creation :
    window = Win(title="Create Player", width=500, height=400)
    Label(window, text="Create your Player", font=("Arial", 16), bg="lightblue")
    Label(window, text="Choose your Name:")
    name_entry = Entry(window, width=20)
    Label(window, text="Choose your Class:")
    classe_entry = Listbox(window, width=20, height=5, scroll=True)

    for item in get_all_classe_name():
        classe_entry.insert('end', item)

    Button(window, text="Create Player", command=submit)
    window.loop()

# ---------------------------------------------------






# --- | brouillon | -----------------------------------------------

# --- | Zone de test | ---

# open_player_window('fg')
# create_player_window()