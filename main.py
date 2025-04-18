from ezTK import *  # Import all components, including TOP
# from other files :
from player import Player
from enemy import Goblin, Orc, Cutiie
import random

def open_game(name):
    """
        Open the game for the selected player.
    """
    print(f"Opening game for {name}")
    game = DnDGame(name)


class DnDGame:
    def __init__(self, name):

        self.root = None
        self.player = Player(name)
        # Create some enemies
        self.enemies = [
            Cutiie(),
            # Orc()
        ]
        self.current_turn = "player"  # Start with player's turn
        self.selected_cell = None  # Track the selected cell
        self.game_over = False  # Track if the game is over
        self.interface()

    def interface(self):
        """
            Create the game interface.
        """
        global win; win = Win(title="game", bg='lightgray', inout=self.on_inout)
        self.win = win
        self.root = Frame(win, fold=2)
    
        # Create map
        self.map_frame = Frame(self.root, fold=20, width=40 * 16, height=20 * 16, bg='white', grow=False)
        # self.map_frame.pack_propagate(False)
        self.cells = []
        for col in range(40):
            col_cells = []
            for row in range(20):
                background = "#bbffbb" if (row + col) % 2 == 0 else "#ccffcc"
                cell = Brick(self.map_frame, width=16, height=16, bg=background, grow=False, state=(row, col))
                cell.bind("<Button-1>", lambda event, r=row, c=col: self.on_cell_click((r, c)))  # Bind click event
                col_cells.append(cell)
            self.cells.append(col_cells)

        # --- | event log panel | ---
        side_frame = Frame(self.root, width=400, bg='gray', grow=False, fold=2)
        status_frame = Frame(side_frame, width=400, bg='gray', grow=False, fold=1)
        Label(status_frame, text="Status", bg='gray', font="Arial 14 bold")
        self.status_case = Label(status_frame, text="On case : " + str(self.player.coord), bg='lightblue', font="Arial 12")
        self.status_name = Label(status_frame, text="Name: " + str(self.player.name), bg='lightblue', font="Arial 12")
        self.status_race = Label(status_frame, text="Race: " + str(self.player.race_name), bg='lightblue', font="Arial 12")
        self.status_classe = Label(status_frame, text="Classe: " + str(self.player.classe_name), bg='lightblue', font="Arial 12")
        self.status_health = Label(status_frame, text="Health: " + str(self.player.health), bg='lightblue', font="Arial 12")
        self.status_xp = Label(status_frame, text="XP: " + str(self.player.xp), bg='lightblue', font="Arial 12")
        event_log = Frame(side_frame, width=400, bg='lightblue', grow=False, fold=1)
        title = Frame(event_log, width=800, height=200, bg='lightblue', grow=False)
        Label(title, text="All the action of the game :", bg='gray', font="Arial 14 bold")
        frame_log = Frame(event_log, width=800, height=200, bg='lightblue' )
        self.show_event = Label(frame_log, text="curent action", bg='lightblue', font="Arial 12")


        # --- | User interface | ---
        self.action_panel = Frame(self.root, bg='lightblue', fold=1)
        self.action_label = Label(self.action_panel, text=f"Actions left: {self.player.actions}", font="Arial 14 bold", bg='lightblue')
        # Label(self.action_panel, text=f"Player: {self.player.name}", bg='lightblue', height=2, font="Arial 14 bold")

        # Game status
        self.status_label = Label(self.action_panel, text=f"Turn: {self.current_turn.capitalize()}", font="Arial 12", bg='lightblue')

        # Buttons
        Button(self.action_panel, text="Move", command=lambda: self.player_action('mouv'), bg='lightgray')
        Button(self.action_panel, text="Attack", command=lambda: self.player_action('attack'), bg='lightgray')
        # Button(self.action_panel, text="End Turn", command=self.end_turn, bg='lightgray')

        self.player.coord = (5,5)
        self.player.health = 1


        # Place enemies away from player
        # for enemy in self.enemies:
        #     while self.distance(enemy.coord, self.player.coord) < 3:
        #         enemy.coord = (random.randrange(0, 10), random.randrange(0, 20))
        # for enemy in self.enemies:
        #     while True:
        #         x, y = random.randrange(0, 10), random.randrange(0, 20)
        #         if (x, y) != self.player.coord:
        #             enemy.coord = (x, y)
        #             break
        for enemy in self.enemies:
            enemy.coord = (4,5)

        # Update the display
        self.update_game_display()
        win.loop()

    def on_inout(self, widget, code, mods):
        """Handle mouse in/out events."""
        if self.game_over:
            return None
            
        if widget.master == self.map_frame and widget.index is not None:
            row, col = widget.index
            for enemy in self.enemies:
                if enemy.coord == (col, row):
                    print(f"Mouse is over cell: ({enemy.coord}) - {enemy}")
                    self.status_case['text'] = f"On case : {enemy.coord}"
                    self.status_name['text'] = f"Name: {enemy.name}"
                    self.status_race['text'] = f"Name: {enemy.range_attack}"
                    self.status_classe['text'] = f"Name: {None}"
                    self.status_health['text'] = f"Health: {enemy.health}"
                    self.status_xp['text'] = f"XP: {None}"
                    return enemy.coord
                else:
                    self.status_case['text'] = f"On case : {self.player.coord}"
                    self.status_name['text'] = f"Name: {self.player.name}"
                    self.status_health['text'] = f"Health: {self.player.health}"
                    self.status_xp['text'] = f"XP: {self.player.xp}"
            return (row, col)
        else:
            # self.display('inout', widget.index)  # Display event parameters
            self.status_case['text'] = f"On case : {self.player.coord}"
            self.status_name['text'] = f"Name: {self.player.name}"
            self.status_health['text'] = f"Health: {self.player.health}"
            self.status_xp['text'] = f"XP: {self.player.xp}"
            return None

    def update_game_display(self):
        """Update the display to show current game state"""
        # Check if player is dead
        if self.player.health <= 0 and not self.game_over:
            self.show_game_over()
            return
            
        # Clear the map
        for row_idx, row in enumerate(self.cells):
            for col_idx, cell in enumerate(row):
                background = "#b7dfb7" if (row_idx + col_idx) % 2 == 0 else "#ccffcc"
                cell.config(bg=background, text="", border=1)

        # Show player
        x, y = self.player.coord
        self.cells[y][x].config(bg="blue", text="P", fg="white", font="Arial 12 bold", border=1)

        # Show enemies
        for enemy in self.enemies:
            print(enemy.coord)
            x, y = enemy.coord
            if 0 <= x < 20 and 0 <= y < 40:
                if isinstance(enemy, Goblin):
                    self.cells[y][x].config(bg="darkgreen", border=1)
                elif isinstance(enemy, Orc):
                    self.cells[y][x].config(bg="red", border=1)
                elif isinstance(enemy, Cutiie):
                    self.cells[y][x].config(bg="darkgreen", border=1)

        if self.player.actions <= 0:
            self.status_label.config(text="No actions left!")
            self.end_turn()
            return

    def show_game_over(self):
        """Display game over screen and provide restart option"""
        self.game_over = True
        
        # Clear the main window
        for widget in self.win.winfo_children():
            widget.destroy()
        
        # Create game over screen
        game_over_frame = Frame(self.win, width=800, height=600, bg='black',fold=3)


        
        # Game over message
        Label(game_over_frame, text="GAME OVER", font="Arial 36 bold", fg="red", bg="black")
        Label(game_over_frame, text=f"{self.player.name} has been defeated!", font="Arial 18", fg="white", bg="black")
        
        # Show stats
        stats_frame = Frame(game_over_frame, bg='black', fold=1)
        Label(stats_frame, text=f"XP earned: {self.player.xp}", font="Arial 14", fg="white", bg="black")
        Label(stats_frame, text=f"Class: {self.player.classe_name}", font="Arial 14", fg="white", bg="black")
        Label(stats_frame, text=f"Race: {self.player.race_name}", font="Arial 14", fg="white", bg="black")
        
        # Button to restart
        Button(game_over_frame, text="Play Again", font="Arial 16 bold", bg="red", fg="green", 
               command=self.restart_game)
        
        # Button to quit
        Button(game_over_frame, text="Quit", font="Arial 16 bold", bg="gray", fg="red", 
               command=lambda: self.win.exit())#win.destroy())

    def restart_game(self):
        """Restart the game with the same player name"""
        self.win.destroy()
        self.win.exit()
        open_game(self.player.name)

    def possible_coords(self, start_coord, move_distance): # todo : a ne pas modifier
        """Calculate possible coordinates within a movement distance"""
        possible_moves = []
        for dx in range(-move_distance, move_distance + 1):
            for dy in range(-move_distance, move_distance + 1):
                if dx**2 + dy**2 > move_distance**2:  # Use circular distance
                    continue
                new_x = start_coord[0] + dx
                new_y = start_coord[1] + dy
                if 0 <= new_x < 20 and 0 <= new_y < 40:
                    possible_moves.append((new_x, new_y))
        return possible_moves


    def grid_dist(self, start_coord, move_distance):
        """
        Modify the grid colors to highlight all available cells within a movement distance.
        Args:
            start_coord (tuple): Starting coordinate (x, y).
            move_distance (int): Maximum movement distance.
        """
        if self.game_over:
            return
            
        # Highlight all possible movement cells
        print(f"Highlighting cells within {move_distance} distance from {start_coord}")

        possible_moves = self.possible_coords(start_coord, move_distance)
        print(f"Possible moves, grid_dist: {possible_moves}")
        for y in range(20):
            for x in range(40):
                # print (f"Checking cell ({x}, {y})")
                if (y,x) == self.player.coord:
                        self.cells[x][y].config(bg="blue", text="P", font="Arial 12 bold", border=1)
                elif (y,x) in possible_moves:
                    if any(enemy.coord == (y, x) for enemy in self.enemies):
                        self.cells[x][y].config(bg="#c60000")  # Highlight enemy position
                    else:
                        self.cells[x][y].config(bg="#f8f8f8")
                else:
                    if any(enemy.coord == (y, x) for enemy in self.enemies):
                        self.cells[x][y].config(bg="darkgreen")
                    else:
                        background = "#74adc3" if (y + x) % 2 == 0 else "#90b577"
                        self.cells[x][y].config(bg=background)
            # print(f"Row {x} updated")
        # print("Grid distance highlighting complete")
        self.root.wait_variable(StringVar())
        self.action_panel.config(text=f"Actions left: {self.player.actions}")

        return


    def on_cell_click(self, coords: tuple[int, int]):
        """Handle cell click events."""
        if self.game_over:
            return

        if self.current_turn != "player":
            self.status_label.config(text="Not your turn!")
            return

        if self.player.actions < 0:
            print("No actions left.")
            return

        if self.action_type == "mouv":

            self.mouv(coords)
            return
        elif self.action_type == "attack":
            if any(enemy.coord == coords for enemy in self.enemies):
                self.attack(coords)
                return
            else:
                self.move_distance = self.player.bonus_range_mouv()

                self.mouv(coords)
                return


    def mouv(self, coords: tuple[int, int]):
        if self.game_over:
            return
            
        row, col = coords

        print(f"Cell clicked: ({row}, {col})")
        # self.move_distance = self.player.bonus_mouv()
        possible_moves = self.possible_coords(self.player.coord, self.move_distance)
        print(f"Possible moves: {possible_moves}")

        if coords in possible_moves:
            if any(enemy.coord == coords for enemy in self.enemies):
                print("Cell contains an enemy!")
                return
            # print (f"Valid move to {coords}")
            # Move the player to the clicked cell
            self.player.coord= coords
            print(f"Player moved to {self.player.coord}")
            # Update the display to show the new position
            # Highlight the clicked cell
            # Reset the previously selected cell if any
            if self.selected_cell:
                prev_row, prev_col = self.selected_cell
                background = "lightblue" if (prev_row + prev_col) % 2 == 0 else "lightgreen"
                self.cells[prev_row][prev_col].config(bg=background)

            self.update_game_display()
        else:
            print("Invalid move. Cell not in possible moves.")

    def attack(self, coords: tuple[int, int]):
        if self.game_over:
            return
            
        row, col = coords

        print(f"Cell clicked: ({row}, {col})")
        # self.move_distance = self.player.bonus_mouv()
        possible_attack = self.possible_coords(self.player.coord, self.attack_distance)
        print(f"Possible attack: {possible_attack}")

        if coords in possible_attack:
            if any(enemy.coord == coords for enemy in self.enemies):
                print("Cell contains an enemy!")
                print(f"Attacking enemy at {coords}")
                attack = self.player.bonus_attack()
                for enemy in self.enemies:
                    if enemy.coord == coords:
                        print("enemy attacked!", enemy)
                        test = enemy.defend(attack)
                        print(f"TEST :: Enemy {enemy} attacked for {test} damage!")
                        if enemy.health <= 0:
                            print(f"Enemy {enemy} defeated!")
                            # Remove enemy from the game
                            self.enemies.remove(enemy)
                            # Update the display to show the new position
                            self.update_game_display()
                            break
                        self.update_game_display()

                if self.selected_cell:
                    prev_row, prev_col = self.selected_cell
                    background = "lightblue" if (prev_row + prev_col) % 2 == 0 else "lightgreen"
                    self.cells[prev_row][prev_col].config(bg=background)
                    self.update_game_display()

                return

            else :
                print("Cell not contains an enemy!")


        else:
            print("Invalid move. Cell not in possible moves.")

    def end_turn(self):
        """
            End the player's turn and switch to the enemy's turn.
        """
        if self.game_over:
            return
            
        if self.current_turn == "player":
            self.current_turn = "enemies"
            self.status_label.config(text="Enemies' turn")
            self.player.actions = 2
            self.root.after(500, self.enemy_action)  # Schedule enemy turn after delay
        else:
            # Update actions display
            self.action_label.config(text=f"Actions left: {self.player.actions}")
            self.current_turn = "player"
            self.status_label.config(text="Player's turn")



    # action for each categories

    def player_action(self, action_type):
        """
            Handle player actions.
        """
        if self.game_over:
            return
            
        if self.current_turn != "player":
            self.status_label.config(text="Not your turn!")
            return

        if self.player.actions <= 0:
            print("No actions left.")
            return

        # Update actions display
        self.player.actions -= 1  # Decrease actions left

        self.action_label.config(text=f"Actions left: {self.player.actions}")

        if action_type == "mouv":
            self.action_type = "mouv"
            # Highlight all possible movement cells using grid_dist
            self.move_distance = self.player.bonus_range_mouv()
            self.grid_dist(self.player.coord, self.move_distance)
            print(f"Player action: {self.player.coord} - Move distance: {self.move_distance}")
            # self.player.action(action_type)
        else :
            self.action_type = "attack"
            self.attack_distance = self.player.bonus_range_attack()
            self.grid_dist(self.player.coord, self.attack_distance)
            print(f"Player action: {self.player.coord} - Attack distance: {self.attack_distance}")

        print(f"Player actions: {self.player.actions}")

        # Update positions on map

        self.update_game_display()

    def enemy_action(self):
        """
            Handle enemy actions.
        """
        if self.game_over:
            return

        if self.current_turn != "enemies":
            self.status_label.config(text="Player turn!")
            return

        self.show_event['text'] = "Enemy action"

        position = [self.player.coord]

        for enemy in self.enemies:
            action, data = enemy.action(position, self.player.coord)
            if action == "attack":
                position.append(enemy.coord)
                self.show_event['text'] = f"Enemy {enemy.name} \n attacks for {data} damage!"

                self.player.defensed(data)
                print(f"{enemy.name} attacks for {data} damage!")
                
                # Check if player died after this attack
                if self.player.health <= 0:
                    self.update_game_display()  # This will trigger the game over screen
                    return  # Exit enemy action loop if player is dead
                    
            if action == "mouv":
                position.append(enemy.coord)

            print(f"{enemy.name} action: {action}, data: {data}")
            # Update display after each enemy acts

        # Add a delay between enemy actions
        self.root.after(50, None)

        # End enemy turn

        if not self.enemies:
            print("No enemies left. Creating new enemies...")
            enemy_type = random.choice([Cutiie])
            enemy_nb = random.randint(1, 10)
            for _ in range(enemy_nb):  # Create 2 new enemies
                self.enemies.append(enemy_type())
            for enemy in self.enemies:
                while True:
                    x, y = random.randrange(0, 20), 0
                    if (x, y) != self.player.coord and all(e.coord != (x, y) for e in self.enemies):
                        enemy.coord = (x, y)
                        break
        self.update_game_display()

        self.root.after(500, self.end_turn)
        pass

if __name__ == "__main__":
    open_game("fg")