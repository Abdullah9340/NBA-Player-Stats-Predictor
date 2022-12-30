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


def convert_player_to_url(player_name, type="career", year=2022):
    """
      This function converts a player name to a url that can be used to scrape the player
      stats from the website. The url is a widget from sports-reference.com that contains
      the html of the player's stats page. The function takes in a player name, a type
      (career, game_log or headshot), and a year (if type is game_log). The function returns the
      url as a string.
    """
    try:
        first_name, last_name = player_name.split(" ")
        prefix = last_name[0:5].lower()
        suffix = first_name[0:2].lower()
        if (type == "career"):
            return f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/players/{prefix[0]}/{prefix}{suffix}01.html&div=div_per_game"
        elif (type == "game_log"):
            return f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/players/{prefix[0]}/{prefix}{suffix}01/gamelog/{year}/&div=div_pgl_basic"
    except Exception as e:
        return None


def get_player_career_stats(player_name):
    """
    This function takes in a player name and returns a dataframe of the player's career
    stats. The function returns None if the player name is invalid.
    """
    url = convert_player_to_url(player_name)
    try:
        r = get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0].dropna(axis=0)
        df = df[~df['Pos'].str.contains("Did Not Play")]
        df['Pos'] = df['Pos'].apply(lambda x: player_to_pos[x.split('-')[0]])
        return df[['Pos', 'Age', 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT',
                  'FTA', 'FT%', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']]
    except Exception as e:
        print(e)
        return None


def get_player_game_log(player_name, year):
    """
    This function takes in a player name and a year and returns a dataframe of the player's
    game log stats for that year. The function returns None if the player name is invalid.
    """
    url = convert_player_to_url(player_name, "game_log", year)
    try:
        r = get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0].dropna(axis=0)
        df_last_10 = df.tail(10)
        return df_last_10[["PTS", "TRB", "AST", "STL", "BLK", "TOV", "PF", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "MP", "+/-"]]
    except Exception as e:
        return None
