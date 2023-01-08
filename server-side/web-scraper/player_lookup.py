import pandas as pd
from requests import get
from bs4 import BeautifulSoup


WIDGET_URL = "https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/players/{}.html&div=div_per_game"


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
        r = get(WIDGET_URL.format(option1))
        soup = BeautifulSoup(r.content, 'html.parser')
        h1 = soup.find('h1')
        found_name = h1.find('span').text
        if found_name.lower() == player_name.lower():
            return option1

        # Try Option 2
        r = get(WIDGET_URL.format(option2))
        soup = BeautifulSoup(r.content, 'html.parser')
        h1 = soup.find('h1')
        found_name = h1.find('span').text
        if found_name.lower() == player_name.lower():
            return option2

        # Player not found
        return None
    except Exception as e:
        return None
