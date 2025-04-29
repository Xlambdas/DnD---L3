from ezTK import *
from enemy import Cutiie, Goblin, Orc, Boss
import random


class GameInterface:
    def __init__(self, game):
        """
            Initialize the game interface.
        """
        self.game = game
        self.root = None
        self.enemies = self.game.enemies
        self.player = self.game.player

        # Colors for each level
        self.palier = self.player.palier
        self.PALIER_COLORS = {
            1: {"bg1": "#b7dfb7", "bg2": "#ccffcc", "border": "#559955"},  # Lush forest
            2: {"bg1": "#d9c7a3", "bg2": "#e5d4b3", "border": "#8a7654"},  # Desert/savanna
            3: {"bg1": "#a3b5d9", "bg2": "#b3c5e5", "border": "#546d8a"},  # Mountains
            4: {"bg1": "#d9a3a3", "bg2": "#e5b3b3", "border": "#8a5454"},  # Volcano/hell
            5: {"bg1": "#1f1f1f", "bg2": "#2a2a2a", "border": "#555555"}   # Final boss lair
        }

        self.MAX_PALIER = 5


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
                colors = self.PALIER_COLORS.get(self.palier, self.PALIER_COLORS[1])
                backg = colors["bg1"] if (row + col) % 2 == 0 else colors["bg2"]
                color_wall = colors["border"] if row==0 or row==19 or col==0 or col==39 else backg
                background = "black" if (row, col) == (10, 0) or (row, col) == (10,39) or (row, col) == (9,0) or (row, col) == (9,39) else color_wall
                # background = "#bbffbb" if (row + col) % 2 == 0 else "#ccffcc"

                cell = Brick(self.map_frame, width=16, height=16, bg=background, grow=False, state=(row, col))
                cell.bind("<Button-1>", lambda event, r=row, c=col: self.game.on_cell_click((r, c)))  # Bind click event
                col_cells.append(cell)
            self.cells.append(col_cells)
        # --- | event log panel | ---
        side_frame = Frame(self.root, width=500, bg='gray', grow=False, fold=2)
        status_frame = Frame(side_frame, width=500, bg='gray', grow=False, fold=1)
        Label(status_frame, text="Status", bg='gray', font="Arial 14 bold")
        self.palier_label = Label(status_frame, text=f"Palier: {self.palier}/{self.MAX_PALIER}", font="Arial 12", bg='lightblue')
        self.status_case = Label(status_frame, text="On case : " + str(self.player.coord), bg='lightblue', font="Arial 12")
        self.status_name = Label(status_frame, text="Name: " + str(self.player.name), bg='lightblue', font="Arial 12")
        self.status_race = Label(status_frame, text="Race: " + str(self.player.race_name), bg='lightblue', font="Arial 12")
        self.status_classe = Label(status_frame, text="Classe: " + str(self.player.classe_name), bg='lightblue', font="Arial 12")
        self.status_health = Label(status_frame, text="Health: " + str(self.player.health), bg='lightblue', font="Arial 12")
        self.status_xp = Label(status_frame, text="XP: " + str(self.player.xp), bg='lightblue', font="Arial 12")
        event_log = Frame(side_frame, width=500, bg='lightblue', grow=False, fold=1)
        title = Frame(event_log, width=500, height=200, bg='lightblue', grow=False)
        Label(title, text="All the action of the game :", bg='gray', font="Arial 14 bold")
        frame_log = Frame(event_log, width=500, height=400, bg='lightblue' )
        self.show_event = Label(frame_log, text="curent action", bg='lightblue', font="Arial 12")


        # --- | User interface | ---
        self.action_panel = Frame(self.root, bg='lightblue', fold=1)
        self.action_label = Label(self.action_panel, text=f"Actions left: {self.player.actions}", font="Arial 14 bold", bg='lightblue')
        # Label(self.action_panel, text=f"Player: {self.player.name}", bg='lightblue', height=2, font="Arial 14 bold")

        # Game status
        self.status_label = Label(self.action_panel, text=f"Turn: {self.game.current_turn.capitalize()}", font="Arial 12", bg='lightblue')

        # Buttons
        Button(self.action_panel, text="Move", command=lambda: self.game.player_act('mouv'), bg='lightgray')
        Button(self.action_panel, text="Attack", command=lambda: self.game.player_act('attack'), bg='lightgray')
        # Button(self.action_panel, text="Save Game", command=self.save_game, bg='lightgray')

        self.player.coord = (9,39)

        for enemy in self.enemies:
            enemy.coord = (random.randrange(1,19),random.randrange(1,29))
        # Update the display
        self.update_game_display()
        win.loop()

    def update_game_display(self):
        """Update the display to show current game state"""
        # Clear the map
        if self.player.health <= 0:
            self.show_game_over()
            return

        if self.palier == self.MAX_PALIER:
            if self.game.is_final_boss:
                print("ui - update game : Final boss")
                self.update_boss_display()
            else:
                self.game.boss_palier()
            return
        if self.player.coord == (9, 0) or self.player.coord == (10, 0):
            self.palier += 1
            if self.palier > self.MAX_PALIER:
                return
            self.game.new_palier(self.palier)

        for col_idx, row in enumerate(self.cells):
            for row_idx, cell in enumerate(row):
                colors = self.PALIER_COLORS.get(self.palier, self.PALIER_COLORS[1])
                backg = colors["bg1"] if (row_idx + col_idx) % 2 == 0 else colors["bg2"]
                color_wall = colors["border"] if row_idx==0 or row_idx==19 or col_idx==0 or col_idx==39 else backg
                background = "black" if (row_idx, col_idx) == (10, 0) or (row_idx, col_idx) == (10,39) or (row_idx, col_idx) == (9, 0) or (row_idx, col_idx) == (9,39) else color_wall
                cell.config(bg=background, text="", border=1)

        # Show player
        x, y = self.player.coord
        self.cells[y][x].config(bg="blue", text="P", fg="white", font="Arial 12 bold", border=1)

        # Show enemies
        for enemy in self.game.enemies:
            x, y = enemy.coord
            if 1 <= x < 19 and 1 <= y < 39:
                if isinstance(enemy, Goblin):
                    self.cells[y][x].config(bg="darkgreen", border=1)
                elif isinstance(enemy, Orc):
                    self.cells[y][x].config(bg="red", border=1)
                elif isinstance(enemy, Cutiie):
                    self.cells[y][x].config(bg="darkgreen", border=1)

        if self.player.actions <= 0:
            self.status_label.config(text="No actions left!")
            self.game.end_turn()
            return

    def grid_dist(self, start_coord, move_distance):
        """
        Modify the grid colors to highlight all available cells within a movement distance.
        Args:
            start_coord (tuple): Starting coordinate (x, y).
            move_distance (int): Maximum movement distance.
        """
        if self.game.game_over:
            return

        possible_moves = self.game.possible_coords(start_coord, move_distance)
        for y in range(20):
            for x in range(40):
                colors = self.PALIER_COLORS.get(self.palier, self.PALIER_COLORS[1])
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
                        backg = colors["bg1"] if (x + y) % 2 == 0 else colors["bg2"]
                        color_wall = colors["border"] if x==0 or y==19 or y==0 or x==39 else backg
                        background = "black" if (y, x) == (10, 0) or (y, x) == (10,39) or (y, x) == (9,0) or (y, x) == (9,39) else color_wall
                        self.cells[x][y].config(bg=background)

        self.root.wait_variable(StringVar())
        self.action_panel.config(text=f"Actions left: {self.player.actions}")
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
        Button(game_over_frame, text="Play Again", font="Arial 16 bold", bg="red", fg="green") #, command=self.restart_game)

        # Button to quit
        Button(game_over_frame, text="Quit", font="Arial 16 bold", bg="gray", fg="red", command=lambda: self.win.exit())#win.destroy())

    def show_end_game(self):
        """Display the end game screen when the player wins."""
        # Clear the main window
        for widget in self.win.winfo_children():
            widget.destroy()

        # Create end game screen
        end_game_frame = Frame(self.win, width=800, height=600, bg='black', fold=3)

        # Victory message
        Label(end_game_frame, text="CONGRATULATIONS!", font="Arial 36 bold", fg="gold", bg="black")
        Label(end_game_frame, text=f"{self.player.name} has defeated the final boss!", font="Arial 18", fg="white", bg="black")

        # Show stats
        stats_frame = Frame(end_game_frame, bg='black', fold=1)
        Label(stats_frame, text=f"XP earned: {self.player.xp}", font="Arial 14", fg="white", bg="black")
        Label(stats_frame, text=f"Class: {self.player.classe_name}", font="Arial 14", fg="white", bg="black")
        Label(stats_frame, text=f"Race: {self.player.race_name}", font="Arial 14", fg="white", bg="black")

        # Button to restart
        Button(end_game_frame, text="Play Again", font="Arial 16 bold", bg="green", fg="white", command=self.restart_game)

        # Button to quit
        Button(end_game_frame, text="Quit", font="Arial 16 bold", bg="gray", fg="red", command=lambda: self.win.exit())

    def on_inout(self, widget, code, mods):
        """Handle mouse in/out events."""
        if self.game.game_over:
            return None

        if not hasattr(self, 'status_case') or not self.status_case.winfo_exists():
            return None

        if widget.master == self.map_frame and widget.index is not None:
            row, col = widget.index
            for enemy in self.game.enemies:
                if enemy.coord == (col, row):
                    self.status_case['text'] = f"On case : {enemy.coord}"
                    self.status_name['text'] = f"Name: {enemy.name}"
                    self.status_race['text'] = f"Range Attack: {enemy.range_attack()}"
                    self.status_classe['text'] = f"level: {1}"
                    self.status_health['text'] = f"Health: {enemy.health}"
                    self.status_xp['text'] = f"XP: {None}"
                    return enemy.coord
                else:
                    self.status_case['text'] = f"On case : {self.player.coord}"
                    self.status_name['text'] = f"Name: {self.player.name}"
                    self.status_race['text'] = f"Race: {self.player.race_name}"
                    self.status_classe['text'] = f"Classe: {self.player.classe_name}"
                    self.status_health['text'] = f"Health: {self.player.health}"
                    self.status_xp['text'] = f"XP: {self.player.xp}"
            return None
        else:
            self.status_case['text'] = f"On case : {self.player.coord}"
            self.status_name['text'] = f"Name: {self.player.name}"
            self.status_race['text'] = f"Race: {self.player.race_name}"
            self.status_classe['text'] = f"Classe: {self.player.classe_name}"
            self.status_health['text'] = f"Health: {self.player.health}"
            self.status_xp['text'] = f"XP: {self.player.xp}"
            return None

    def log_action(self, message):
        """Log actions to the event log."""
        if not hasattr(self, 'action_history'):
            self.action_history = []

        # Append the action to history and keep only the last 5
        self.action_history.append(message)
        self.action_history = self.action_history[-9:]

        # Display the last 5 actions
        self.show_event['text'] = "\n".join(self.action_history)


    def update_boss_display(self):
        """Update the display to show current game state"""

        if all(enemy.health <= 0 for enemy in self.enemies if isinstance(enemy, Boss)):
            self.show_end_game()
            return

        for col_idx, row in enumerate(self.cells):
            for row_idx, cell in enumerate(row):
                colors = self.PALIER_COLORS.get(self.palier, self.PALIER_COLORS[1])
                backg = colors["bg1"] if (row_idx + col_idx) % 2 == 0 else colors["bg2"]
                color_wall = colors["border"] if row_idx==0 or row_idx==19 or col_idx==0 or col_idx==39 else backg
                background = "black" if (row_idx, col_idx) == (10, 0) or (row_idx, col_idx) == (10,39) or (row_idx, col_idx) == (9, 0) or (row_idx, col_idx) == (9,39) else color_wall
                cell.config(bg=background, text="", border=1)

        # Show player
        x, y = self.player.coord
        self.cells[y][x].config(bg="blue", text="P", fg="white", font="Arial 12 bold", border=1)

        for enemy in self.game.enemies:
            x, y = enemy.coord
            if 1 <= x < 19 and 1 <= y < 39:
                if isinstance(enemy, Boss):
                    self.cells[y][x].config(bg="#FF4500")


        if self.player.actions <= 0:
            self.status_label.config(text="No actions left!")
            self.game.end_turn()
            return

