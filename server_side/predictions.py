import pickle
from web_scraper.players import get_player_game_log, get_player_career_stats


class Predictions:
    def __init__(self):
        self.points_model = pickle.load(
            open('model_creation/pickle_models/points.pkl', 'rb'))
        self.assists_model = pickle.load(
            open('model_creation/pickle_models/assists.pkl', 'rb'))
        self.rebounds_model = pickle.load(
            open('model_creation/pickle_models/rebounds.pkl', 'rb'))

    def predict_points(self, player_name):
        input_data = get_player_career_stats(player_name).tail(2).head(1)
        prediction = self.points_model.predict(input_data)
        return prediction

    def predict_assists(self, input_data):
        prediction = self.assists_model.predict(input_data)
        return prediction

    def predict_rebounds(self, input_data):
        prediction = self.rebounds_model.predict(input_data)
        return prediction


lebron_stats = [[2, 29, 77, 37.7, 10.0, 17.6, .567, 1.5,
                4.0, .379, 5.7, 7.6, .750, 6.9, 6.3, 1.6, 0.3, 3.5, 1.6, 22.1]]

test = Predictions()
print(test.predict_points("Ja Morant"))
