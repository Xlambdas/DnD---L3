from ezTK import *  # Import all components, including TOP
from random import randint, random, choice, shuffle  # Import random functions
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
            Cutiie(), Cutiie(), Cutiie()
        ]
        self.is_final_boss = False  # Track if the final boss is active
        self.action_type = None  # Track the current action type
        self.current_turn = "player"  # Start with player's turn
        self.selected_cell = None  # Track the selected cell
        self.game_over = False  # Track if the game is over
        self.ui = GameInterface(self)  # Create the game interface
        self.act = GameActions(self, self.ui)  # Create the game actions handler
        self.ui.interface()

    def player_act(self, action_type):
        print(f"game - Player action: {action_type}")
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

        print(f"Cell clicked oncellclick 1 - action type : {self.action_type}")

        if self.action_type == "mouv":
            print(f"Cell clicked: {self.action_type} - {coords}")
            self.act.mouv(coords)
            self.action_type = "None"
            return
        elif self.action_type == "attack":
            if any(enemy.coord == coords for enemy in self.enemies):
                # print(f"get enemy at {coords}, or {self.enemies}")
                self.act.attack(coords)
                # print(f"Attacking enemy at {coords}")
                self.action_type = "None"
                return
            else:
                self.move_distance = self.player.bonus_range_mouv()
                # print(f"Cell clicked: {self.action_type} - {coords}")
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

    def reset_game(self, keep_progress=False, skip_ui_updates=False):
        """
        Reset the game state to start a new game
        
        Args:
            keep_progress (bool): If True, keep the player's palier and just restore health
                                If False, reset to palier 1 (but XP will be managed by caller)
            skip_ui_updates (bool): If True, skip any UI updates during reset
        """
        # Save XP and palier in case we need them
        saved_xp = self.player.xp
        saved_palier = self.player.palier
        
        # Reset player health and actions
        self.player.health = 105  # self.player.max_health
        self.player.actions = 2   # self.player.max_actions
        
        if keep_progress:
            # Continue from current palier (after death)
            self.player.palier = saved_palier
            self.player.xp = saved_xp
        else:
            # Start from beginning (after winning)
            self.player.palier = 1
            # XP is reset here, but caller will restore it if needed
            self.player.xp = 0
        
        # Reset player position to starting position
        self.player.coord = (9, 39)
        
        # Reset enemy list with new enemies
        self.enemies = []
        
        # Créer les ennemis, mais sans mettre à jour l'UI
        if skip_ui_updates:
            enemy_count = 3 * self.player.palier
            player_level = self.player.level
            
            # Déterminer les types d'ennemis basés sur le palier
            from enemy import Cutiie, Goblin, Orc
            
            enemy_types = []
            if self.player.palier <= 2:
                enemy_types = [Cutiie]
            elif self.player.palier <= 3:
                enemy_types = [Cutiie, Goblin]
            else:
                enemy_types = [Cutiie, Goblin, Orc]
                
            # Créer les ennemis sans mettre à jour l'UI
            for _ in range(enemy_count):
                enemy_class = random.choice(enemy_types)
                enemy = enemy_class()
                
                # Ajuster les statistiques en fonction du niveau
                if player_level > 1:
                    enemy.health = int(enemy.health * (1 + 0.1 * player_level))
                    enemy.strength = int(enemy.strength * (1 + 0.05 * player_level))
                    enemy.xp_value = int(enemy.xp_value * (1 + 0.1 * player_level))
                    
                # Position aléatoire pour l'ennemi (à éviter les murs et le joueur)
                enemy.coord = (randint(1, 18), randint(1, 38))
                self.enemies.append(enemy)
        else:
            # Utiliser la méthode standard avec mise à jour de l'UI
            self.create_enemy(self.player.palier)
        
        # Reset game state
        self.game_over = False
        self.is_final_boss = False
        self.current_turn = "player"
        self.action_type = None
        self.selected_cell = None    


    def create_enemy(self, palier):
        """
            Create a new enemy of the specified type.
        """
        self.enemies = []
        enemy_types = []
        player_level = self.player.level

        if palier <= 2:
            enemy_types = [Cutiie]
        elif palier <= 3:
            enemy_types = [Cutiie, Goblin]
        else:
            enemy_types = [Cutiie, Goblin, Orc]
        enemy_count = 3 * palier

        for _ in range(enemy_count):
            enemy_class = random.choice(enemy_types)
            enemy = enemy_class()

            # Ajuster les statistiques en fonction du niveau
            if player_level > 1:
                enemy.health = int(enemy.health * (1 + 0.1 * player_level))
                enemy.strength = int(enemy.strength * (1 + 0.05 * player_level))
                enemy.xp_value = int(enemy.xp_value * (1 + 0.1 * player_level))
            self.enemies.append(enemy)
        
        # Vérifier si l'interface est disponible avant de mettre à jour le log
        if hasattr(self, 'ui') and self.ui is not None:
            try:
                self.ui.log_action(f"{enemy_count} nouveaux ennemis sont apparus!")
            except Exception as e:
                print(f"Error logging action: {e}")
                # Continue sans planter en cas d'erreur
                
    def new_palier(self, palier):

        """
            Create a new palier of enemies.
        """
        print(f"Creating new palier: {palier}")

        self.create_enemy(palier=palier)
        # print(f"Enemies created: {self.enemies}")
        self.enemy_coords()

        self.ui.log_action(f"You enter in a new palier : {palier}")
        self.ui.status_label.config(text="New palier created")
        self.current_turn = "player"
        self.ui.action_label.config(text=f"Actions left: {self.player.actions}")
        # print(f"New palier: {self.ui.palier}")
        self.ui.palier_label.config(text=f"Palier: {self.ui.palier}/{self.ui.MAX_PALIER}")
        self.ui.player.coord = (9, 39)
        self.player.palier = self.ui.palier
        self.player.set_bdd()


        # print(f"Enemies: {self.enemies}")
        self.ui.action_label.config(text=f"Actions left: {self.player.actions}")


    def enemy_coords(self):
        """
            Check if the clicked cell contains an enemy.
        """
        position = [(0, y) for y in range(0, 40)] + [(20, y) for y in range(0, 40)] + [(x, 0) for x in range(0, 20)] + [(x, 40) for x in range(0, 20)]
        position.append((1,1))
        # print(f"Cell clicked on enemy coords: {position}")
        for enemy in self.enemies:
            if enemy.coord in position:
                # print("enemy coords", enemy.coord)
                # Ensure all enemies are placed on different cells
                while True:
                    x, y = randint(0, 19), randint(0, 39)
                    if (x, y) not in position:
                        enemy.coord = (x, y)
                        position.append(enemy.coord)
                        # print(f"Enemy {enemy.name} moved to {enemy.coord}")
                        break

        self.ui.enemies = self.enemies
        self.act.enemies = self.enemies
        self.ui.root.after(500, self.end_turn)
        pass

    def boss_palier(self):
        """
            Create the final boss.
        """
        self.is_final_boss = True

        self.enemies = [Boss()]
        self.ui.log_action(f"You enter in the final boss !")
        self.current_turn = "player"
        self.ui.action_label.config(text=f"Actions left: {self.player.actions}")
        print(f"Final boss: {self.ui.palier}")
        self.ui.palier_label.config(text=f"Palier: {self.ui.palier}/{self.ui.MAX_PALIER}")
        self.ui.player.coord = (9, 39)
        self.ui.enemies = self.enemies
        self.act.enemies = self.enemies
        self.ui.update_boss_display()
        self.ui.root.after(500, self.end_turn)
        pass