import json
import os

class Player ():
    def __init__(self, id, name, level):
        self.id = id
        self.name = name
        self.level = level

    def to_dict(self):
        return {"id": self.id, "name": self.name, "level": self.level}

    def create_player(self, filename='game_database.json'):
        # Vérifie si le fichier existe et lit les données existantes
        data = get_players()
        print("create player",data)
        
        # Vérifie si le nom existe déjà
        existing_names = [player["name"] for player in data["players"]]

        if self.name in existing_names:
            print("Sorry, name already used")
            return False  # Évite d'aller plus loin si le nom existe déjà
    
        # Ajoute le joueur et sauvegarde
        data["players"].append(self.to_dict())

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Player {self.name} added successfully!")
        return True  # Indique que le joueur a bien été ajouté
    
def get_players(filename='game_database.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"players": []}
    else:
        data = {"players": []}
    return data

# def delete_player(name, filename='game_database.json'):
#         """Supprime un joueur en fonction de son nom."""
#         data = get_players(filename)

#         # Filtrer les joueurs à garder
#         new_players = [p for p in data["players"] if p["name"] != name]

#         if len(new_players) == len(data["players"]):
#             print(f"❌ Player {name} not found.")
#             return False

#         # Sauvegarde les nouveaux joueurs
#         data["players"] = new_players
#         Player.save_all_data(data, filename)
#         print(f"✅ Player {name} deleted successfully!")
#         return True

player1 = Player(8, "Mon_enoooorme_chibre", 50)
# print("get_players",get_players('game_database.json'))
player1.create_player()
