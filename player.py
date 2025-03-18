import json

def create_player():
    # Sample data
    data = {
        "players": [
            {"id": 1, "name": "Alice", "level": 1},
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