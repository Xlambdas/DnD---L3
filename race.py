# race.py
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

class BaseRace:
    """Base class for all races"""
    def __init__(self, name):
        self.name = name
        self.base_health = 25  # Default value
        self.bonus = {}  # Default empty bonus
        
    def describe(self):
        """Return a description of the race"""
        bonus_descr = ", ".join(f"{key}: {value}" for key, value in self.bonus.items())
        return f"Race: {self.name}, Base Health: {self.base_health}, Abilities: {bonus_descr}"
    
    def attack_bonus(self, base_attack):
        """Calculate attack bonus based on race abilities"""
        bonus = sum(self.bonus.values())
        return base_attack + bonus

    def get_endurance(self):
        """Each race might modify endurance differently"""
        return 0  # Base modifier

class Race(BaseRace):
    """Race class that loads data from database"""
    def __init__(self, name):
        super().__init__(name)
        self.data = self.get_race(name)
        self.base_health = self.data['base_health']
        self.bonus = self.data['bonus']
        
    def get_race(self, name):
        """Get race data from database"""
        data = get_all_data()
        for race in data['race']:
            if race['name'] == name:
                return race
        return data['race'][0]  # Return first race as default

# Specific race classes
class Elf(Race):
    def __init__(self):
        super().__init__("Elf")
        # Additional elf-specific attributes
        self.night_vision = True
        
    def get_endurance(self):
        """Elves are more agile but have less endurance"""
        return -2

class Dwarf(Race):
    def __init__(self):
        super().__init__("Dwarf")
        # Additional dwarf-specific attributes
        self.stone_resistance = True
        
    def get_endurance(self):
        """Dwarves have better endurance"""
        return +3

class Human(Race):
    def __init__(self):
        super().__init__("Human")
        # Additional human-specific attributes
        self.adaptability = True
        
    def get_endurance(self):
        """Humans have average endurance"""
        return +1