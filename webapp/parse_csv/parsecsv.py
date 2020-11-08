import csv

def get_athletes():

	athlete = {}
	with open('athlete_events.csv') as f:
		reader = csv.reader(f)
		for row in reader:
			athlete_name = row[1]
			
			if not (athlete_name in athlete):
				birth_year = row[9] - row[3]
				athlete[athlete_name] = {'sex': row[2], 'birth_year': birth_year, 'height': row[4], 'weight': row[5]}
	return athlete
	
def get_games():
	game = {}
	with open('athlete_events.csv') as f:
		reader = csv.reader(f)
		for row in reader:
			year = row[9]
			
			if not (year in game):
				game[year] = {'season': row[10], 'city': row[11]}
				
	return game
	
def get_events():
	events = {}
	with open('athlete_events.csv') as f:
		reader = csv.reader(f)
		for row in reader:
			event = row[13]
			
			if not (event in events):
				events[event] = row[12]
				
	return events
	

				