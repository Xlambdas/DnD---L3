from ezTK import *  # Import all components, including TOP
from random import randint, random, choice, shuffle  # Import random functions=:
import random
# from other files :
from player import Player
from enemy import Goblin, Orc, Cutiie, Boss
from interface import GameInterface
from actions import GameActions

class DNDGame:
    def __init__(self, name):
        self.player = Player(name)
        # Create some enemies
        self.enemies = [
            Cutiie(),Orc(),Goblin()
            # Orc()
        ]
        self.action_type = None  # Track the current action type
        self.current_turn = "player"  # Start with player's turn
        self.selected_cell = None  # Track the selected cell
        self.game_over = False  # Track if the game is over
        self.ui = GameInterface(self)  # Create the game interface
        self.act = GameActions(self, self.ui)  # Create the game actions handler
        self.ui.interface()

    def player_act(self, action_type):
        print(f"Player action: {action_type}")
        self.act.player_action(action_type)


    def possible_coords(self, start_coord, move_distance): # todo : a ne pas modifier
        """Calculate possible coordinates within a movement distance"""
        possible_moves = []
        for dx in range(-move_distance, move_distance + 1):
            for dy in range(-move_distance, move_distance + 1):
                if dx**2 + dy**2 > move_distance**2:  # Use circular distance
                    continue
                new_x = start_coord[0] + dx
                new_y = start_coord[1] + dy
                if 1 <= new_x < 19 and 1 <= new_y < 39 or (new_x,new_y) == (10,0) or (new_x,new_y) == (9,0) or (new_x,new_y) == (10,39) or (new_x,new_y) == (9,39):
                    possible_moves.append((new_x, new_y))
        return possible_moves

    def on_cell_click(self, coords: tuple[int, int]):
        """Handle cell click events."""
        if self.game_over:
            return

        if self.current_turn != "player":
            self.ui.status_label.config(text="Not your turn!")
            return

        if self.player.actions < 0:
            print("No actions left.")
            return

        print(f"Cell clicked oncellclick 1 - action tye : {self.action_type}")

        if self.action_type == "mouv":
            print(f"Cell clicked: {self.action_type} - {coords}")
            self.act.mouv(coords)
            self.action_type = "None"
            return
        elif self.action_type == "attack":
            if any(enemy.coord == coords for enemy in self.enemies):
                print(f"get enemy at {coords}, or {self.enemies}")
                self.act.attack(coords)
                print(f"Attacking enemy at {coords}")
                self.action_type = "None"
                return
            else:
                self.move_distance = self.player.bonus_range_mouv()
                print(f"Cell clicked: {self.action_type} - {coords}")
                self.act.mouv(coords)
                self.action_type = "None"
                return

    def end_turn(self):
        """
            End the player's turn and switch to the enemy's turn.
        """
        if self.game_over:
            return

        if self.current_turn == "player":
            self.current_turn = "enemies"
            self.ui.status_label.config(text="Enemies' turn")
            self.player.actions = 2
            self.ui.root.after(500, self.act.enemy_action)  # Schedule enemy turn after delay
        else:
            # Update actions display
            self.ui.action_label.config(text=f"Actions left: {self.player.actions}")
            self.current_turn = "player"
            self.ui.status_label.config(text="Player's turn")


    def create_enemy(self, palier):
        """
            Create a new enemy of the specified type.
        """
        self.enemies = []
        enemy_types = []
        player_level = self.player.level


        # if palier == 5 and player_level % 2 == 1 :#not hasattr(self, 'boss_spawned') or (hasattr(self, 'boss_spawned') and not self.boss_spawned):
        #     # Engendrer un boss de palier
        #     self.ui.palier_boss()
        #     # self.boss_spawned = True
        #     return  # Ne pas générer d'autres ennemis quand le boss est présent

        # Les types d'ennemis disponibles dépendent du palier
        if palier <= 2:
            enemy_types = [Cutiie]
        elif palier <= 3:
            enemy_types = [Cutiie, Goblin]
        else:
            enemy_types = [Cutiie, Goblin, Orc]
        # else:
        #     self.ui.palier_boss();return
    
        # Le nombre d'ennemis est exactement 3 fois le palier du joueur
        enemy_count = 3 * palier

        # Création des ennemis réguliers
        for _ in range(enemy_count):
            enemy_class = random.choice(enemy_types)
            enemy = enemy_class()
            print(enemy)

            # Ajuster les statistiques en fonction du niveau
            if player_level > 1:
                enemy.health = int(enemy.health * (1 + 0.1 * player_level))
                enemy.strength = int(enemy.strength * (1 + 0.05 * player_level))
                enemy.xp_value = int(enemy.xp_value * (1 + 0.1 * player_level))
            self.enemies.append(enemy)
    
        self.ui.log_action(f"{enemy_count} nouveaux ennemis sont apparus!")


    def new_palier(self, palier):
        """
            Create a new palier of enemies.
        """
        print(f"Creating new palier: {palier}")
        self.player.set_bdd()
        print(f"saving new palier {palier} in bdd ")
        
        # Special handling for boss palier
        if palier == self.ui.MAX_PALIER:
            self.enemies = []  # Clear existing enemies
            # from enemy import Boss
            # boss = Boss()
            # # boss.coord = (20, 10)  # Place boss in center
            # self.enemies.append(boss)
            self.ui.palier_boss()
            self.ui.log_action(f"BOSS FINAL DU PALIER {palier}!")
            # self.ui.log_action(f"Un {boss.name} terrifiant avec {boss.health} points de vie saa mère est apparu!")
        else:
            # Normal enemy creation
            self.create_enemy(palier=palier)
        
        print(f"Enemies created: {self.enemies}")
        self.enemy_coords()

        self.ui.log_action(f"You enter in a new palier : {palier}")
        self.ui.status_label.config(text="New palier created")
        self.current_turn = "player"
        self.ui.action_label.config(text=f"Actions left: {self.player.actions}")
        print(f"New palier: {self.ui.palier}")
        self.ui.palier_label.config(text=f"Palier: {self.ui.palier}/{self.ui.MAX_PALIER}")
        self.ui.player.coord = (9, 39)

        print(f"Enemies: {self.enemies}")
        self.ui.action_label.config(text=f"Actions left: {self.player.actions}")


    def enemy_coords(self):
        """
            Check if the clicked cell contains an enemy.
        """
        position = [(0, y) for y in range(0, 40)] + [(20, y) for y in range(0, 40)] + [(x, 0) for x in range(0, 20)] + [(x, 40) for x in range(0, 20)]
        position.append((1,1))
        print(f"Cell clicked on enemy coords: {position}")
        for enemy in self.enemies:
            if enemy.coord in position:
                print("enemy coords", enemy.coord)
                # Ensure all enemies are placed on different cells
                while True:
                    x, y = randint(0, 19), randint(0, 39)
                    if (x, y) not in position:
                        enemy.coord = (x, y)
                        position.append(enemy.coord)
                        print(f"Enemy {enemy.name} moved to {enemy.coord}")
                        break

        self.ui.enemies = self.enemies
        self.act.enemies = self.enemies
        self.ui.root.after(500, self.end_turn)
        pass