import json
import os
# from other files :
from main import get_all_data


class Race:
    def __init__(self, name, health, bonus):
        self.name = name
        self.health = health
        self.bonus = bonus

    def describe(self):
        """
            Return a description of the player Race : name, speed and abilities.
        """
        bonus_descr = ", ".join(f"{key}: {value}" for key, value in self.bonus.items())
        return f"Race: {self.name}, Speed: {self.health}, Abilities: {bonus_descr}"
        # Example of predefined races stored in a dictionary

    def attack_bonus(self, base_attack):
        """
            Calcule le bonus d'attaque en fonction des capacités de la race.
        """
        bonus = sum(self.abilities.values())
        return base_attack + bonus



def get_race(name):
    """
        Get all the data concerning the races (about the player) from the database
    """
    data = get_all_data()
    for race in data['race']:
        if race['name'] == name:
            return race
    return data['race']

playerRace = get_race("Elf")
player01 = Race(playerRace['name'], playerRace['base_health'], playerRace['bonus'])

print(player01.describe())
