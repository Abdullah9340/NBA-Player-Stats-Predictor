import json
import functions_framework
from players import game_log_table, career_stats_table
import predictions as p
from dotenv import load_dotenv
import datetime

load_dotenv()

import os
import psycopg2



@functions_framework.http
def main(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """

    def get_set_from_database(table_name, player_name, expiry_duration, update_function):
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE player_name = '{player_name}'")
        
        if cur.rowcount == 0:
            data = update_function(player_name)
            cur.execute(f"""INSERT INTO {table_name} (player_name, jsondata) VALUES ('{player_name}', '{data}')""")
            conn.commit()
            cur.close()
            conn.close()
            return data
        fetched_data = cur.fetchone()
        updateDate = fetched_data[3]
        currTime = datetime.datetime.now()
        if (currTime - updateDate).days > expiry_duration:
            data = update_function(player_name)
            # Update player data and update timestamp
            cur.execute(f"UPDATE {table_name} SET jsondata = '{data}', updated_at = '{currTime}' WHERE player_name = '{player_name}'")
            conn.commit()
            cur.close()
            conn.close()
            return data
        return fetched_data[2]
        

    request_json = request.get_json(silent=True)
    if request_json and 'action' in request_json and 'name' in request_json:
        action = request_json['action']
        name = request_json['name']
        if action == 'game_logs':
            # return {'data': game_logs(name)}
            return {'data': get_set_from_database('game_stats', name, 2, game_logs)}
        if action == 'career_stats':
            return {'data': get_set_from_database('career_stats', name, 30, career_stats)}
        if action == "predict":
            predict_class = p.Predictions()
            k = get_set_from_database('predicted_stats', name, 2, predict_class.predict)
            return {'data': k}
        return {'error': 'Invalid Action'}

    else:
        return {'error': 'Invalid Input'}


def career_stats(player_name):
    """Background Cloud Function
    Args:
         player_name (dict): The dictionary with data specific to this type of
         event. The `data` field contains the Pub/Sub message. The `attributes`
         field will contain custom attributes if there are any.
    Returns:
         None; the output is written to Stackdriver Logging
    """

    res = career_stats_table(player_name)
    test = res.to_json(orient='records')
    return test


def game_logs(player_name):
    """Background Cloud Function
    Args:
         player_name (dict): The dictionary with data specific to this type of
         event. The `data` field contains the Pub/Sub message. The `attributes`
         field will contain custom attributes if there are any.
    Returns:
         None; the output is written to Stackdriver Logging
    """

    res = game_log_table(player_name)
    test = res.to_json(orient='records')
    return test
