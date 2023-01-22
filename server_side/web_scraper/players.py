import pandas as pd
from requests import get
from bs4 import BeautifulSoup

player_to_pos = {
    'PG': 1,
    'SG': 2,
    'SF': 3,
    'PF': 4,
    'C': 5
}

LOOK_UP_URL = "https://basketball-reference.com/players/{}.html"


def get_player_string(player_name):
    """
    This function takes in a player name and returns a string that can be used to
    scrape the player's stats from the website.
    """
    try:
        first_name, last_name = player_name.split(" ")
        prefix = last_name[0:5].lower()
        suffix = first_name[0:2].lower()
        option1 = f"{prefix[0]}/{prefix}{suffix}01"
        option2 = f"{prefix[0]}/{prefix}{suffix}02"

        # Try Option 1
        r = get(LOOK_UP_URL.format(option1))
        soup = BeautifulSoup(r.content, 'html.parser')
        h1 = soup.find('h1')
        found_name = h1.find('span').text
        if found_name.lower() == player_name.lower():
            return option1

        # Try Option 2
        r = get(LOOK_UP_URL.format(option2))
        soup = BeautifulSoup(r.content, 'html.parser')
        h1 = soup.find('h1')
        found_name = h1.find('span').text
        if found_name.lower() == player_name.lower():
            return option2

        # Player not found
        return None
    except Exception as e:
        return None


def career_stats_table(player_name):
    """
    This function takes in a player name and returns a dataframe of the player's career
    stats. The function returns None if the player name is invalid.
    """
    try:
        player_string = get_player_string(player_name)
        if player_string is None:
            return None

        URL = f"https://www.basketball-reference.com/players/{player_string}.html"
        r = get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0].dropna(axis=0)
        df = df[~df['Pos'].str.contains("Did Not Play")]
        df['Pos'] = df['Pos'].apply(lambda x: player_to_pos[x.split(',')[0]])
        df['Season'] = df['Season'].apply(lambda x: int(x.split('-')[0]))
        return df[['Season', 'Pos', 'Age', 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT',
                  'FTA', 'FT%', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']]
    except Exception as e:
        print("error", e)
        return None


def game_log_table(player_name, year=2023):
    """
    This function takes in a player name and a year and returns a dataframe of the player's
    game log stats for that year. The function returns None if the player name is invalid.
    """
    try:
        player_string = get_player_string(player_name)
        if player_string is None:
            return None

        URL = f"https://www.basketball-reference.com/players/{player_string}/gamelog/{year}"
        r = get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table', {'id': 'pgl_basic'})
        df = pd.read_html(str(table))[0].drop(
            'Unnamed: 5', axis=1).dropna(axis=0)
        df_last_10 = df.tail(10)
        return df_last_10[["PTS", "TRB", "AST", "STL", "BLK", "TOV", "PF", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "MP", "+/-"]]
    except Exception as e:
        return None
