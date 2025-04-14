# enemy.py
import random
from race import BaseRace

class Enemy:
    """Base class for all enemies"""
    def __init__(self, name, health, strength, endurance):
        self.name = name
        self.health = health
        self.strength = strength
        self.endurance = endurance
        self.coord = (random.randrange(0,10), random.randrange(0,3))
        
    def describe(self):
        """Return a description of the enemy"""
        return f"{self.name}: Health={self.health}, Strength={self.strength}, Endurance={self.endurance}"
        
    def act(self, player_coord):
        """Decide what action to take based on player position"""
        # Calculate distance to player
        distance = self.distance_to(player_coord)
        
        # If player is within attack range, attack
        if distance <= 1:
            return self.attack()
        # Otherwise, move toward player
        else:
            return self.move_toward(player_coord)
            
    def distance_to(self, target_coord):
        """Calculate Manhattan distance to target"""
        x1, y1 = self.coord
        x2, y2 = target_coord
        return abs(x2 - x1) + abs(y2 - y1)
        
    def attack(self):
        """Attack the player"""
        damage = self.strength + random.randint(1, 6)  # Base strength + random roll
        print(f"{self.name} attacks for {damage} damage!")
        return ("attack", damage)
        
    def move_toward(self, target_coord):
        """Move toward the target coordinates"""
        # Calculate direction
        current_x, current_y = self.coord
        target_x, target_y = target_coord
        
        # Move up to endurance/10 steps (rounded up, minimum 1)
        movement_range = max(1, self.endurance // 10)
        
        # Determine direction with priority (x-axis first)
        if current_x < target_x:
            new_x = min(current_x + movement_range, target_x)
            new_y = current_y
        elif current_x > target_x:
            new_x = max(current_x - movement_range, target_x)
            new_y = current_y
        elif current_y < target_y:
            new_x = current_x
            new_y = min(current_y + movement_range, target_y)
        elif current_y > target_y:
            new_x = current_x
            new_y = max(current_y - movement_range, target_y)
        else:
            # Already at target
            new_x, new_y = current_x, current_y
            
        # Update position
        self.coord = (new_x, new_y)
        print(f"{self.name} moves to {self.coord}")
        return ("move", self.coord)

class Goblin(Enemy):
    """Goblin enemy - fast but weak"""
    def __init__(self):
        super().__init__("Goblin", health=15, strength=8, endurance=25)
        self.sneaky = True
        
    def attack(self):
        """Goblins have a chance to do a sneak attack"""
        if random.random() < 0.3 and self.sneaky:  # 30% chance of sneak attack
            damage = self.strength * 2 + random.randint(1, 4)
            print(f"{self.name} performs a sneak attack for {damage} damage!")
            return ("attack", damage)
        else:
            return super().attack()

class Orc(Enemy):
    """Orc enemy - strong but slow"""
    def __init__(self):
        super().__init__("Orc", health=30, strength=15, endurance=20)
        self.rage = 0  # Rage builds up when taking damage
        
    def attack(self):
        """Orcs do more damage when enraged"""
        rage_bonus = self.rage
        damage = self.strength + rage_bonus + random.randint(1, 8)
        print(f"{self.name} attacks with rage ({rage_bonus}) for {damage} damage!")
        return ("attack", damage)
    

    #  Button(self.action_panel, text="Inventory")#, command=self.inventory_action, bg='lightgray')
    #     Button(self.action_panel, text="End Turn")#, command=self.end_turn_action, bg='lightgray')