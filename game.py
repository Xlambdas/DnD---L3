from ezTK import *
from random import randint, random, choice, shuffle
# from other files :
from player import Player
from enemy import Goblin, Orc, Cutiie, Boss, Dragon, Vampire, Troll
from interface import GameInterface
from actions import GameActions

class DNDGame:
    def __init__(self, name):
        self.player = Player(name)
        self.__create_enemy(palier=self.player.palier)
        self.is_final_boss = False
        self.action_type = None
        self.current_turn = "player"
        self.selected_cell = None
        self.game_over = False
        self.ui = GameInterface(self)
        self.act = GameActions(self, self.ui)
        self.ui.interface()

    def player_act(self, action_type):
        print(f"game - Player action: {action_type}")
        self.act.player_action(action_type)


    def possible_coords(self, start_coord, move_distance):
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

        print(f"class dndgame - Cell clicked oncellclick 1 - action type : {self.action_type}")

        if self.action_type == "mouv":
            print(f"Cell clicked: {self.action_type} - {coords}")
            self.act.mouv(coords)
            if not self.act.mouv(coords):
                print("Invalid move!")
                return
            else:
                self.action_type = "None"
                return
        elif self.action_type == "attack":
            if any(enemy.coord == coords for enemy in self.enemies):
                self.act.attack(coords)
                if not self.act.attack(coords):
                    print("Invalid attack!")
                    return
                else:
                    self.action_type = "None"
                    return
            else:
                self.move_distance = self.player.bonus_range_mouv()
                self.act.mouv(coords)
                if not self.act.mouv(coords):
                    print("Invalid move!")
                    return
                else:
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
            self.ui.root.after(500, self.act.enemy_action)
        else:
            # Update actions display
            self.ui.action_label.config(text=f"Actions left: {self.player.actions}")
            self.current_turn = "player"
            self.ui.status_label.config(text="Player's turn")


    def __create_enemy(self, palier):
        """
            Create a new enemy of the specified type.
        """
        self.enemies = []
        enemy_types = []
        player_level = self.player.level

        if self.player.palier <= 2:
                enemy_types = [Cutiie]
        elif self.player.palier <= 3:
            enemy_types = [Cutiie, Goblin]
        elif self.player.palier <= 4:
            enemy_types = [Goblin, Orc, Troll]
        elif self.player.palier <= 5:
            enemy_types = [Dragon, Vampire]
        else:
            enemy_types = [Boss]
        enemy_count = 3 * palier


        for _ in range(enemy_count):
            enemy_class = random.choice(enemy_types)
            enemy = enemy_class()

            if player_level > 1:
                enemy.health = int(enemy.health * (1 + 0.1 * player_level))
                enemy.strength = int(enemy.strength * (1 + 0.05 * player_level))
                enemy.xp_value = int(enemy.xp_value * (1 + 0.1 * player_level))
            self.enemies.append(enemy)

        if hasattr(self, 'ui') and self.ui is not None:
            try:
                self.ui.log_action(f"{enemy_count} nouveaux ennemis sont apparus!")
            except Exception as e:
                print(f"Error logging action: {e}")


    def new_palier(self, palier):

        """
            Create a new palier of enemies.
        """
        print(f"Creating new palier: {palier}")

        self.__create_enemy(palier=palier)
        self.__enemy_coords()

        self.ui.log_action(f"You enter in a new palier : {palier}")
        self.ui.status_label.config(text="New palier created")
        self.current_turn = "player"
        self.ui.action_label.config(text=f"Actions left: {self.player.actions}")
        self.ui.palier_label.config(text=f"Palier: {self.ui.palier}/{self.ui.MAX_PALIER}")
        self.ui.player.coord = (9, 39)
        self.player.palier = self.ui.palier
        self.player.set_bdd()

        self.ui.action_label.config(text=f"Actions left: {self.player.actions}")


    def __enemy_coords(self):
        """
            Check if the clicked cell contains an enemy.
        """
        position = [(0, y) for y in range(0, 40)] + [(20, y) for y in range(0, 40)] + [(x, 0) for x in range(0, 20)] + [(x, 40) for x in range(0, 20)]
        position.append((1,1))
        for enemy in self.enemies:
            if enemy.coord in position:
                # Ensure all enemies are placed on different cells
                while True:
                    x, y = randint(0, 19), randint(0, 39)
                    if (x, y) not in position:
                        enemy.coord = (x, y)
                        position.append(enemy.coord)
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
        self.player.actions = 2
        self.ui.enemies = self.enemies
        self.act.enemies = self.enemies
        self.ui.update_boss_display()
        return


    def reset_game(self, keep_progress=False, skip_ui_updates=False):
        """
        Reset the game state to start a new game
        Args:
            keep_progress (bool): If True, keep the player's palier and just restore health
                                If False, reset to palier 1 (but XP will be managed by caller)
            skip_ui_updates (bool): If True, skip any UI updates during reset
        """
        saved_xp = self.player.xp
        saved_palier = self.player.palier
        self.player.health = 105
        self.player.actions = 2

        if keep_progress:
            self.player.palier = saved_palier
            self.player.xp = saved_xp
        else:
            self.player.palier = 1
            self.player.xp = 0

        self.player.coord = (9, 39)
        self.enemies = []
        if skip_ui_updates:
            enemy_count = 3 * self.player.palier
            player_level = self.player.level

            enemy_types = []
            if self.player.palier <= 2:
                enemy_types = [Cutiie]
            elif self.player.palier <= 3:
                enemy_types = [Cutiie, Goblin]
            elif self.player.palier <= 4:
                enemy_types = [Goblin, Orc, Troll]
            elif self.player.palier <= 5:
                enemy_types = [Dragon, Vampire]
            else:
                enemy_types = [Boss]

            for _ in range(enemy_count):
                enemy_class = random.choice(enemy_types)
                enemy = enemy_class()

                if player_level > 1:
                    enemy.health = int(enemy.health * (1 + 0.1 * player_level))
                    enemy.strength = int(enemy.strength * (1 + 0.05 * player_level))
                    enemy.xp_value = int(enemy.xp_value * (1 + 0.1 * player_level))

                enemy.coord = (randint(1, 18), randint(1, 38))
                self.enemies.append(enemy)
        else:
            self.create_enemy(self.player.palier)

        # Reset game state
        self.game_over = False
        self.is_final_boss = False
        self.current_turn = "player"
        self.action_type = None
        self.selected_cell = None

