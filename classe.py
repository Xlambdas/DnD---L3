# classe.py
import json
import os

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

def get_all_classe_name():
    """Retrieve all class names from the dataset."""
    data = get_all_data()
    classes = data['classe']
    classes_name = [classe['name'] for classe in classes]
    return classes_name

class BaseClasse:
    """Base class for all character classes"""
    def __init__(self, name):
        self.class_name = name
        self.strength = 20  # Default value
        self.endurance = 20  # Default value
        self.bonus = {}  # Default empty bonus
        
    def describe(self):
        """Returns a description of the class."""
        bonus_desc = ", ".join(f"{key}: {value}" for key, value in self.bonus.items())
        return f"Class: {self.class_name}, Strength: {self.strength}, Endurance: {self.endurance}, Bonus: {bonus_desc}"
        
    def attack(self):
        """Basic attack method"""
        return f"{self.class_name} attacks with a strength of {self.strength}!"
        
    def defend(self):
        """Basic defend method"""
        return f"{self.class_name} defends with an endurance of {self.endurance}."
        
    def get_endurance(self):
        """Return the endurance value for movement calculations"""
        return self.endurance
        
    def special_ability(self):
        """Each class has a special ability"""
        return f"{self.class_name} uses a special ability!"

class Classe(BaseClasse):
    """Class that loads data from database"""
    def __init__(self, name):
        super().__init__(name)
        self.data = self.get_classe(name)
        self.strength = self.data['strength']
        self.endurance = self.data['endurance']
        self.bonus = self.data['bonus']
        
    def get_classe(self, name):
        """Retrieve a specific class by name from the dataset."""
        data = get_all_data()
        for classe in data['classe']:
            if classe['name'] == name:
                return classe
        raise ValueError(f"Class {name} not found.")

# Specific class implementations
class Warrior(Classe):
    def __init__(self):
        super().__init__("Warrior")
        # Additional warrior-specific attributes
        self.weapon_mastery = True
        
    def special_ability(self):
        return f"{self.class_name} uses Heroic Strike!"

class Mage(Classe):
    def __init__(self):
        super().__init__("Mage")
        # Additional mage-specific attributes
        self.spell_mastery = True
        
    def special_ability(self):
        return f"{self.class_name} casts Arcane Explosion!"
        
    def attack(self):
        """Mages attack with magic"""
        return f"{self.class_name} casts a spell with intelligence of {self.bonus.get('intelligence', 0)}!"

class Rogue(Classe):
    def __init__(self):
        super().__init__("Rogue")
        # Additional rogue-specific attributes
        self.stealth_mastery = True
        
    def special_ability(self):
        return f"{self.class_name} uses Shadowstrike!"