import pandas as pd
from requests import get
from bs4 import BeautifulSoup

#change the function name to something more appropriate, or perhaps split into 2 functions
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
            url_option1 = f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/players/{prefix[0]}/{prefix}{suffix}01.html&div=div_per_game"
            url_option2 = f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/players/{prefix[0]}/{prefix}{suffix}02.html&div=div_per_game"
            r = get(url_option1)
            soup = BeautifulSoup(r.content, 'html.parser')
            h1 = soup.find('h1')
            found_name = h1.find('span').text
            table = None
            if found_name == player_name:
                table = soup.find('table')
            else:
                r = get(url_option2)
                soup = BeautifulSoup(r.content, 'html.parser')
                table = soup.find('table')
            return table
        
        elif (type == "game_log"):
            url_option1 = f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/players/{prefix[0]}/{prefix}{suffix}01/gamelog/{year}/&div=div_pgl_basic"
            url_option2 = f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/players/{prefix[0]}/{prefix}{suffix}01/gamelog/{year}/&div=div_pgl_basic"
            r = get(url_option1)
            soup = BeautifulSoup(r.content, 'html.parser')
            h1 = soup.find('h1')
            found_name = h1.find('span').text
            table = None
            if found_name == player_name:
                table = soup.find('table')
            else:
                r = get(url_option2)
                soup = BeautifulSoup(r.content, 'html.parser')
                table = soup.find('table')
            return table

    except Exception as e:
        return None


#need to make adjustments to function calls
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
        df.rename(columns={'Season': 'SEASON', 'Age': 'AGE',
                           'Tm': 'TEAM', 'Lg': 'LEAGUE', 'Pos': 'POS'}, inplace=True)
        return df
    except Exception as e:
        return None

#need to make adjustments to function calls
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

