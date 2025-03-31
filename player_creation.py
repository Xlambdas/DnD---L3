# import tkinter as tk
import json
from ezTK import *  # Import all widgets from ezTK
# import sys
# sys.path.append('../ezTK')
# import sys
# sys.path.append('../player')
from player import get_player, create_player
from classe import get_classe, get_all_classe_name
from race import *



# def get_all_race_name ():
#     """
#         Retrieve all race from the dataset.
#         Returns:
#             data: A list representing all races in the dataset.
#     """
#     data = get_all_data()
#     races = data['race']
#     races_name = [races['name'] for races in races]
#     return races_name



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
    """
        Create a new player using a GUI. You need to enter a name and select a class. 
        The race is set to "Human" by default.
        The player is then created and saved in the database.
    """
    def submit():
        # Retrieve values from the input fields
        name = name_entry.get()
        data = get_all_data()
        for player in data['players']:
            # print("player test for : ", player) b
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
        if not classe_entry.curselection():
            alert = Win(title="Alert", width=300, height=100)
            Label(alert, text="Please select a class in the list.", font=("Arial", 12), bg="lightyellow")
            alert.loop()
            return

        player_class = classe_entry.get(classe_entry.curselection())
        player_race = 'Human'


        create_player(name, player_class, player_race)
        result_label.text = f"Player '{name}' created successfully!"
        window.quit()  # todo : close the window after creating the player
        open_player_window(name)  # Open the player window

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

    # Result :
    result_label = Label(window, text="")
    window.loop()


def open_player_window(name):

    window = Win(title="test Create Player", width=300, height=200)
    player = get_player(name)
    print(" player Creation (open_player_window) - player : ", player)
    
    # player = {"player": [theplayer]}
    # # print(f"Opening player window for {player['name']}")
    # print(player)  # Add this line to inspect the player object
    # print(f"Opening player window for {player['name']}")


    # Name input
    Label(window, text=f"Name:{player['name']}")
    Label(window, text=f"Level:{player['level']}")
    Label(window, text=f"ID:{player['id']}")
    Label(window, text=f"Class: {player['classe']}")
    Label(window, text=f"Race: {player['race']}")
    # Label(window, text='caca'f"description: {get_class_by_name(player['classe']).describe()}")
    Button(window, text="Play", command=lambda: {
        print("play"),
        window.quit(),  # Close the player window
        open_game(player)
    })
    # Button(window, text="Close", command=window.quit)  # Close the player window

    # Run the window
    window.loop()

# if __name__ == "__main__":
#     create_player_window()
# if __name__ == "__main__":
#     create_player_window()


def open_game(player):
    # print(f"Opening game for {player['name']}")
    window = Win(title="Game", width=300, height=200)
    Label(window, text=f"Welcome to the game, {player['name'] }!")
    Button(window, text="Close", command=window.quit)
    window.loop()


# --- | Zone de test | ---

# player01 = Classe(playerClass["name"], playerClass["strength"], playerClass["endurance"], playerClass["bonus"])
# print(player01.describe())
# print(player01['Speed'])
# playerinfo = player01.describe()
# print(playerinfo)
# print(player01)
# open_player_window('Mon_enoooorme_chibre')
# test_player = get_player("Shadow_Strike")
# print(test_player)
# create_player_window()

# open_player_window('Mon_enoooorme_chibre')
# print(test_player['players'][0]['name'])
# open_player_window('Mon_enoooorme_chibre')
# open_player_window('Mon_enoooorme_chibre')
# create_player_window()
# create_player("Mon_enoooorme_chibre", "Barbarian", "Elf")
# open_game(test_player)
# open_player_window(test_player['name'])

# open_game(test_player)
# create_player_window()

