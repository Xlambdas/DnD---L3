import json
import os
from ezTK import *
#from other files :
from main import get_all_data
from race import get_race, Race
from classe import get_classe, Classe
# from player_creation import create_player_window

class Player ():
    def __init__(self, name, classe, race):
        self.name = name
        self.classe = classe
        # self.race = race
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
    """
    data = get_all_data()
    for player in data['players']:
        # print("player test for : ", player)
        if player['name'] == name:
            return player
    return data['player']


def create_player(name: str, classe: str, race: str):
    """
        Create a new player and save it in the database.
    """
    data = get_all_data()
    data_players = data['players']
    # print("data_players",data_player)

    # Vérifie si le nom existe déjà
    exist_names = [player["name"] for player in data_players]
    # print("existing_names",exist_names)

    if name in exist_names:
        print("You can't use this name, it is already used...")
        return create_player_window()

    data_players.append({"id": 0, "name": name, "level": 1, "classe": classe, "race": race, "health": 100, "mana": 100, "inventory": [], "xp": 0})
    # print("test data : ", data_player)

    with open('players_database.json', 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Player {name} added successfully!")

    return get_player(name)


def delete_player(name):
        """Supprime un joueur en fonction de son nom."""
        data = get_all_data()
        data_player = {"players": data.get("players", [])}

        #  = get_players(name)
        # print("current players",data)

        # Filtrer les joueurs à garder
        new_players = [p for p in data["players"] if p["name"] != name]
        print("new_players",new_players)
        print(len(new_players), len(all_data["players"]))
        # Si aucun joueur n'a été supprimé, le nom n'existe pas


        if len(new_players) == len(data["players"]):
            print(f"❌ Player {name} not found.")
            return False

        # Sauvegarde les nouveaux joueurs
        data["players"] = new_players
        print("all_data players",data["players"])
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
delete_player("Mon_big_chibre")
