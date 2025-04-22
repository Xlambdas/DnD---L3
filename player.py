# player.py
import json
import os
import random
from race import BaseRace, Elf, Dwarf, Human
from classe import BaseClasse, Warrior, Mage, Rogue

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
            Initialize a player with their name and load their data.²
        """
        self.name = name
        info_player = self.get_bdd()
        self.race_name = info_player['race']
        self.classe_name = info_player['classe']
        self.xp = info_player['xp']
        self.health = info_player['health']

        # Create race object - use specific class if available
        race_class = globals().get(self.race_name)
        self.info_race = race_class() if race_class else BaseRace("Human")
        # Create class object - use specific class if available
        classe_class = globals().get(self.classe_name)
        self.info_classe = classe_class() if classe_class else BaseClasse("Warrior")

        self.actions = 2
        self.coord = (random.randrange(0,10), random.randrange(0,3))

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
        data = get_all_data()
        for player in data.get('players', []):
            if player['name'] == self.name:
                player['xp'] = self.xp
                break
        else:
            # If player not found, add new player data
            pass

        # Save updated data back to the file
        with open('players_database.json', 'w') as f:
            json.dump(data, f, indent=4)

    def bonus_range_mouv (self):
        """randomly take a number between 1 and 6 for the bonus of mouvement of the player
        return the bonus of movement"""
        bonus = random.randint(1, 3) + 1
        print ("bonus range mouvement : ", bonus)
        return bonus

    def bonus_range_attack (self):
        """randomly take a number between 1 and 6 for the bonus of mouvement of the player
        return the bonus of movement"""
        bonus = random.randint(1, 3) + 1
        print ("bonus range attack : ", bonus)
        return bonus

    def bonus_attack (self):
        """randomly take a number between 1 and 6 for the bonus of attack of the player
        return the bonus of attack"""
        bonus = random.randint(1, 3) + 1
        print ("bonus attack : ", bonus)
        return bonus

    def bonus_defense (self):
        """randomly take a number between 1 and 6 for the bonus of defense of the player
        return the bonus of defense"""
        bonus = random.randint(1, 3) + 1
        print ("bonus defense : ", bonus)
        return bonus


    def defensed (self, damage):
        """Defend against an attack"""
        # Calculate damage after endurance reduction
        bonus = self.bonus_defense()
        reduced_damage = max(0, damage - bonus)
        self.health -= reduced_damage
        print(f"{self.name} defends and takes {reduced_damage} damage!")
        return reduced_damage


