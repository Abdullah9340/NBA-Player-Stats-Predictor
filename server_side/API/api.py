from flask import Flask
from predictions import Predictions
p = Predictions()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return {"message": "Hello, World!"}


@app.route("/predict_season_stats/<player_name>")
def predict_season_stats(player_name):
    p = Predictions()
    player_name = player_name.replace("_", " ")
    points, assists, rebounds = p.predict_season_stats(player_name)
    # return JSON response
    return {
        "points": points[0],
        "assists": assists[0],
        "rebounds": rebounds[0]
    }


@app.route("/predict_next_game/<player_name>")
def predict_next_game(player_name):
    p = Predictions()
    player_name = player_name.replace("_", " ")
    points, assists, rebounds = p.predict_next_game(player_name)
    # return JSON response
    return {
        "points": points[0],
        "assists": assists[0],
        "rebounds": rebounds[0]
    }


if __name__ == "__main__":
    app.run()
