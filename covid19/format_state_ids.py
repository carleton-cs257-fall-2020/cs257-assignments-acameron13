#Alison Cameron and Adam Nik

import csv

def get_states():
    states = {}
    with open("all-states-history.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            state_abr = row[1]

            if state_abr == 'state':
                continue

            states[state_abr] = states.get(state_abr, 0) + 1
    return states

def assign_state_ids(state_dict):
    state_list = state_dict.keys()
    new_state_dict = {}
    i = 0
    for state in state_list:
        new_state_dict[state] = i
        i += 1

    return new_state_dict

def get_full_state_name(abr):
    state_names = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas',
                'AS': 'American Samoa', 'AZ': 'Arizona', 'CA': 'California',
                'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia',
                'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam',
                'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana',
                'KS': 'Kansas', 'KY': "Kentucky", 'LA': 'Louisiana', 'MA': 'Massachusetts',
                'MD': 'Maryland', 'MI': 'Michigan', 'ME': 'Maine', 'MN': 'Minnesota',
                'MO': 'Missouri', 'MS': 'Mississippi', 'MT': 'Montana',
                'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska',
                'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
                'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma',
                'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico',
                'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota',
                'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia',
                'VI': 'US Virgin Island', 'VT': 'Vermont', 'WA': 'Washington',
                'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming',
                'MP': 'Northern Mariana Islands'}

    state_name = state_names[abr]
    return state_name

def create_state_id_csv(states_ids):
    with open('state_ids.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "abbreviation"])
        for state in states_ids:
            row = [states_ids[state], get_full_state_name(state), state]
            writer.writerow(row)

def edit_all_states_history(state_ids):
    new = open('new-all-states-history.csv', 'w')
    old = open('all-states-history.csv', 'r')
    reader = csv.reader(old)
    writer = csv.writer(new)

    header = ['date', 'state_id', 'deaths', 'new_positive_tests', 'new_negative_tests', 'new_hospitalizations']
    writer.writerow(header)

    for row in reader:
        date, state, death, hosp, neg, pos = row[0], row[1], row[2], row[3], row[4], row[5]

        if state == "state":
            continue

        id = state_ids[state]

        new_row = [date, id, death, pos, neg, hosp]
        writer.writerow(new_row)

    new.close()
    old.close()

def main():
    states_ids = assign_state_ids(get_states())
    create_state_id_csv(states_ids)
    edit_all_states_history(states_ids)

if __name__ == "__main__":
    main()
