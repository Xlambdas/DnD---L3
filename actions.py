import random
from enemy import Cutiie

class GameActions:
    def __init__(self, game, ui):
        self.game = game
        self.ui = ui
        self.player = self.game.player
        self.enemies = self.game.enemies

    def player_action(self, action_type):
        """
        Handle player actions.
        """
        if self.game.game_over:
            return

        if self.game.current_turn != "player":
            self.ui.status_label.config(text="Not your turn!")
            return

        if self.player.actions <= 0:
            print("No actions left.")
            return

        # Update actions display
        self.player.actions -= 1  # Decrease actions left
        self.ui.action_label.config(text=f"Actions left: {self.player.actions}")
        print(f"Player actions: {action_type}")
        if action_type == "mouv":
            self.game.action_type = "mouv"
            # Highlight all possible movement cells using grid_dist
            self.move_distance = self.player.bonus_range_mouv()
            self.ui.grid_dist(self.player.coord, self.move_distance)
            print(f"Player action: {self.player.coord} - Move distance: {self.move_distance}")
            self.ui.log_action(f"You move to {self.player.coord}")

        else:
            self.game.action_type = "attack"
            self.attack_distance = self.player.bonus_range_attack()
            self.ui.grid_dist(self.player.coord, self.attack_distance)
            print(f"Player action: {self.player.coord} - Attack distance: {self.attack_distance}")

        print(f"Player actions: {self.player.actions}")

        # Update positions on map
        self.ui.update_game_display()

    def mouv(self, coords: tuple[int, int]):
        if self.game.game_over:
            return
        row, col = coords
        possible_moves = self.game.possible_coords(self.player.coord, self.move_distance)
        # print(f"Possible moves: {possible_moves}")

        if coords in possible_moves:
            if any(enemy.coord == coords for enemy in self.enemies):
                print("Cell contains an enemy!")
                return

            # Move the player to the clicked cell
            self.player.coord= coords
            # print(f"Player moved to {self.player.coord}")
            self.ui.log_action(f"You move to {self.player.coord}")

            # Update the display to show the new position
            # Highlight the clicked cell
            # Reset the previously selected cell if any
            if self.game.selected_cell:
                prev_row, prev_col = self.game.selected_cell
                background = "lightblue" if (prev_row + prev_col) % 2 == 0 else "lightgreen"
                self.ui.cells[prev_row][prev_col].config(bg=background)

            self.ui.update_game_display()
        else:
            print("Invalid move. Cell not in possible moves.")

    def attack(self, coords: tuple[int, int]):
        if self.game.game_over:
            return

        row, col = coords

        # print(f"Cell clicked on attack class action: ({row}, {col})")
        # self.move_distance = self.player.bonus_mouv()
        possible_attack = self.game.possible_coords(self.player.coord, self.attack_distance)
        # print(f"Possible attack: {possible_attack}")

        if coords in possible_attack:
            if any(enemy.coord == coords for enemy in self.enemies):
                attack = self.player.bonus_attack()
                for enemy in self.enemies:
                    if enemy.coord == coords:
                        enemy.player_level = self.player.level

                        # print("enemy attacked!", enemy)
                        action, data = enemy.defend(attack)
                        # print(f"TEST :: Enemy {enemy} attacked for {data} damage!")

                        if enemy.health <= 0:
                            print(f"Enemy {enemy} defeated!")
                            self.player.gain_xp(enemy.xp_value)

                            # Remove enemy from the game
                            self.ui.log_action(f"You killed {enemy.name}!")
                            self.enemies.remove(enemy)
                            # Update the display to show the new position
                            self.ui.update_game_display()
                            break
                        else:
                            self.ui.log_action(f"You attacked {enemy.name} for {data} damage!")
                            # Update the display to show the new position
                            self.ui.update_game_display()
                            break


                if self.game.selected_cell:
                    prev_row, prev_col = self.game.selected_cell
                    background = "lightblue" if (prev_row + prev_col) % 2 == 0 else "lightgreen"
                    self.ui.cells[prev_row][prev_col].config(bg=background)
                    self.ui.update_game_display()

                return

            else :
                print("Cell not contains an enemy!")


        else:
            print("Invalid move. Cell not in possible moves.")


    # action for each categories

    # def player_action(self, action_type):
    #     """
    #         Handle player actions.
    #     """
    #     if self.game.game_over:
    #         return

    #     if self.game.current_turn != "player":
    #         self.ui.status_label.config(text="Not your turn!")
    #         return

    #     if self.player.actions <= 0:
    #         print("No actions left.")
    #         return

    #     # Update actions display
    #     self.player.actions -= 1  # Decrease actions left

    #     self.ui.action_label.config(text=f"Actions left: {self.player.actions}")

    #     if action_type == "mouv":
    #         self.game.action_type = "mouv"
    #         # Highlight all possible movement cells using grid_dist
    #         self.move_distance = self.player.bonus_range_mouv()
    #         self.game.grid_dist(self.player.coord, self.move_distance)
    #         print(f"Player action: {self.player.coord} - Move distance: {self.move_distance}")
    #         # self.player.action(action_type)
    #         self.ui.log_action(f"You move to {self.player.coord}")

    #     else :
    #         self.action_type = "attack"
    #         self.attack_distance = self.player.bonus_range_attack()
    #         self.game.grid_dist(self.player.coord, self.attack_distance)
    #         print(f"Player action: {self.player.coord} - Attack distance: {self.attack_distance}")

    #     print(f"Player actions: {self.player.actions}")

    #     # Update positions on map

    #     self.ui.update_game_display()

    def enemy_action(self):
        """
            Handle enemy actions.
        """
        if self.game.game_over:
            return

        if self.game.current_turn != "enemies":
            self.ui.status_label.config(text="Player turn!")
            return

        position = [self.player.coord]

        for enemy in self.enemies:
            action, data = enemy.action(position, self.player.coord)
            if action == "attack":
                position.append(enemy.coord)
                if self.game.is_final_boss:
                    boss_attack_type = enemy.get_attack_type()
                    self.ui.log_action(f"Boss {enemy.name} prepares a {boss_attack_type} attack!")
                dmg = self.player.defensed(data)
                self.ui.log_action(f"You defend and take {dmg} damage!")

                # Check if player died after this attack
                if self.game.is_final_boss:
                    print(f"Boss {enemy.name} prepares a {boss_attack_type} attack!")
                    # Allow the player to move and avoid the attack
                if self.player.health <= 0:
                    self.ui.update_game_display()  # This will trigger the game over screen
                    return  # Exit enemy action loop if player is dead

            if action == "mouv":
                position.append(enemy.coord)

            print(f"{enemy.name} action: {action}, data: {data}")


        self.ui.root.after(50, None)

        self.ui.update_game_display()
        self.ui.root.after(500, self.game.end_turn)
        pass

