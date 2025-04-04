from ezTK import *
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

def get_all_classe_name ():
    """
        Retrieve all classes from the dataset.
        Returns:
            data: A list representing all classes in the dataset.
    """
    data = get_all_data()
    classes = data['classe']
    classes_name = [classe['name'] for classe in classes]
    return classes_name



# --- | Instance of Classe | ---
class Classe ():
    def __init__(self, name):
        self.class_name = name
        self.data = self.get_classe(name)
        self.strength = self.data['strength']
        self.endurance = self.data['endurance']
        self.bonus = self.data['bonus']

    def describe(self):
        """
            Returns a description of the choosen class.
        """
        bonus_desc = ", ".join(f"{key}: {value}" for key, value in self.bonus.items())
        return f"Class: {self.class_name}, Strength: {self.strength}, Endurance: {self.endurance}, Bonus: {bonus_desc}"

    def get_classe(self, name: str):
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
        for classe in data['classe']:
            if classe['name'] == name:
                return classe
        raise ValueError(f"Class {name} not found.")


    def attack(self):
        return f"{self.class_name} attacks with a strength of {self.strength}!"

    def defend(self):
        return f"{self.class_name} defends with an endurance of {self.endurance}."



# --- | brouillon | -----------------------------------------------

# --- | Zone de test | ---