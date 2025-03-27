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
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {"players": []}
        else:
            data = {"players": []}

        # Ajoute le joueur et sauvegarde
        data["players"].append(self.to_dict())

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

def get_players():
    # Read data from the JSON file
    with open('game_database.json', 'r') as f:
        try:
            data = json.load(f)
            return data.get('players', [])
        except json.JSONDecodeError:
            return []

# test
player1 = Player(1, "Steve", 5)
# player1.create_player()
print(get_players())
