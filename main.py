from ezTK import *
# from other files :
from player import Player

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
<<<<<<< Updated upstream
        self.interface()

    def interface(self):
        self.root = Win(title="game", width=600, height=400, bg='lightgray', fold=10)
        # creation of the map :
        self.map_frame = Frame(self.root, fold=10, bg='white')
        for row in range(20):
            for col in range(10):
                background = "lightblue" if (row + col) % 2 == 0 else "lightgreen"
                Label(self.map_frame, text="", width=4, height=2, relief="ridge", bg=background)
=======
        # Create some enemies
        self.enemies = [
            Goblin(),
            # Orc()
        ]
        self.current_turn = "player"  # Start with player's turn
        self.selected_cell = None  # Track the selected cell
        self.interface()
    
    def restart_game(self):
        """Restart the game by recreating everything"""
        # Clear current window contents
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Reset game state
        self.__init__(self.name)  # Reinitialize with the same name

    def interface(self):
        """
            Create the game interface.
        """
        global root; root = Win(title="game", width=600, height=400, bg='lightgray', fold=10)
        self.root = root

        # Create map
        self.map_frame = Frame(self.root, fold=10, bg='white')
        self.cells = []
        for col in range(20):
            col_cells = []
            for row in range(10):
                background = "lightblue" if (row + col) % 2 == 0 else "lightgreen"
                cell = Brick(self.map_frame, width=32, height=32, border=2, relief="ridge", bg=background, state=(row, col))
                cell.bind("<Button-1>", lambda event, r=row, c=col: self.on_cell_click((r, c)))  # Bind click event
                col_cells.append(cell)
            self.cells.append(col_cells)

        # User interface
        self.action_panel = Frame(self.root, width=150, bg='lightblue')
<<<<<<< Updated upstream
        Label(self.action_panel, text=f"Actions left :{self.player.actions}", font="Arial 14 bold", bg='lightblue')
        Label(self.action_panel, text=f"Player: {self.player.name}", bg='lightblue')
        Button(self.action_panel, text="Move", command=lambda: (
            self.player.action('mouv'),
            ), bg='lightgray')
        Button(self.action_panel, text="Attack", command=lambda: (
            self.player.action('attack'),
            ), bg='lightgray')
        Button(self.action_panel, text="Inventory")#, command=self.inventory_action, bg='lightgray')
        Button(self.action_panel, text="End Turn")#, command=self.end_turn_action, bg='lightgray')
        self.root.loop()


