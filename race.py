import json
import os
from main import get_all_data


class Race:
    def __init__(self, name, speed, abilities):
        self.name = name
        self.speed = speed
        self.abilities = abilities

    def describe(self):
        """
        renvoie une description de la race.
        """
        abilities_desc = ", ".join(f"{key}: {value}" for key, value in self.abilities.items())
        return f"Race: {self.name}, Speed: {self.speed}, Abilities: {abilities_desc}"
        # Example of predefined races stored in a dictionary

    def attack_bonus(self, base_attack):
        """
        Calcule le bonus d'attaque en fonction des capacités de la race.
        """
        bonus = sum(self.abilities.values())
        return base_attack + bonus



def get_race(name):
    data = get_all_data()
    for race in data['race']:
        if race['name'] == name:
            return race
    return data['race']

playerRace = get_race("Elf")
player01 = Race(playerRace['name'], playerRace['base_health'], playerRace['bonus'])

print(player01.describe())
