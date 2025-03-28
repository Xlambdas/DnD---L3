from ezTK import *
import json
# from other files :
from main import get_all_data

class Classe (): # --- | Classe | ---
    def __init__(self, name, strength, endurance, bonus):
        self.class_name = name
        self.strength = strength
        self.endurance = endurance
        self.bonus = bonus

    def describe(self):
        """
            Returns a description of the choosen class.
        """
        bonus_desc = ", ".join(f"{key}: {value}" for key, value in self.bonus.items())
        return f"Class: {self.class_name}, Strength: {self.strength}, Endurance: {self.endurance}, Bonus: {bonus_desc}"

    def attack(self):
        return f"{self.class_name} attacks with a strength of {self.strength}!"

    def defend(self):
        return f"{self.class_name} defends with an endurance of {self.endurance}."


# --- | fonction annexe | ---
# To get the class by her name
def get_classe(name: str):
    """
        Retrieve a specific class by its name from the dataset.
        Args: name (str): The name of the class to retrieve.
        Returns:
            data: A dictionary representing the class with the specified name (if found in the database).

        Note:
            This function assumes the existence of a `get_all_data` function that
            retrieves the dataset, which is expected to be a dictionary containing
            a 'classe' key with a list of class dictionaries.
    """

    data = get_all_data()
    # print("data",data)
    for classe in data['classe']:
        print("classe",classe)
        if classe['name'] == name:
            return classe
    raise ValueError(f"Class {name} not found.")



# test
playerClass = get_classe("Warrior")

player01 = Classe(playerClass["name"], playerClass["strength"], playerClass["endurance"], playerClass["bonus"])
print(player01.describe())