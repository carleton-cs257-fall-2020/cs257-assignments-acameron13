#Alison Cameron and Adam Nik

import sys
import argparse
import flask
import json
import psycopg2

from config import user
from config import password
from config import database

#app = flask.Flask(__name__)
api = flask.Blueprint('api', __name__)

def get_psql_cursor():
	'''
	Returns cursor to psql database connection
	'''
	try:
		connection = psycopg2.connect(database=database, user=user, password=password)
		cursor = connection.cursor()
	except Exception as e:
		print(e)
		exit()

	return cursor

@api.route('/olympics/search')
def get_search_results():
    athlete = flask.request.args.get('athlete')
    team = flask.request.args.get('team')
    games = flask.request.args.get('games')
    sport = flask.request.args.get('sport')
    event = flask.request.args.get('event')

    try:
        query = '''SELECT results.game_id, results.country_id, results.event_id, results.medal_id, results.athlete_id, games.id, countries.id, events.id, medals.id, athletes.id, games.year, games.season, countries.noc, events.sport, events.event, medals.medal, athletes.name, athletes.sex, athletes.height, athletes.weight, athletes.birth_year
                FROM results, games, countries, events, medals, athletes
                WHERE results.game_id=games.id
                AND results.country_id=countries.id
                AND results.event_id=events.id
                AND results.medal_id=medals.id
                AND results.athlete_id=athletes.id'''

        if athlete is not None:
            query += 'AND athletes.name={}'.format(athlete)
        if team is not None:
            query += 'AND countries.noc={}'.format(team)
        if games is not None:
            #just get the year
            query += 'AND games.year={}'.format(games[0:4])
        if sport is not None:
            query += 'AND events.sport={}'.format(sport)
        if event is not None:
            query += 'AND events.event={}'.format(event)

        cursor = get_psql_cursor()
        cursor.execute(query)

    except Exception as e:
        print(e)
        exit()

    table_data = []
    for row in cursor:
        year, season, noc, sport, event = row[10], row[11], row[12], row[13], row[14]
        medal, athlete, sex, height, weight, birth_year = row[15], row[16], row[17], row[18], row[19], row[20]

        table_entry = {'games': '{} {}'.format(year, season),
                        'team': noc,
                        'sport': sport,
                        'event': event,
                        'medal': medal,
                        'athlete': athlete,
                        'sex': sex,
                        'height': height,
                        'weight': weight,
                        'birth year': birth_year}

        table_data.append(table_entry)

    return json.dumps(table_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
