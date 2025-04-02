from ezTK import *
# from other files :
from player import Player

def open_game(name):
    """
        Open the game for the selected player.
    """
    print(f"Opening game for {name}")
    game = DnDGame(name)
    return game.root.loop()
    # player = Player(name)
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
        self.create_main_menu()
    
    def create_main_menu(self):
        self.root = Win(title="Main Menu", width=300, height=200, bg='lightgray')
        Label(self.root, text="Main menu", font="Arial 20 bold")
        # Button(self.root, text="Create new Player", command=self.create_player_window, bg='lightblue')
        # Button(self.root, text="Play", command=self.open_game)
        pass  # The loop is already handled in open_game


open_game("fg")  # Replace with the actual player name you want to test



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