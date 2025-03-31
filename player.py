import json
import os
from ezTK import *
#from other files :
from race import get_race, get_all_data, Race
from classe import get_classe, Classe
# from player_creation import create_player_window

class Player ():
    def __init__(self, name, classe, race):
        """
            require :
                - name : str : name of the player
                - classe : str : class of the player (in a predetermined list)
                - race : str : race of the player (by default = Human)
            Ensures : get all the information about the player in the database.
        """
        self.name = name
        self.classe = classe
        self.race = race
        playerRace = get_race(race)
        self.race = Race(playerRace['name'], playerRace['base_health'], playerRace['bonus'])
        playerClass = get_classe(classe)
        self.classe = Classe(playerClass["name"], playerClass["strength"], playerClass["endurance"], playerClass["bonus"])
        print("test race : ", self.race.describe())
        print("test class : ", self.classe.describe())


    def to_dict(self):
        return {"id":0, "name": self.name, "level": 1, "classe": self.classe, "race": self.race}
    
    def descr(self):
        return {"name": self.name, "level": 1, "classe": self.classe, "race": self.race}


def get_player(name):
    """
        Get all the data concerning the player from the database.
        required : name : str : name of the player.
        Ensures : New player in the database if the name is not already used.
    """
    data = get_all_data()
    for player in data['players']:
        if player['name'] == name:
            return player
    if not name in data['players']:
        print("You can't use this name, it is already used...")
        return {}
    return data['players']

def create_player(name: str, classe: str, race: str): # todo : not so usefull !! only used in player_creation.py (creation_player_window())
    """
        Create a new player and save it in the database.
        required :
            - name : str : name of the player
            - classe : str : class of the player (in a predetermined list)
            - race : str : race  of the player (by default = Human)
        Ensures : New player in the database if the name is not already used.
    """
    data = get_all_data()
    data_players = data['players']

    exist_names = [player["name"] for player in data_players] # check if the name already exists

    if name in exist_names:
        print("You can't use this name, it is already used...")
        return False #create_player_window()

    data_players.append({"id": 0, "name": name, "level": 1, "classe": classe, "race": race, "health": 100, "mana": 100, "inventory": [], "xp": 0})
    data ["players"]= data_players #{"players": data_players}
    # print("data_players",data_players)
    # print("test data : ", data_player)

    with open('players_database.json', 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Player {name} added successfully!")

    return get_player(name)


def delete_player(name):
        """Supprime un joueur en fonction de son nom."""
        data = get_all_data()
        # print("data",data)
        # data_player = {"players": data.get("players", [])}

        #  = get_players(name)
        # print("current players",data)

        # Filtrer les joueurs à garder
        new_players = [p for p in data["players"] if p["name"] != name]
        # print("new_players",new_players)
        # print(len(new_players), len(data["players"]))
        # Si aucun joueur n'a été supprimé, le nom n'existe pas


        if len(new_players) == len(data["players"]):
            print(f"❌ Player {name} not found.")
            return False

        # Sauvegarde les nouveaux joueurs
        data["players"] = new_players
        # print("all_data players",data["players"])
        # all_data["players"] = data["players"]
        # print("all_data",all_data)
        # data = all_data
        with open('players_database.json', 'w') as f:
            json.dump(data, f, indent=4)
        # Sauvegarde les données
        print(f"✅ Player {name} deleted successfully!")
        return True

# player1 = Player(8, "Mon_enoooorme_chibre", 50, "Warrior", "Elf")
# player2 = Player(3, "Mamdre", 50, "Warrior", "Elf")

# print("get_players",get_players('game_database.json'))
# player2.create_player()
# delete_player("Mon_big_chibre")


# def create_player_window():
#     def submit():
#         name = name_entry.value
#         player_class = class_entry.value
#         player_race = race_entry.value
#         create_player(name, player_class, player_race)
#         result_label.text = f"Player '{name}' created successfully!"

#     # Create the window using ezTK
#     window = Win(title="Create Player", width=300, height=300)

#     # Name input
#     Label(window, text="Name:")
#     name_entry = Entry(window, width=20)

#     # Level input
#     Label(window, text="Level:")
#     level_entry = Entry(window, width=20)

#     # Class input
#     Label(window, text="Class:")
#     class_entry = Entry(window, width=20)

#     # Race input
#     Label(window, text="Race:")
#     race_entry = Entry(window, width=20)

#     # Submit button
#     Button(window, text="Create Player", command=submit)

#     # Result label
#     result_label = Label(window, text="")

#     # Run the window
#     window.loop()



# # print("test create player : ", create_player("testme", "Warrior", "Elf"))

# # print ("test del player : ", delete_player("testme"))


# # player = get_player("test_name")
# # testPlayer = Player(player['name'], player['classe'], player['race'])

# # print("show current player : ", testPlayer.descr())


# create_player_window()