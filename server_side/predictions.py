import pickle
import web_scraper.players as ws
import numpy as np


class Predictions:
    def __init__(self):
        self.points_model = pickle.load(
            open('model_creation/pickle_models/points.pkl', 'rb'))
        self.assists_model = pickle.load(
            open('model_creation/pickle_models/assists.pkl', 'rb'))
        self.rebounds_model = pickle.load(
            open('model_creation/pickle_models/rebounds.pkl', 'rb'))

    def predict_next_game(self, player_name, year=2021):
        df = ws.career_stats_table(player_name)
        season_pts = self.predict_points(player_name, df, year)
        season_ast = self.predict_assists(player_name, df, year)
        season_reb = self.predict_rebounds(player_name, df, year)
        df = ws.game_log_table(player_name, year + 2)
        if len(df) < 10:
            return season_pts, season_ast, season_reb
        p = self.perform_regression(df['PTS'].values)
        game_prediction = p(10)
        a = self.perform_regression(df['AST'].values)
        game_prediction_assists = a(10)
        r = self.perform_regression(df['TRB'].values)
        game_prediction_rebounds = r(10)
        return (0.80 * season_pts + 0.2 * game_prediction), (0.8 * season_ast + 0.2 * game_prediction_assists), (0.8 * season_reb + 0.2 * game_prediction_rebounds)

    def perform_regression(self, values):
        X = [i for i in range(10)]
        Y = [int(v) for v in values]
        p = np.poly1d(np.polyfit(X, Y, 3))
        return p

    def predict_points(self, player_name, df, year=2021):
        # Get Season Prediction
        input_data = df.loc[df['Season'] == year].copy().tail(1)
        print(input_data)
        input_data.drop('Season', axis=1, inplace=True)
        season_prediction = self.points_model.predict(input_data)
        return season_prediction

    def predict_assists(self, player_name, df, year=2021):
        input_data = df.loc[df['Season'] == year].copy().tail(1)
        input_data.drop('Season', axis=1, inplace=True)
        prediction = self.assists_model.predict(input_data)
        return prediction

    def predict_rebounds(self, player_name, df, year=2021):
        input_data = df.loc[df['Season'] == year].copy().tail(1)
        input_data.drop('Season', axis=1, inplace=True)
        prediction = self.rebounds_model.predict(input_data)
        return prediction

    def predict_season_stats(self, player_name, year=2021):
        df = ws.career_stats_table(player_name)
        points = self.predict_points(player_name, df, year)
        assists = self.predict_assists(player_name, df, year)
        rebounds = self.predict_rebounds(player_name, df, year)
        return points, assists, rebounds


test = Predictions()
print(test.predict_next_game(input("Enter a player name: ")))
