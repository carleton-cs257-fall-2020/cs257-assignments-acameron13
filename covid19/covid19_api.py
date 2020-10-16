#!/usr/bin/env python3
'''
    Alison Cameron and Adam Nik
'''
import sys
import argparse
import flask
import json
import psycopg2

from config import user
from config import password
from config import database

app = flask.Flask(__name__)

def get_psql_cursor():
	try:
		connection = psycopg2.connect(database=database, user=user, password=password)
		cursor = connection.cursor()
	except Exception as e:
		print(e)
		exit()

	return cursor

def get_daily_data(state_abbreviation):
	try:
		query = '''SELECT covid19_days.date, covid19_days.state_id, states.id, states.abbreviation, covid19_days.deaths, covid19_days.new_positive_tests, covid19_days.new_negative_tests, covid19_days.new_hospitalizations
					FROM covid19_days, states
					WHERE covid19_days.state_id=states.id
					AND states.abbreviation = %s'''
		cursor = get_psql_cursor()
		cursor.execute(query, (state_abbreviation.upper(),))
	except Exception as e:
		print(e)
		exit()

	daily_state_data = []
	for row in cursor:
		date, deaths, positive, negative, hospitalizations = row[0], row[4], row[5], row[6], row[7]
		abrv_upper = state_abbreviation.upper()
		state = {'date': str(date),
				'state': abrv_upper,
				'deaths': int(deaths),
				'positive': int(positive),
				'negative': int(negative),
				'hospitalizations': int(hospitalizations)}

		daily_state_data.append(state)

	return daily_state_data

def get_cumulative_data(state_abbreviation):
	daily_state_data = get_daily_data(state_abbreviation)

	start_date = daily_state_data[0]['date']
	end_date = daily_state_data[0]['date']

	total_deaths = 0
	total_positives = 0
	total_negatives = 0
	total_hospitalizations = 0

	for data_on_date in daily_state_data:
		total_deaths += data_on_date['deaths']
		total_positives += data_on_date['positive']
		total_negatives += data_on_date['negative']
		total_hospitalizations += data_on_date['hospitalizations']

		cur_date = data_on_date['date']
		if cur_date > start_date:
			start_date = cur_date
		if cur_date < end_date:
			end_date = cur_date

	cumulative_data = {'start_date': start_date,
						'end_date': end_date,
						'state': state_abbreviation.upper(),
						'deaths': total_deaths,
						'positive': total_positives,
						'negative': total_negatives,
						'hospitalizations': total_hospitalizations}

	return cumulative_data

def get_all_cumulative_data():
	try:
		query = '''SELECT abbreviation FROM states'''
		cursor = get_psql_cursor()
		cursor.execute(query)
	except Exception as e:
		print(e)
		exit()

	all_cumulative_data = []
	for row in cursor:
		abbreviation = row[0]
		all_cumulative_data.append(get_cumulative_data(abbreviation))

	return all_cumulative_data

@app.route('/states/cumulative')
def route_all_cumulative_data():
    all_cumulative_data = get_all_cumulative_data()
    sort = flask.request.args.get('sort')
    if sort is None:
        sort = 'deaths'
    if sort == 'cases':
        sort = 'positive'
    sorted_cumulative_data = sorted(all_cumulative_data, key=lambda x: x[sort], reverse=True)

    return json.dumps(sorted_cumulative_data)

@app.route('/state/<state_abbreviation>/cumulative')
def route_cumulative_data(state_abbreviation):
	cumulative_data = get_cumulative_data(state_abbreviation)
	return json.dumps(cumulative_data)

@app.route('/state/<state_abbreviation>/daily')
def route_daily_data(state_abbreviation):
	daily_state_data = get_daily_data(state_abbreviation)
	return json.dumps(daily_state_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
