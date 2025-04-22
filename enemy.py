import random

class Enemy:
    """Base for all enemies"""
    def __init__(self, name, health, strength, endurance):
        self.name = name
        self.health = health
        self.strength = strength
        self.endurance = endurance
        self.coord = (0,0)

    def describe(self):
        """Return a description of the enemy"""
        return f"{self.name}: Health={self.health}, Strength={self.strength}, Endurance={self.endurance}"

    def action(self, position, player_coord):
        """Decide what action to take based on player position"""
        # Calculate distance to player
        distance = self.distance_to(player_coord)

        if distance <= 1: # if in range attack the player
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
        damage = self.strength + random.randint(1, 6)  # Base strength + random roll
        print(f"{self.name} attacks for {damage} damage!")
        return damage

    def range_attack(self):
        """Range for the attack"""
        range = 1
        return range

    def defend(self, damage):
        """Defend against an attack"""
        # Calculate damage after endurance reduction
        reduced_damage = max(0, damage - self.endurance // 10)
        self.health -= reduced_damage
        print(f"{self.name} defends and takes {reduced_damage} damage!")
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
        print (f"Potential moves: {potential_moves} in {position}")
        valid_moves = [move for move in potential_moves if move not in position]

        if not valid_moves:
            print(f"{self.name} cannot move (all paths blocked).")
            return self.coord

        # Choose the first valid move (priority given to x-axis movement)
        new_x, new_y = valid_moves[0]

        # Update position
        self.coord = (new_x, new_y)
        print(f"{self.name} moves to {self.coord}")
        return self.coord

    def is_occupied(self, position):
        """Check if a position is occupied by another enemy"""
        # This method should be implemented to check the game state for other enemies
        # For now, it returns False as a placeholder
        return False


class Boss(Enemy):
    def __init__(self):
        super().__init__("Boss", health=45, strength=30, endurance=15)







class Cutiie(Enemy):
    def __init__(self):
        super().__init__("Cutiie", health=3, strength=5, endurance=15)


# --- | Specific enemy classes | ---
class Goblin(Enemy):
    """Goblin enemy - fast but weak"""
    def __init__(self):
        super().__init__("Goblin", health=3, strength=8, endurance=25)
        self.sneaky = True

    def attack(self):
        """Goblins have a chance to do a sneak attack"""
        if random.random() < 0.3 and self.sneaky:  # 30% chance of sneak attack
            damage = self.strength * 2 + random.randint(1, 4)
            print(f"{self.name} performs a sneak attack for {damage} damage!")
            return ("attack", damage)
        else:
            return super().attack()

    def defend(self, damage):
        """Goblins are quick and can dodge some attacks"""
        dodge_chance = random.random()
        if dodge_chance < 0.05:
            print(f"{self.name} dodges the attack!")
            return ("dodge", 1)
        else:
            return super().defend(damage+3)



class Orc(Enemy):
    """Orc enemy - strong but slow"""
    def __init__(self):
        super().__init__("Orc", health=5, strength=15, endurance=20)
        self.rage = 0

    def attack(self):
        """Orcs do more damage when enraged"""
        rage_bonus = self.rage
        damage = self.strength + rage_bonus + random.randint(1, 8)
        print(f"{self.name} attacks with rage ({rage_bonus}) for {damage} damage!")
        return ("attack", damage)
