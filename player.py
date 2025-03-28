import json
import os
from main import get_all_data

class Player ():
    def __init__(self, id, name, level, classe, race):
        self.id = id
        self.name = name
        self.level = level
        self.classe = classe
        self.race = race

    def to_dict(self):
        return {"id": self.id, "name": self.name, "level": self.level, "classe": self.classe, "race": self.race}

    def create_player(self, filename='players_database.json'):
        # Vérifie si le fichier existe et lit les données existantes
        data = get_players(self.name)
        print("current players",data)
        
        # Vérifie si le nom existe déjà
        existing_names = [player["name"] for player in data["players"]]
        print("existing_names",existing_names)

        if self.name in existing_names:
            print("Sorry, name already used")
            return False  # Évite d'aller plus loin si le nom existe déjà
    
        # Ajoute le joueur et sauvegarde
        all_data = get_all_data()
        data["players"].append(self.to_dict())
        print("data",data)
        all_data["players"] = data["players"]
        data = all_data
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Player {self.name} added successfully!")
        return True  # Indique que le joueur a bien été ajouté

    
def get_players(name):
    data = get_all_data()
    if "players" in data:
        for player in data["players"]:
            if player["name"] == name:
                return {"players": [player]}
                print("player found", player)
    return {"players": data.get("players", [])}

def delete_player(name, filename='players_database.json'):
        """Supprime un joueur en fonction de son nom."""
        all_data = get_all_data()
        data = {"players": all_data.get("players", [])}

        #  = get_players(name)
        print("current players",data)

        # Filtrer les joueurs à garder
        new_players = [p for p in data["players"] if p["name"] != name]
        print("new_players",new_players)
        print(len(new_players), len(all_data["players"]))
        # Si aucun joueur n'a été supprimé, le nom n'existe pas


        if len(new_players) == len(all_data["players"]):
            print(f"❌ Player {name} not found.")
            return False

        # Sauvegarde les nouveaux joueurs
        all_data["players"] = new_players
        print("all_data players",all_data["players"])
        # all_data["players"] = data["players"]
        # print("all_data",all_data)
        # data = all_data
        with open(filename, 'w') as f:
            json.dump(all_data, f, indent=4)
        # Sauvegarde les données
        print(f"✅ Player {name} deleted successfully!")
        return True

player1 = Player(8, "Mon_enoooorme_chibre", 50, "Warrior", "Elf")
player2 = Player(8, "Mama_mia", 50, "Warrior", "Elf")

# print("get_players",get_players('game_database.json'))
# player2.create_player()
delete_player("Mon_big_chibre")
