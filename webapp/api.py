'''
Alison Cameron and Adam Nik
CS257 Software Design
Carleton College
'''

import sys
import argparse
import flask
import json
import psycopg2

from config import user
from config import password
from config import database

api = flask.Blueprint('api', __name__)

def get_psql_cursor():
	try:
		connection = psycopg2.connect(database=database, user=user, password=password)
		cursor = connection.cursor()
	except Exception as e:
		print(e)
		exit()

	return cursor

@api.route('/olympics/search')
def get_search_results():
    '''
    Retrieves the data needed to fill in the table on search.html
    '''
    athlete = flask.request.args.get('athlete')
    team = flask.request.args.get('team')
    games = flask.request.args.get('games')
    sport = flask.request.args.get('sport')
    event = flask.request.args.get('event')
    first_entry = flask.request.args.get('first_entry')
    last_entry = flask.request.args.get('last_entry')
    prev_last_entry = flask.request.args.get('prev_last_entry')

    try:
        query = '''SELECT results.game_id, results.country_id, results.event_id, results.medal_id, results.athlete_id, games.id, countries.id, events.id, medals.id, athletes.id, games.year, games.season, countries.noc, events.sport, events.event, medals.medal, athletes.name, athletes.sex, athletes.height, athletes.weight, athletes.birth_year, results.id
				FROM results, games, countries, events, medals, athletes
				WHERE results.game_id=games.id
                AND results.country_id=countries.id
                AND results.event_id=events.id
                AND results.medal_id=medals.id
                AND results.athlete_id=athletes.id'''

        opt_params = [athlete, team, games, sport, event]
        param_names = []
        for i in range(len(opt_params)):
            param = opt_params[i]
            if param is not None:
                param_names.append(param)
                if i == 0:
                    query += ' AND athletes.name=%s'
                elif i == 1:
                    query += ' AND countries.noc=%s'
                elif i == 2:
                    query += ' AND games.year=%s'
                elif i == 3:
                    query += ' AND events.sport=%s'
                elif i == 4:
                    query += ' AND events.event=%s'

        if last_entry is not None:
        	query += ' AND results.id<={}'.format(last_entry);
        if first_entry is not None:
            query += ' AND results.id>={}'.format(first_entry);
        if prev_last_entry is not None:
            query += ' AND results.id>{}'.format(prev_last_entry);

        query += ' LIMIT 20'

        cursor = get_psql_cursor()
        cursor.execute(query, tuple(param_names))

    except Exception as e:
        print(e)
        exit()

    table_data = [None, None]
    first = True
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

        #Retrieve the id of the first and last entry for this page of data
        if first:
            table_data[1] = row[21]
            first = False

        table_data[0] = row[21]

    return json.dumps(table_data)

@api.route('olympics/dropdowns')
def get_fields():
    '''
    Retrieves data to fill in the options for each dropdown menu on search.html
    '''
    field = flask.request.args.get('field')
    try:
        if field == 'games':
            query = '''SELECT games.year, games.season FROM games'''
        elif field == 'teams':
            query = '''SELECT countries.noc FROM countries'''
        elif field == 'sports':
        	query = '''SELECT events.sport FROM events'''
        elif field == 'events':
        	query = '''SELECT events.event FROM events'''
        elif field == 'athletes':
        	query = '''SELECT athletes.name FROM athletes'''

        cursor = get_psql_cursor()
        cursor.execute(query)

    except Exception as e:
        print(e)
        exit()

    dropdown_options = []
    for row in cursor:
        if field == 'games':
            dropdown_options.append({'year': row[0], 'season': row[1]})
        elif field == 'sports':
            if row not in dropdown_options:
                dropdown_options.append(row)
        else:
            dropdown_options.append(row)

    if field == 'games':
        dropdown_options = sorted(dropdown_options, key=lambda x: x['year'], reverse=True)
    else:
        dropdown_options = sorted(dropdown_options)
    return json.dumps(dropdown_options)

@api.route('olympics/countries')
def get_country_data():
    '''
    Retrieves data to be used for the map in index.html. The data for each
    country includes the total number of medals they have won, as well as if
    they have hosted Olympic games and where.
    '''
    medal_count_by_region = get_medal_counts_by_region()
    medal_count_by_noc = convert_region_to_noc(medal_count_by_region)
    games_by_country = get_games_list()

    medal_nocs = set(medal_count_by_noc.keys())
    games_nocs = set(games_by_country.keys())
    all_nocs = medal_nocs.union(games_nocs)

    country_info = {}
    for noc in all_nocs:
        if noc in medal_count_by_noc:
            medal_count = medal_count_by_noc[noc]
        else:
            medal_count = 0

        country_info[noc] = {'medal_count':medal_count}

        if noc in games_by_country:
            country_info[noc]['games_list'] = games_by_country[noc]


    return json.dumps(country_info)

def get_medal_counts_by_region():
    try:
        query = '''SELECT results.medal_id, countries.id, games.id, countries.region, games.year, games.city, games.season
                    FROM results, countries, games
                    WHERE results.country_id = countries.id
                    AND results.medal_id > 0
                    AND results.game_id = games.id
                    '''
        cursor = get_psql_cursor()
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    medal_count_by_region = {}
    for row in cursor:
         region = row[3]
         if region in medal_count_by_region:
             medal_count_by_region[region] += 1
         else:
             medal_count_by_region[region] = 1
    return medal_count_by_region

def convert_region_to_noc(medal_count_by_region):
    try:
        query = '''SELECT results.game_id, games.year, countries.id, countries.region, countries.noc
                    FROM results, games, countries
                    WHERE results.game_id = games.id
                    AND games.year = 2016
                    AND results.country_id = countries.id
                    '''
        cursor = get_psql_cursor()
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    medal_count_by_noc = {}
    for row in cursor:
        region, noc = row[3], row[4]
        if not(noc in medal_count_by_noc) and (region in medal_count_by_region):
            medal_count_by_noc[noc] = medal_count_by_region[region]
    return medal_count_by_noc

def get_games_list():
    try:
        query = '''SELECT games.year, games.season, games.city, games.country_id, countries.id, countries.noc
                    FROM games, countries
                    WHERE games.country_id = countries.id'''
        cursor = get_psql_cursor()
        cursor.execute(query)

    except Exception as e:
        print(e)
        exit()

    games_by_country = {}
    for row in cursor:
        year, season, city, noc = row[0], row[1], row[2], row[5]
        game_dict = {'year': year, 'season': season, 'city':city}
        if not(noc in games_by_country):
            games_by_country[noc] = [game_dict]
        else:
            games_by_country[noc].append(game_dict)
            games_by_country[noc] = sorted(games_by_country[noc], key=lambda x: x['year'], reverse=True)

    return games_by_country


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
