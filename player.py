# player.py
import json
import os
import random
from race import Human
from classe import Warrior

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
        self.health = info_player['health']
        self.palier = info_player['palier']

        self.level = self.calculate_level()
        self.xp_to_next_level = 100 * self.level

        race_class = globals().get(self.race_name)
        self.info_race = race_class() if race_class else Human()
        classe_class = globals().get(self.classe_name)
        self.info_classe = classe_class() if classe_class else Warrior()

        self.actions = 2
        self.coord = (random.randrange(0,10), random.randrange(0,3))

    def calculate_level(self):
        """Calcule le niveau en fonction de l'XP"""
        level = 1
        xp_threshold = 100

        while self.xp >= xp_threshold:
            level += 1
            xp_threshold += 100 * level
        return level

    def gain_xp(self, amount):
        """Ajoute de l'XP au joueur et gère la montée de niveau"""
        old_level = self.level
        self.xp += amount

        new_level = self.calculate_level()
        if new_level > old_level:
            self.level = new_level
            self.xp_to_next_level = 100 * self.level
            for _ in range(new_level - old_level):
                self.health += 5

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
                player['palier'] = self.palier
                player['health'] = self.health
                player['level'] = self.level
                player['race'] = self.race_name
                player['classe'] = self.classe_name
                break

        with open('players_database.json', 'w') as f:
            json.dump(data, f, indent=4)
        return

    def bonus_range_mouv(self):
        """Calculate a balanced bonus for the player's movement range."""
        bonus_race = self.info_race.range_mouv()
        bonus_classe = self.info_classe.range_mouv()
        random_bonus = random.randint(1, 3)
        bonus = random_bonus + bonus_race + bonus_classe

        max_bonus = 10
        bonus = min(bonus, max_bonus)
        print("class player - Bonus range mouvement:", bonus)
        return bonus

    def bonus_range_attack(self):
        """Calculate a balanced bonus for the player's attack range."""
        bonus_race = self.info_race.range_attack()
        bonus_classe = self.info_classe.range_attack()
        random_bonus = random.randint(1, 3)
        bonus = random_bonus + bonus_race + bonus_classe

        max_bonus = 10
        bonus = min(bonus, max_bonus)
        print("class player - Bonus range attack:", bonus)
        return bonus

    def bonus_attack(self):
        """Calculate a balanced bonus for the player's attack."""
        base_bonus = random.randint(1, 6)
        level_bonus = int(self.level * 2)
        bonus_race = self.info_race.attack(base_bonus)
        bonus_classe = self.info_classe.attack()
        total_bonus = base_bonus + level_bonus + bonus_race + bonus_classe

        max_bonus = 20
        total_bonus = min(total_bonus, max_bonus)

        print(f"class player - Bonus attack: {base_bonus} (base) + {level_bonus} (level) + {bonus_race} (race) + {bonus_classe} (class) = {total_bonus}")
        return total_bonus

    def bonus_defense(self):
        """Calculate a balanced bonus for the player's defense."""
        base_bonus = random.randint(1, 6)
        level_bonus = int(self.level * 2)
        bonus_race = self.info_race.defend()
        bonus_classe = self.info_classe.defend()
        total_bonus = base_bonus + level_bonus + bonus_race + bonus_classe

        max_bonus = 20
        total_bonus = min(total_bonus, max_bonus)

        print(f"class player - Bonus defense: {base_bonus} (base) + {level_bonus} (level) + {bonus_race} (race) + {bonus_classe} (class) = {total_bonus}")
        return total_bonus

    def defensed(self, damage):
        """Defend against an attack."""
        bonus = self.bonus_defense()
        reduced_damage = max(0, damage - bonus)
        self.health -= reduced_damage

        print(f"class player - {self.name} defends and takes {reduced_damage} damage!")
        return reduced_damage


