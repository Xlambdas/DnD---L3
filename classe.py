# from ezTK import *
# import json


# # Function to retrieve a class by name
# def get_class_by_name(name):
#     return predefined_classes.get(name, None)


class Classe ():
    def __init__(self, nom, force, endurance, bonus):
        self.nom_classe = nom
        self.force = force
        self.endurance = endurance
        self.bonus = bonus

    def describe(self):
        """
        Renvoie une description de la classe.
        """
        bonus_desc = ", ".join(f"{key}: {value}" for key, value in self.bonus.items())
        return f"Classe: {self.nom_classe}, Force: {self.force}, Endurance: {self.endurance}, Bonus: {bonus_desc}"


    def attaquer(self):
        return f"{self.nom} attaque avec une force de {self.force}!"

    def defendre(self):
        return f"{self.nom} se défend avec une endurance de {self.endurance}."

# # ----------------------------------
# filename = 'players_database.json'
# dataClass = {}

# # Load the JSON data from the file
# try:
#     with open(filename, 'r') as file:
#         data = json.load(file)
#         print("All data:", data)

#     # Retrieve the class data for "Warrior"
#     # Adjusting to handle different JSON structures
#     if isinstance(data, dict) and "classe" in data and "Warrior" in data["classe"]:
#         warrior_data = data["classe"]["Warrior"]
#         print("Warrior data:", warrior_data)
#     elif isinstance(data, list):
#         for item in data:
#             if isinstance(item, dict) and "classe" in item and "Warrior" in item["classe"]:
#                 warrior_data = item["classe"]["Warrior"]
#                 print("Warrior data:", warrior_data)
#                 break
#         else:
#             print("Error: 'Warrior' class not found in the list.")
#             warrior_data = None
#     else:
#         print("Error: Unexpected JSON structure.")
#         warrior_data = None
#     if warrior_data:
#         dataClass["Warrior"] = Classe(
#             warrior_data["nom"],
#             warrior_data["force"],
#             warrior_data["endurance"],
#             warrior_data["bonus"]
#         )
# except FileNotFoundError:
#     print(f"Error: The file '{filename}' was not found.")
# except json.JSONDecodeError:
#     print(f"Error: The file '{filename}' contains invalid JSON.")
# # dataClass["Warrior"] = Classe("Warrior", 40, 35, {"Strength": 5, "Defense": 3})
# print("dataClass : ", dataClass)
predefined_classes = {

    "Warrior": Classe("Warrior", 40, 35, {"Strength": 5, "Defense": 3}),
    "Mage": Classe("Mage", 20, 25, {"Intelligence": 5, "Mana": 3}),
    "Rogue": Classe("Rogue", 30, 20, {"Dexterity": 5, "Stealth": 3}),
    "Cleric": Classe("Cleric", 25, 30, {"Wisdom": 5, "Healing": 3}),
    "Paladin": Classe("Paladin", 35, 40, {"Charisma": 5, "Holy Power": 3}),
    "Ranger": Classe("Ranger", 30, 25, {"Dexterity": 4, "Marksmanship": 3}),
    "Barbarian": Classe("Barbarian", 45, 30, {"Strength": 6, "Rage": 3}),
    "Sorcerer": Classe("Sorcerer", 20, 20, {"Magic Power": 6, "Arcane Knowledge": 3}),
}

# guerrier = Classe(dataClass["Warrior"])

# print(get_class_by_name("Warrior").describe())

# guerrier.describe()



# retry -------------------------

import json
import os

def get_data(filename='players_database.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"classe": []}
    else:
        data = {"classe": []}
    return data


def get_classe(name):
    data = get_data()
    for classe in data['classe']:
        if classe['name'] == name:
            return classe
    return data['classe']


playerClass = get_classe("cataa")

player01 = Classe(playerClass["name"], playerClass["strength"], playerClass["endurance"], playerClass["bonus"])
print(player01.describe())