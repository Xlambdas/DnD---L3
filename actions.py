from enemy import Boss

class GameActions:
    def __init__(self, game, ui):
        self.game = game
        self.ui = ui
        self.player = self.game.player
        self.enemies = self.game.enemies


    def player_action(self, action_type):
        """ Handle player actions."""
        if self.game.game_over or self.game.current_turn != "player":
            self.ui.status_label.config(text="Not your turn!")
            return

        if self.player.actions <= 0:
            self.ui.status_label.config(text="No actions left.")
            return

        self.player.actions -= 1
        self.ui.action_label.config(text=f"Actions left: {self.player.actions}")

        if action_type == "mouv":
            self.game.action_type = "mouv"
            self.move_distance = self.player.bonus_range_mouv()
            self.ui.grid_dist(self.player.coord, self.move_distance)
            self.ui.log_action(f"You move to {self.player.coord}")
        elif action_type == "attack":
            self.game.action_type = "attack"
            self.attack_distance = self.player.bonus_range_attack()
            self.ui.grid_dist(self.player.coord, self.attack_distance)

        self.ui.update_game_display()

    def mouv(self, coords: tuple[int, int]):
        """ Handle player movement."""
        if self.game.game_over:
            return

        if coords in self.game.possible_coords(self.player.coord, self.move_distance):
            if any(enemy.coord == coords for enemy in self.enemies):
                print("Cell contains an enemy!")
                return

            self.player.coord = coords
            self.ui.update_game_display()
            return True
        else:
            print("Invalid move. Cell not in possible moves.")
            return False

    def attack(self, coords: tuple[int, int]):
        """ Handle player attack."""
        if self.game.game_over:
            return False

        if coords in self.game.possible_coords(self.player.coord, self.attack_distance):
            if any(enemy.coord == coords for enemy in self.enemies):
                attack = self.player.bonus_attack()
                for enemy in self.enemies:
                    if enemy.coord == coords:
                        enemy.player_level = self.player.level
                        action, damage = enemy.defend(attack)

                        if enemy.health <= 0:
                            self.player.gain_xp(enemy.xp_value)
                            self.ui.log_action(f"You killed {enemy.name}!")
                            self.enemies.remove(enemy)
                        else:
                            self.ui.log_action(f"You attacked {enemy.name} for {damage} damage!")

                        self.ui.update_game_display()
                        return True
                print("Cell not contains an enemy!")
                return False
        else:
            print("Invalid move. Cell not in possible moves.")
            return False

    def enemy_action(self):
        """ Handle enemy actions."""
        if self.game.game_over or self.game.current_turn != "enemies":
            self.ui.status_label.config(text="Player turn!")
            return

        position = [self.player.coord]
        for enemy in self.enemies:
            if self.game.is_final_boss:
                print("Final boss phase")
                if isinstance(enemy, Boss):
                    if enemy.ability == None:
                        print(f"enemy_action - Boss action: {enemy.ability}")
                        enemy.get_attack()
                        boss_attack_type = enemy.ability
                        self.__grid_boss_next_attack(boss_attack_type)
                        self.ui.log_action(f"Boss prepares a {boss_attack_type} attack!")
                    elif enemy.ability == "Fireball":
                        print(f"enemy_action (elif) - Boss action: {enemy.ability}")
                        # enemy.get_attack()
                        boss_attack_type = enemy.ability
                        self.__show_boss_attack(boss_attack_type)
                        self.ui.log_action(f"Boss uses {boss_attack_type} attack!")
                        enemy.ability = None
                    if self.player.health <= 0:
                        self.ui.update_game_display()  # This will trigger the game over screen
                        return
                    self.ui.root.after(50, None)

                    self.ui.update_boss_display()
                    self.ui.root.after(500, self.game.end_turn)
                return

            action, data = enemy.action(position, self.player.coord)
            if action == "attack":
                position.append(enemy.coord)
                dmg = self.player.defensed(data)
                self.ui.get_damage()
                self.ui.log_action(f"{enemy.name} attacks you !")
                self.ui.log_action(f"You defend and take {dmg} damage!")
                self.ui.update_game_display()

                # Check if player died after this attack

                if self.player.health <= 0:
                    self.ui.update_game_display()  # This will trigger the game over screen
                    return  # Exit enemy action loop if player is dead

            if action == "mouv":
                position.append(enemy.coord)

            print(f"{enemy.name} action: {action}, data: {data}")

        self.ui.root.after(50, None)
        self.ui.update_game_display()
        self.ui.root.after(500, self.game.end_turn)
        return

    def __grid_boss_next_attack(self, attack_type):
        """ Show the next boss attack."""
        if attack_type == "Fireball":
            player_x, player_y = self.player.coord
            boss = next((enemy for enemy in self.enemies if isinstance(enemy, Boss)), None)
            if boss:
                boss_x, boss_y = boss.coord
                position = []
                MAX_X = 19
                MAX_Y = 39

                # 1: horizontal attack
                if player_x == boss_x:
                    step = 1 if player_y > boss_y else -1
                    for y in range(boss_y + step, MAX_Y if step == 1 else 0, step):
                        for offset in range(3):
                            position.append((boss_x - 1 + offset, y))

                # 2: vertical attack
                elif player_y == boss_y:
                    step = 1 if player_x > boss_x else -1
                    for x in range(boss_x + step, MAX_X if step == 1 else 0, step):
                        for offset in range(3):
                            position.append((x, boss_y - 1 + offset))

                # 3: Diagonal or any other position
                else:
                    dx = 1 if player_x > boss_x else -1
                    dy = 1 if player_y > boss_y else -1

                    rise = abs(player_y - boss_y)
                    run = abs(player_x - boss_x)

                    x, y = boss_x + dx, boss_y + dy

                    is_more_horizontal = run > rise
                    x, y = boss_x + dx, boss_y + dy

                    # Use Bresenham's line algorithm (enhanced by claude AI)
                    error = 0
                    if is_more_horizontal:
                        error_step = rise / run
                        while 0 < x < MAX_X and 0 < y < MAX_Y:
                            for offset in range(3):
                                offset_y = y - 1 + offset
                                if 0 < offset_y < MAX_Y:
                                    position.append((x, offset_y))
                            error += error_step
                            x += dx
                            if error >= 0.5:
                                y += dy
                                error -= 1.0
                    else:
                        error_step = run / rise
                        while 0 < x < MAX_X and 0 < y < MAX_Y:
                            for offset in range(3):
                                offset_x = x - 1 + offset
                                if 0 < offset_x < MAX_X:
                                    position.append((offset_x, y))
                            error += error_step
                            y += dy
                            if error >= 0.5:
                                x += dx
                                error -= 1.0

                boss.attack_pos = position
                return position

        elif attack_type == "meteor":
            # todo
            pass
        else:
            print("Unknown boss attack type!")

    def __show_boss_attack(self, attack_type="Fireball"):
        """
        Show the boss attack with an animation.
        """
        boss = next((enemy for enemy in self.enemies if isinstance(enemy, Boss)), None)
        if not boss or not hasattr(boss, "attack_pos"):
            print("No boss or attack position not set!")
            return

        position = boss.attack_pos
        # Initialize burned_cells attribute if it doesn't exist
        if not hasattr(self, 'burned_cells'):
            self.burned_cells = {}

        if attack_type == "Fireball":
            boss_x, boss_y = boss.coord
            sorted_cells = sorted(position, key=lambda cell: abs(cell[0] - boss_x) + abs(cell[1] - boss_y))

            # Create animation in waves from boss to player
            cell_groups = []
            current_distance = 0
            current_group = []

            for cell in sorted_cells:
                cell_distance = abs(cell[0] - boss_x) + abs(cell[1] - boss_y)
                if cell_distance > current_distance:
                    if current_group:
                        cell_groups.append(current_group)
                    current_group = [cell]
                    current_distance = cell_distance
                else:
                    current_group.append(cell)

            if current_group:
                cell_groups.append(current_group)

            # Animation phases: prepare, execute, fade
            self.ui.animate_attack_prepare(cell_groups)
            self.ui.animate_attack_execute(cell_groups, attack_type)
            self.ui.animate_attack_fade(position)

            player_x, player_y = self.player.coord
            if (player_x, player_y) in position:
                boss.get_attack()
                self.player.defensed(boss.dmg)
                self.ui.get_damage()
