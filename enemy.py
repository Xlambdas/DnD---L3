import random

class Enemy:
    """Base for all enemies"""
    def __init__(self, name, health, strength, endurance, xp_value = 5, range_att = 1):
        self.name = name
        self.health = health
        self.strength = strength
        self.endurance = endurance
        self.coord = (1,1)
        self.xp_value = xp_value
        self.player_level = 1
        self.range_att = range_att

    def descr(self):
        """Return a description of the enemy"""
        return f"{self.name}: Health={self.health}, Strength={self.strength}, Endurance={self.endurance}"

    def action(self, position, player_coord):
        """Decide what action to take based on player position"""
        distance = self.distance_to(player_coord)

        if distance <= self.range_att:
            return ('attack', self.__attack())
        else:
            return ('mouv', self.__move_toward(position, player_coord))

    def distance_to(self, target_coord):
        """Calculate Manhattan distance to target"""
        x1, y1 = self.coord
        x2, y2 = target_coord
        return abs(x2 - x1) + abs(y2 - y1)

    def __attack(self):
        """Attack the player"""
        base_damage = self.strength + random.randint(1, 6)

        if self.player_level <= 2:
            damage = base_damage
        else:
            level_multiplier = 1 + (self.player_level - 2) * 0.2
            damage = int(base_damage * level_multiplier)
        return damage

    def defend(self, damage):
        """Defend against an attack"""
        reduced_damage = max(0, damage - self.endurance // 10)
        self.health -= reduced_damage
        return ("defend", reduced_damage)

    def __move_toward(self, position, target_coord):
        """Move toward the target (player) coordinates"""
        current_x, current_y = self.coord
        target_x, target_y = target_coord

        movement_range = max(1, self.endurance // 10)
        potential_moves = []
        if current_x < target_x and current_x + movement_range < 39:
            potential_moves.append((min(current_x + movement_range, target_x), current_y))
        if current_x > target_x and current_x - movement_range > 0:
            potential_moves.append((max(current_x - movement_range, target_x), current_y))
        if current_y < target_y and current_y + movement_range < 19:
            potential_moves.append((current_x, min(current_y + movement_range, target_y)))
        if current_y > target_y and current_y - movement_range > 0:
            potential_moves.append((current_x, max(current_y - movement_range, target_y)))

        valid_moves = [move for move in potential_moves if move not in position]
        if not valid_moves:
            print(f"enemy - move_toward : {self.name} cannot move (all paths blocked).")
            return self.coord

        new_x, new_y = valid_moves[0]
        self.coord = (new_x, new_y)
        return self.coord


# --- | Specific enemy classes | ---

class Cutiie(Enemy):
    def __init__(self):
        super().__init__("Cutiie", health=3, strength=5, endurance=15, xp_value=15, range_att=1)

class Goblin(Enemy):
    """Goblin enemy - fast but weak"""
    def __init__(self):
        super().__init__("Goblin", health=4, strength=8, endurance=25, xp_value=25, range_att=2)

class Orc(Enemy):
    """Orc enemy - strong but slow"""
    def __init__(self):
        super().__init__("Orc", health=5, strength=15, endurance=20, xp_value=40, range_att=1)

class Troll(Enemy):
    """Troll enemy - high endurance and health"""
    def __init__(self):
        super().__init__("Troll", health=10, strength=12, endurance=30, xp_value=50, range_att=1)

class Vampire(Enemy):
    """Vampire enemy - regenerates health"""
    def __init__(self):
        super().__init__("Vampire", health=8, strength=10, endurance=20, xp_value=60, range_att=2)

    def defend(self, damage):
        """Vampire regenerates a portion of health when defending"""
        reduced_damage = max(0, damage - self.endurance // 10)
        self.health -= reduced_damage
        self.health += 2
        print(f"{self.name} regenerates 2 health points!")
        return ("defend", reduced_damage)

class Dragon(Enemy):
    """Dragon enemy - powerful and has a ranged attack"""
    def __init__(self):
        super().__init__("Dragon", health=20, strength=25, endurance=40, xp_value=100, range_att=5)

    def __attack(self):
        """Dragon has a chance to use a fire breath attack"""
        if random.random() < 0.3:  # 30% chance to use fire breath
            damage = self.strength * 2 + random.randint(10, 20)
            print(f"{self.name} uses Fire Breath for {damage} damage!")
            return damage
        else:
            return super().__attack()



#  final boss :

class Boss(Enemy):
    def __init__(self):
        super().__init__("Boss", health=1, strength=30, endurance=15, xp_value=150, range_att=10)
        self.coord = (10, 20)
        self.special_abilities = ["Fireball", "meteor"]
        self.phase = 1
        self.ability = None
        self.attack_pos = []
        self.dmg = 0

    def __attack(self):
        """Boss has a chance to use a special ability"""
        self.dmg = self.__next_attack()
        print(f"enemy (Boss) - attack : {self.dmg}!")
        return


    def action(self, position, player_coord):
        self.get_attack()
        return

    def get_attack(self):
        """Get the type of attack the boss will use"""
        if self.ability != None:
            print(f"enemy (Boss) - get_attack : {self.name} is attacking with {self.ability}!")
            self.__attack()
            self.ability = None
        else:
            self.ability = random.choice(self.special_abilities)
            self.dmg = self.__next_attack()
        return

    def __next_attack(self):
        """Boss has a chance to use a special ability"""
        if self.ability == "Fireball":
            damage = self.strength * 2 + random.randint(5, 10)
            return damage
        elif self.ability == "meteor":
            damage = self.strength + random.randint(10, 15)
            return ("special_attack", "Earthquake", damage)
        else:
            damage = self.strength + random.randint(1, 8)
            print(f"enemy (Boss) - next_attack : {self.name} attacks for {damage} damage!")
            return

    def defend(self, damage):
        """Boss has a chance to reduce incoming damage significantly"""
        if random.random() < 0.2:  # 20% chance to block most damage
            reduced_damage = max(0, damage // 2)
            print(f"enemy (Boss) - defend (block) : {self.name} blocks most of the attack, taking only {reduced_damage} damage!")
        else:
            reduced_damage = max(0, damage - self.endurance // 5)
            print(f"enemy (Boss) - defend : {self.name} defends and takes {reduced_damage} damage!")
        self.health -= reduced_damage
        return ("defend", reduced_damage)

    def phase_transition(self):
        """Transition to the next phase when health is low"""
        if self.health < 50 and self.phase == 1:
            self.phase = 2
            self.strength += 10
            self.endurance += 5
            print(f"{self.name} enters Phase 2, becoming more powerful!")