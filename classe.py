from ezTK import *


# Function to retrieve a class by name
def get_class_by_name(name):
    return predefined_classes.get(name, None)


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



# print(get_class_by_name("Warrior").describe())