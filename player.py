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
    

def get_players():
    # Read data from the JSON file
    with open('game_database.json', 'r') as f:
        try:
            data = json.load(f)
            return data.get('players', [])
        except json.JSONDecodeError:
            return []

# test
player1 = Player(8, "Mon_enoooorme_chibre", 50)
player1.create_player()
print(get_players())
