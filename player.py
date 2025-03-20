import json


class player ():
    def __init__(self, id, name, level):
        self.id = id
        self.name = name
        self.level = level

    def create_player(self):
        # Sample data
        data = {
            "players": [
                {"id": {self.id}, "name": {self.name}, "level": {self.level}},
                {"id": 2, "name": "Bob", "level": 2}
            ]
        }


        # Write data to a JSON file
        with open('game_database.json', 'w') as f:
            json.dump(data, f, indent=4)

        return data

def get_players():
    # Read data from the JSON file
    with open('game_database.json', 'r') as f:
        data = json.load(f)

    return data['players']