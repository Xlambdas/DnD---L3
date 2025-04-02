
from ezTK import *
# from other files :
from player_creation import create_player_window, open_player_window
from race import get_all_data

# ---------------------------------------------------





















# ---------------------------------------------------

def get_all_players():
    """
        Get all players from the database.
        Returns:
            players: A list of dictionaries representing all players in the database.
    """
    data = get_all_data()
    # print("get_all_players - data : ", data)
    players = data['players']
    # print("get_all_players - players : ", players)
    return players

def home_page():
    """
        Open the home page for the game. to get or create the player instance.
    """
    root = Win(title="Main Menu", width=300, height=200, bg='lightgray')
    Label(root, text="Main menu", font="Arial 20 bold")
    players = get_all_players()
    Button(root, text="Create Player", command=lambda: {create_player_window(), root.quit()})
    for player in players:
        Button(root, text=f"Name: {player['name']}, Level: {player['level']}, Classe: {player['classe']}, Race: {player['race']}", command=lambda:{open_player_window(player['name']), root.quit()})
    root.loop()


if __name__ == "__main__":
    open = home_page()



# --- | brouillon | -----------------------------------------------


# --- | Zone de test | ---