=======
        self.action_label = Label(self.action_panel, text=f"Actions left: {self.player.actions}", font="Arial 14 bold", bg='lightblue')
        Label(self.action_panel, text=f"Player: {self.player.name}", bg='lightblue', height=2, font="Arial 14 bold")
        
        # Game status
        self.status_label = Label(self.action_panel, text=f"Turn: {self.current_turn.capitalize()}", font="Arial 12", bg='lightblue')
        
        # Buttons
        Button(self.action_panel, text="Move", command=lambda: self.player_action('mouv'), bg='lightgray')
        Button(self.action_panel, text="Attack", command=lambda: self.player_action('attack'), bg='lightgray')
        Button(self.action_panel, text="End Turn", command=self.end_turn, bg='lightgray')
        
        # Randomize player position
        # self.player.coord_player = (random.randrange(0, 10), random.randrange(0, 20))
        self.player.coord_player = (5,5)
        
        # Place enemies away from player
        # for enemy in self.enemies:
        #     while self.distance(enemy.coord, self.player.coord_player) < 3:
        #         enemy.coord = (random.randrange(0, 10), random.randrange(0, 20))
        for enemy in self.enemies:
            enemy.coord = ((4,4))
        # Update the display
        self.update_game_display()
        self.root.loop()

    def on_cell_click(self, coords: tuple[int, int]):
            """Handle cell click events."""
            row, col = coords
            print(f"Cell clicked: ({row}, {col})")
            if self.current_turn != "player":
                self.status_label.config(text="Not your turn!")
                return
            
            # if self.actions <= 0:
            #     print("No actions left.")
            # return None
            self.player.actions -= 1  # Decrease actions left
            possible_moves = self.possible_coords(self.player.coord_player, move_distance=2)
            print(f"Possible moves: {possible_moves}")

            if coords in possible_moves:
                print (f"Valid move to {coords}")
                # Move the player to the clicked cell
                self.player.coord_player = coords
                print(f"Player moved to {self.player.coord_player}")
                # Update the display to show the new position
                self.update_game_display()
                # Highlight the clicked cell
                # Reset the previously selected cell if any
                if self.selected_cell:
                    prev_row, prev_col = self.selected_cell
                    background = "lightblue" if (prev_row + prev_col) % 2 == 0 else "lightgreen"
                    self.cells[prev_row][prev_col].config(bg=background)

                # Highlight the clicked cell in yellow
                self.cells[row][col].config(bg="yellow")
                self.selected_cell = (row, col)
                self.player.coord_player = coords
                self.update_game_display()
            else:
                print("Invalid move. Cell not in possible moves.")


    def distance(self, coord1, coord2):
        """Calculate Manhattan distance between two coordinates"""
        x1, y1 = coord1
        x2, y2 = coord2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def possible_coords(self, start_coord, move_distance):
        """Calculate possible coordinates within a movement distance"""
        possible_moves = []
        for dx in range(-move_distance, move_distance + 1):
            for dy in range(-move_distance, move_distance + 1):
                if abs(dx) + abs(dy) > move_distance:
                    continue
                new_x = start_coord[0] + dx
                new_y = start_coord[1] + dy
                if 0 <= new_x < 10 and 0 <= new_y < 20:
                    possible_moves.append((new_x, new_y))
        return possible_moves

    def grid_dist(self, start_coord, move_distance):
        """
        Modify the grid colors to highlight all available cells within a movement distance.
        Args:
            start_coord (tuple): Starting coordinate (x, y).
            move_distance (int): Maximum movement distance.
        """
        # Highlight all possible movement cells
        print(f"Highlighting cells within {move_distance} distance from {start_coord}")

        possible_moves = self.possible_coords(start_coord, move_distance)
        print(f"Possible moves, grid_dist: {possible_moves}")
        for x in range(20):
            for y in range(10):
                if (x, y) in possible_moves and (x, y) != self.player.coord_player:
                    # Highlight available cells in gray
                    if any(enemy.coord == (x, y) for enemy in self.enemies):
                        self.cells[x][y].config(bg="red")  # Highlight enemy position
                    else:
                        # print("test cell")
                        self.cells[x][y].config(bg="lightgray")
                else:
                    # Keep the original color for other cells
                    background = self.cells[x][y].cget("bg")
                    self.cells[y][x].config(bg=background)

        # for x in range(20):
        #     for y in range(10):
        #         # print(f"Checking cell ({x}, {y})")
        #         if (x, y) in possible_moves and (x, y) != self.player.coord_player:
        #             # Check if the cell is occupied by an enemy
        #             # print(f"Cell ({x}, {y}) is a possible move")
        #             if any(enemy.coord == (x, y) for enemy in self.enemies):
        #                 self.cells[x][y].config(bg="red")  # Highlight enemy position
        #             else:
        #                 # print("test cell")
        #                 self.cells[x][y].config(bg="lightgray")
        #         else:
        #             print(f"Cell ({x}, {y}) is not a possible move")
        #             # Keep the previous color
        #             background = self.cells[x][y].cget("bg")
        #             self.cells[x][y].config(bg=background)
        # # self.update_game_display()


    def player_action(self, action_type):
        """Handle player action"""
        if self.current_turn != "player":
            self.status_label.config(text="Not your turn!")
            return

        if action_type == "mouv":
            # Highlight all possible movement cells using grid_dist
            self.grid_dist(self.player.coord_player, move_distance=2)
            print(f"Player action: {action_type}")
            # self.player.action(action_type)
        else :
            self.player.action(action_type)

        # Update actions display
        self.action_label.config(text=f"Actions left: {self.player.actions}")
        
        # Update positions on map
        self.update_game_display()
        
        # If player has no actions left, end turn
        if self.player.actions <= 0:
            self.end_turn()

    def end_turn(self):
        """End current turn and switch to next"""
        if self.current_turn == "player":
            self.current_turn = "enemies"
            self.status_label.config(text="Enemies' turn")
            self.player.actions = 2  # Reset player actions for next turn
            self.root.after(500, self.enemy_turn)  # Schedule enemy turn after delay
        else:
            # Update actions display
            self.action_label.config(text=f"Actions left: {self.player.actions}")
            self.current_turn = "player"
            self.status_label.config(text="Player's turn")

    def enemy_turn(self):
        """Process enemy actions"""
        for enemy in self.enemies:
            # Enemy AI decides what to do
            action, data = enemy.act(self.player.coord_player)
            
            # Update display after each enemy acts
            self.update_game_display()
            
            # Add a delay between enemy actions
            self.root.after(500, None)
        
        # End enemy turn
        
        self.root.after(500, self.end_turn)

    def update_game_display(self):
        """Update the display to show current game state"""
        # Clear the map
        for row_idx, row in enumerate(self.cells):
            for col_idx, cell in enumerate(row):
                background = "lightblue" if (row_idx + col_idx) % 2 == 0 else "lightgreen"
                cell.config(bg=background, text="")
        
        # Show player
        x, y = self.player.coord_player
        self.cells[y][x].config(bg="blue", text="P")
        
        # Show enemies
        for enemy in self.enemies:
            x, y = enemy.coord
            if 0 <= x < 10 and 0 <= y < 20:
                if isinstance(enemy, Goblin):
                    self.cells[y][x].config(bg="green", text="G")
                elif isinstance(enemy, Orc):
                    self.cells[y][x].config(bg="red", text="O")


# --- | brouillon | -----------------------------------------------

# class DnDGame:
#    def __init__(self):
        # self.root = Win(title="Main Menu", width=300, height=200, bg='lightgray')
        # Label(self.root, text="Main menu", font="Arial 20 bold")
        # # print("class mainMenu - test view player : ", self.display_players())
        # Button(self.root, text="Create new Player", command=create_player_window, bg='lightblue')
        # players = self.display_players()
        # for player in players:
        #     Button(self.root, text=f"Name: {player['name']}, Level: {player['level']}, Classe: {player['classe']}, Race: {player['race']}",command=lambda p=player['name']: open_player_window(p))
        # self.root.loop()



# --- | Zone de test | ---

open_game("fg")