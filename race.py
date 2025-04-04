import json
import os

# --- | general functions | ---
def get_all_data(filename='players_database.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    return data



# --- | instance of Race | ---
class Race:
    def __init__(self, name):
        self.name = name
        self.data = self.get_race(name)
        self.health = self.data['base_health']
        self.bonus = self.data['bonus']

    def describe(self):
        """
            Return a description of the player Race : name, speed and abilities.
        """
        bonus_descr = ", ".join(f"{key}: {value}" for key, value in self.bonus.items())
        return f"Race: {self.name}, Speed: {self.health}, Abilities: {bonus_descr}"
        # Example of predefined races stored in a dictionary

    def get_race(self, name):
        """
            Get all the data concerning the races (about the player) from the database
        """
        data = get_all_data()
        for race in data['race']:
            if race['name'] == name:
                return race
        return data['race']

    def attack_bonus(self, base_attack):
        """
            Calcule le bonus d'attaque en fonction des capacités de la race.
        """
        bonus = sum(self.abilities.values())
        return base_attack + bonus



# --- | brouillon | -----------------------------------------------

# --- | Zone de test | ---
