from ezTK import *
# from other files :
from player import Player

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
        self.interface()

    def interface(self):
        self.root = Win(title="game", width=600, height=400, bg='lightgray', fold=10)
        # creation of the map :
        self.map_frame = Frame(self.root, fold=10, bg='white')
        for row in range(20):
            for col in range(10):
                background = "lightblue" if (row + col) % 2 == 0 else "lightgreen"
                Label(self.map_frame, text="", width=4, height=2, relief="ridge", bg=background)


        # user interface :
        self.action_panel = Frame(self.root, width=150, bg='lightblue')
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