import csv

def get_athletes():
	athlete = {}
	with open('athlete_events.csv') as f:
		reader = csv.reader(f)
		for row in reader:
			if len(row) < 15:
				continue

			athlete_name = row[1]

			#skip header row
			if athlete_name == "Name":
				continue

			if not (athlete_name in athlete):
				age, year = row[3], row[9]
				if not(age.isnumeric()):
					birth_year = "NA"
				else:
					birth_year = int(year) - int(age)
				athlete[athlete_name] = {'sex': row[2], 'birth_year': birth_year, 'height': row[4], 'weight': row[5]}
	return athlete

def get_games():
	game = {}
	with open('athlete_events.csv') as f:
		reader = csv.reader(f)
		for row in reader:
			if len(row) < 15:
				continue

			year = row[9]

			if year == "Year":
				continue

			if not (year in game):
				game[year] = {'season': row[10], 'city': row[11]}

	return game

def get_events():
	events = {}
	with open('athlete_events.csv') as f:
		reader = csv.reader(f)
		for row in reader:

			if len(row) < 15:
				continue

			event = row[13]

			if event == "Event":
				continue

			if not (event in events):
				events[event] = {'sport': row[12]}

	return events

def get_nocs():
	nocs = {}
	with open('athlete_events.csv') as f:
		reader = csv.reader(f)
		for row in reader:
			if len(row) < 15:
				continue

			noc = row[7]

			if noc == "NOC":
				continue

			if not(noc in nocs):
				nocs[noc] = {'team': row[6]}

	with open('noc_regions.csv') as f2:
		reader2 = csv.reader(f2)
		for row in reader2:
			noc, region = row[0], row[1]

			if noc == "NOC":
				continue

			if (noc in nocs) and (not(region in nocs[noc])):
				nocs[noc]['region'] = region

	return nocs

def assign_ids(data_dict):
	i = 0
	for key in data_dict:
		data_dict[key]['id'] = i
		i += 1
	return data_dict

def write_to_CSV(data_dict, filename):
	with open(filename, 'w', newline='') as f:
		writer = csv.writer(f)
		for key in data_dict:
			row = [data_dict[key]['id'], key]
			for field in data_dict[key]:
				if field != 'id':
					row.append(data_dict[key][field])
			writer.writerow(row)

def match_results_and_write(athletes, games, events, nocs):
	results = []
	medal_ids = {'NA': 0, 'Gold': 1, 'Silver': 2, 'Bronze': 3}
	with open('athlete_events.csv') as f:
		reader = csv.reader(f)
		for row in reader:
			if "Year" in row or len(row) < 15:
				continue

			year, noc, event, medal, athlete = row[9], row[7], row[13], row[14], row[1]

			year_id = games[year]['id']
			noc_id = nocs[noc]['id']
			event_id = events[event]['id']
			medal_id = medal_ids[medal]
			athlete_id = athletes[athlete]['id']

			results.append([year_id, noc_id, event_id, medal_id, athlete_id])

	with open("results.csv", 'w', newline='') as newf:
		writer = csv.writer(newf)
		for row in results:
			writer.writerow(row)


def main():
	athletes = assign_ids(get_athletes())
	games = assign_ids(get_games())
	events = assign_ids(get_events())
	nocs = assign_ids(get_nocs())

	write_to_CSV(athletes,'athletes.csv')
	write_to_CSV(games, 'games.csv')
	write_to_CSV(events, 'events.csv')
	write_to_CSV(nocs, 'nocs.csv')

	match_results_and_write(athletes, games, events, nocs)

main()
