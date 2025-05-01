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

    def describe(self):
        """Return a description of the enemy"""
        return f"{self.name}: Health={self.health}, Strength={self.strength}, Endurance={self.endurance}"

    def action(self, position, player_coord):
        """Decide what action to take based on player position"""
        # Calculate distance to player
        distance = self.distance_to(player_coord)

        if distance <= self.range_att: # if in range attack the player
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

        # Ajuster les dégâts en fonction du niveau du joueur
        # À partir du niveau 3, les ennemis deviennent plus forts
        if self.player_level <= 2:
            damage = base_damage
        else:
            # Augmentation de 10% par niveau au-dessus de 2
            level_multiplier = 1 + (self.player_level - 2) * 0.1
            damage = int(base_damage * level_multiplier)

        # print(f"{self.name} attacks for {damage} damage (level adjustment: x{level_multiplier if self.player_level > 2 else 1})!")
        return damage

    def defend(self, damage):
        """Defend against an attack"""
        # Calculate damage after endurance reduction
        reduced_damage = max(0, damage - self.endurance // 10)
        self.health -= reduced_damage
        # print(f"{self.name} defends and takes {reduced_damage} damage!")
        return ("defend", reduced_damage)

    def __move_toward(self, position, target_coord):
        """Move toward the target coordinates"""
        # Calculate direction
        current_x, current_y = self.coord
        target_x, target_y = target_coord

        # Move up to endurance/10 steps (rounded up, minimum 1)
        movement_range = max(1, self.endurance // 10)
        # Determine direction with priority (x-axis first)
        potential_moves = []
        if current_x < target_x and current_x + movement_range < 39:
            potential_moves.append((min(current_x + movement_range, target_x), current_y))
        if current_x > target_x and current_x - movement_range > 0:
            potential_moves.append((max(current_x - movement_range, target_x), current_y))
        if current_y < target_y and current_y + movement_range < 19:
            potential_moves.append((current_x, min(current_y + movement_range, target_y)))
        if current_y > target_y and current_y - movement_range > 0:
            potential_moves.append((current_x, max(current_y - movement_range, target_y)))

        # Filter out positions that are in the 'position' list (unavailable)
        # print (f"Potential moves: {potential_moves} in {position}")
        valid_moves = [move for move in potential_moves if move not in position]

        if not valid_moves:
            print(f"enemy - move_toward : {self.name} cannot move (all paths blocked).")
            return self.coord

        # Choose the first valid move (priority given to x-axis movement)
        new_x, new_y = valid_moves[0]

        # Update position
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
        self.sneaky = True



class Orc(Enemy):
    """Orc enemy - strong but slow"""
    def __init__(self):
        super().__init__("Orc", health=5, strength=15, endurance=20, xp_value=40, range_att=1)




#  final boss :

class Boss(Enemy):
    def __init__(self):
        super().__init__("Boss", health=1, strength=30, endurance=15, xp_value=150, range_att=10)
        self.coord = (10, 20)
        self.special_abilities = ["Fireball", "Earthquake", "Summon Minions"]
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
            print("enemy (Boss) - get_attack : Boss is preparing to attack!")
            self.ability = "Fireball"
            # if random.random() < 0.5:
            #     self.ability = random.choice(self.special_abilities)
            # else:
            #     self.ability = "Normal"
            dmg = self.__next_attack()
            print(f"enemy (Boss) - get_attack : uses {self.ability} for {dmg} damage!")
        return

    def __next_attack(self):
        """Boss has a chance to use a special ability"""
        if self.ability == "Fireball":
            damage = self.strength * 2 + random.randint(5, 10)
            return damage
        elif self.ability == "Earthquake":
            damage = self.strength + random.randint(10, 15)
            return ("special_attack", "Earthquake", damage)
        elif self.ability == "Summon Minions":
            print(f"enemy (Boss) - next_attack 2 : {self.name} summons minions to aid in battle!")
            return ("summon", "Minions")
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

