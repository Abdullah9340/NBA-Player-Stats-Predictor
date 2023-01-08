import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from player_lookup import get_player_string

player_to_pos = {
    'PG': 1,
    'SG': 2,
    'SF': 3,
    'PF': 4,
    'C': 5
}


def career_stats_table(player_name):
    """
    This function takes in a player name and returns a dataframe of the player's career
    stats. The function returns None if the player name is invalid.
    """
    try:
        player_string = get_player_string(player_name)
        if player_string is None:
            return None

        URL = f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/players/{player_string}.html&div=div_per_game"
        r = get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0].dropna(axis=0)
        df = df[~df['Pos'].str.contains("Did Not Play")]
        df['Pos'] = df['Pos'].apply(lambda x: player_to_pos[x.split('-')[0]])
        df['Season'] = df['Season'].apply(lambda x: int(x.split('-')[0]))
        return df[['Season', 'Pos', 'Age', 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT',
                  'FTA', 'FT%', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']]
    except Exception as e:
        print(e)
        return None


def game_log_table(player_name, year=2022):
    """
    This function takes in a player name and a year and returns a dataframe of the player's
    game log stats for that year. The function returns None if the player name is invalid.
    """
    try:
        player_string = get_player_string(player_name)
        if player_string is None:
            return None

        URL = f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/players/{player_string}/gamelog/{year}/&div=div_pgl_basic"
        r = get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0].drop(
            'Unnamed: 5', axis=1).dropna(axis=0)
        df_last_10 = df.tail(10)
        return df_last_10[["PTS", "TRB", "AST", "STL", "BLK", "TOV", "PF", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "MP", "+/-"]]
    except Exception as e:
        return None
