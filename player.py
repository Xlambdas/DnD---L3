import json
import os
from ezTK import *
#from other files :
from race import get_all_data, Race
from classe import Classe

class Player ():
    def __init__(self, name):
        """
            require :
                - name : str : name of the player
                - classe : str : class of the player (in a predetermined list)
                - race : str : race of the player (by default = Human)
            Ensures : get all the information about the player in the database.
        """
        self.name = name
        info_player = self.get_bdd()
        self.race = info_player['race']
        self.classe = info_player['classe']
        self.xp = info_player['xp']
        self.info_race = Race(self.race)
        self.info_classe = Classe(self.classe)
        self.actions = 2

    def descr(self):
        return {"name": self.name, "level": 1, "classe": self.classe, "race": self.race}

    def get_bdd(self):
        """
            Get all the data concerning the player from the database.
            required : name : str : name of the player.
            Ensures : get all the infos about the current player from the database.
        """
        data = get_all_data()
        # print("class player - data :",data)
        for player in data['players']:
            if player['name'] == self.name:
                return player
        if not self.name in data['players']:
            print("You can't play, the name enter is not in the Database...")
            return {}
        return data['players']

    def set_bdd(self): # todo -
        """
            Set all the data concerning the player in the database.
            required : name : str : name of the player.
            Ensures : set all the infos about the current player in the database.
        """
        pass

    def action(self, type):
        """
            Perform an action based on the type of action.
            required : type : str : type of action (attack, heal, etc.)
            Ensures : perform the action and return the result.
        """
        if self.actions <= 0:
            print("No actions left.")
            return None
        self.actions -= 1
        if type == "attack":
            return self.attack()
        elif type == "mouv":
            return self.mouv()
        else:
            print("Unknown action type.")
            return None

    def attack(self):
        """
            Calculate the attack bonus of the player.
            Ensures : return the attack bonus of the player.
        """
        # base_attack = 10
        print ("file player - attack")
        pass

    def mouv(self):
        """
            Calculate the movement of the player.
            Ensures : return the movement of the player.
        """
        print("file player - mouv")
        pass


# --- | brouillon | -----------------------------------------------





# # print("test create player : ", create_player("testme", "Warrior", "Elf"))

# # print ("test del player : ", delete_player("testme"))


# # player = get_player("test_name")
# # testPlayer = Player(player['name'], player['classe'], player['race'])

# # print("show current player : ", testPlayer.descr())


# # create_player_window()
# plyer = Player("zdc")
# # plyer.get_player()
# print("show current player : ", plyer.descr())







# def save_player(name, level, player_class, player_race):
#     data = {"players": []}  # Initialize an empty data structure for players
#     print("player creation - : ", data)
#     # Read existing data from the JSON file
#     with open('game_database.json', 'r') as f:
#         data = json.load(f)

#     # Generate a new ID for the player
#     new_id = max(player['id'] for player in data['players']) + 1 if data['players'] else 1

#     # Add the new player to the data
#     data['players'].append({
#         "id": new_id,
#         "name": name,
#         "level": level,
#         "classe": player_class,
#         "race": player_race
#     })

#     # Write updated data back to the JSON file
#     with open('game_database.json', 'w') as f:
#         json.dump(data, f, indent=4)





# def delete_player(name):
#         """Supprime un joueur en fonction de son nom."""
#         data = get_all_data()
#         # print("data",data)
#         # data_player = {"players": data.get("players", [])}

#         #  = get_players(name)
#         # print("current players",data)

#         # Filtrer les joueurs à garder
#         new_players = [p for p in data["players"] if p["name"] != name]
#         # print("new_players",new_players)
#         # print(len(new_players), len(data["players"]))
#         # Si aucun joueur n'a été supprimé, le nom n'existe pas


#         if len(new_players) == len(data["players"]):
#             print(f"❌ Player {name} not found.")
#             return False

#         # Sauvegarde les nouveaux joueurs
#         data["players"] = new_players
#         # print("all_data players",data["players"])
#         # all_data["players"] = data["players"]
#         # print("all_data",all_data)
#         # data = all_data
#         with open('players_database.json', 'w') as f:
#             json.dump(data, f, indent=4)
#         # Sauvegarde les données
#         print(f"✅ Player {name} deleted successfully!")
#         return True

# --- | Zone de test | ---
