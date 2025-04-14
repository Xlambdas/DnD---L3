from ezTK import *
# from other files :
from player import Player
from enemy import Goblin, Orc
import random

def open_game(name):
    """
        Open the game for the selected player.
    """
    print(f"Opening game for {name}")
    game = DnDGame(name)
    # return game.root.loop()
    # player_name = player.name
    # print(f"Player name: {player_name}")
    # print(f"Player info: {player.descr()}")
    # window = Win(title="Game", width=300, height=200)
    # Label(window, text=f"Welcome to the game, {player.name}!")
    # Button(window, text="Close", command=window.quit)
    # window.loop()


class DnDGame:
    def __init__(self, name):
        self.root = None
        self.player = Player(name)
        # Create some enemies
        self.enemies = [
            Goblin(),
            Orc()
        ]
        self.current_turn = "player"  # Start with player's turn
        self.interface()
    
    def all_enemies_dead(self):
        """Check if all enemies are dead"""
        return all(enemy.health <= 0 for enemy in self.enemies)

    def all_players_dead(self):
        """Check if all players are dead"""
        # If you have multiple players, adjust accordingly
        return self.player.health <= 0

    def game_over_screen(self, player_won):
        """Display game over screen with restart/exit options"""
        # Clear current window contents
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Create game over message
        message = "Victory! All enemies defeated." if player_won else "Game Over! Your character has fallen."
        tk.Label(self.window, text=message, font=("Arial", 18)).pack(pady=20)
        
        # Create buttons
        restart_button = tk.Button(self.window, text="Play Again", command=self.restart_game)
        restart_button.pack(pady=10)
        
        exit_button = tk.Button(self.window, text="Exit Game", command=self.window.destroy)
        exit_button.pack(pady=10)
    
    def restart_game(self):
        """Restart the game by recreating everything"""
        # Clear current window contents
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Reset game state
        self.__init__(self.name)  # Reinitialize with the same name

    def interface(self):
        self.root = Win(title="game", width=600, height=400, bg='lightgray', fold=10)
        
        # Create map
        self.map_frame = Frame(self.root, fold=10, bg='white')
        self.cells = []
        for row in range(20):
            for col in range(10):
                background = "lightblue" if (row + col) % 2 == 0 else "lightgreen"
                cell = Label(self.map_frame, text="", width=4, height=2, relief="ridge", bg=background)
                self.cells.append(cell)

        # User interface
        self.action_panel = Frame(self.root, width=150, bg='lightblue')
        self.action_label = Label(self.action_panel, text=f"Actions left: {self.player.actions}", font="Arial 14 bold", bg='lightblue')
        Label(self.action_panel, text=f"Player: {self.player.name}", bg='lightblue')
        
        # Game status
        self.status_label = Label(self.action_panel, text=f"Turn: {self.current_turn.capitalize()}", font="Arial 12", bg='lightblue')
        
        # Buttons
        Button(self.action_panel, text="Move", command=lambda: self.player_action('mouv'), bg='lightgray')
        Button(self.action_panel, text="Attack", command=lambda: self.player_action('attack'), bg='lightgray')
        Button(self.action_panel, text="End Turn", command=self.end_turn, bg='lightgray')
        # Button(self.action_panel, text="Inventory")#, command=self.inventory_action, bg='lightgray')
        # Button(self.action_panel, text="End Turn")#, command=self.end_turn_action, bg='lightgray')
        
        # Randomize player position
        self.player.coord_player = (random.randrange(0,10), random.randrange(0,3))
        
        # Place enemies away from player
        for enemy in self.enemies:
            # Make sure enemies start at least 3 squares away from player
            while self.distance(enemy.coord, self.player.coord_player) < 3:
                enemy.coord = (random.randrange(0,10), random.randrange(10,20))
        
        # Update the display
        self.update_game_display()
        self.root.loop()

    def distance(self, coord1, coord2):
        """Calculate Manhattan distance between two coordinates"""
        x1, y1 = coord1
        x2, y2 = coord2
        # return abs(x2 - x1) + abs(y2 - y1)
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def player_action(self, action_type):
        """Handle player action"""
        if self.current_turn != "player":
            self.status_label.config(text="Not your turn!")
            return
            
        result = self.player.action(action_type)
        
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
        for i, cell in enumerate(self.cells):
            row = i // 10
            col = i % 10
            background = "lightblue" if (row + col) % 2 == 0 else "lightgreen"
            cell.config(bg=background, text="")
        
        # Show player
        x, y = self.player.coord_player
        cell_index = (y * 10) + x
        if 0 <= cell_index < len(self.cells):
            self.cells[cell_index].config(bg="blue", text="P")
        
        # Show enemies
        for enemy in self.enemies:
            x, y = enemy.coord
            cell_index = (y * 10) + x
            if 0 <= cell_index < len(self.cells):
                if isinstance(enemy, Goblin):
                    self.cells[cell_index].config(bg="green", text="G")
                elif isinstance(enemy, Orc):
                    self.cells[cell_index].config(bg="red", text="O")
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