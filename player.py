# player.py
import json
import os
import random
from race import Race, Elf, Dwarf, Human
from classe import Classe, Warrior, Mage, Rogue

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

class Player():
    def __init__(self, name):
        """
            Initialize a player with their name and load their data.
        """
        self.name = name
        info_player = self.get_bdd()
        self.race_name = info_player['race']
        self.classe_name = info_player['classe']
        self.xp = info_player['xp']
        
        # Create race object - use specific class if available
        if self.race_name == "Elf":
            self.info_race = Elf()
        elif self.race_name == "Dwarf":
            self.info_race = Dwarf()
        elif self.race_name == "Human":
            self.info_race = Human()
        else:
            self.info_race = Race(self.race_name)
            
        # Create class object - use specific class if available
        if self.classe_name == "Warrior":
            self.info_classe = Warrior()
        elif self.classe_name == "Mage":
            self.info_classe = Mage()
        elif self.classe_name == "Rogue":
            self.info_classe = Rogue()
        else:
            self.info_classe = Classe(self.classe_name)
            
        self.actions = 2
        self.coord_player = (random.randrange(0,10), random.randrange(0,3))

    def descr(self):
        return {"name": self.name, "level": 1, "classe": self.classe_name, "race": self.race_name}

    def get_bdd(self):
        """Get player data from database"""
        data = get_all_data()
        for player in data['players']:
            if player['name'] == self.name:
                return player
        print("You can't play, the name enter is not in the Database...")
        return {}

    def set_bdd(self):
        """Set player data in database"""
        pass

    def action(self, type):
        """Perform player action"""
        if self.actions <= 0:
            print("No actions left.")
            return None
        self.actions -= 1
        if type == "attack":
            return self.attack()
        elif type == "mouv":
            return self.mouv()
        else:
            print("Unknown action type.")
            return None

    def attack(self):
        """Player attack action"""
        print("file player - attack")
        # Use class-specific attack and race bonuses
        base_attack = self.info_classe.strength
        attack_with_bonus = self.info_race.attack_bonus(base_attack)
        print(f"{self.name} attacks with {attack_with_bonus} strength!")
        return attack_with_bonus

    def mouv(self):
        """Movement based on class endurance and race modifiers"""
        print("file player - mouv")
        if not hasattr(self, 'coord_player'):
            print("Error: Player coordinates not initialized")
            return None
        
        print(f"Current position: {self.coord_player}")
        
        # Get endurance from class and race modifier
        base_endurance = self.info_classe.get_endurance()
        race_modifier = self.info_race.get_endurance()
        total_endurance = base_endurance + race_modifier
        
        # Calculate movement range based on endurance
        if total_endurance < 25:
            movement_range = 1
        elif total_endurance < 35:
            movement_range = 2
        else:
            movement_range = 3
        
        print(f"Movement range based on endurance ({total_endurance}): {movement_range}")
        
        # Random movement within range
        current_x, current_y = self.coord_player
        
        # Movement logic
        new_x = max(0, min(9, current_x + random.randint(-movement_range, movement_range)))
        new_y = max(0, min(19, current_y + random.randint(-movement_range, movement_range)))
        
        # Update player coordinates
        self.coord_player = (new_x, new_y)
        print(f"Moved to: {self.coord_player}")
        
        return self.coord_player