// Alison Cameron and Adam Nik

var direction = ''
var lastEntry = -1;
var firstEntry = 20;
var prevFirstEntry = -1;
window.onload = initialize;

function initialize() {

	propogateGamesDropdown();
	propogateDropdown('teams');
	propogateDropdown('sports');
	propogateDropdown('events');
	propogateDropdown('athletes');
	console.log(lastEntry)
	var submit = document.getElementById('search_submit');
	submit.onclick = tableOnClicked;
	console.log(lastEntry)
	var back = document.getElementById('back');
	var forward = document.getElementById('forward');
	forward.onclick = go_forward;
	back.onclick = go_backward;

}


function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function tableOnClicked() {
	var url = getAPIBaseURL() + '/olympics/search';
    var addition = get_dropdown_values();
    var return_entry;
    url += addition;
    if (direction == 'forward'){
        url += 'last_entry=' + lastEntry;
    }
    else if (direction == 'backward'){
        url += 'first_entry=' + firstEntry; + '&prev_first_entry=' + prevFirstEntry;
    }
    // console.log(direction);
    console.log(url);

//     Send the request to the Books API /authors/ endpoint
    fetch(url, {method: 'get'})

//     When the results come back, transform them from a JSON string into
//     a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

//     Once you have your list of author dictionaries, use it to build
//     an HTML table displaying the author names and lifespan.
    .then(function(results) {
        // Build the table body.
        prevFirstEntry = firstEntry;
        lastEntry = results[0];
        firstEntry = results[1];
        console.log(firstEntry);
        console.log(lastEntry);
        console.log(prevFirstEntry);
        var tableBody = '<tr><th>Games</th><th>Team</th><th>Sport</th><th>Event</th><th>Medal</th><th>Athlete</th><th>Sex</th><th>Height</th><th>Weight</th><th>Birth Year</th></tr>';
        for (var k = 2; k < results.length; k++) {
            tableBody += '<tr>';

            tableBody += '<td>' + results[k]['games'] + '</td>'
                        + '<td>' + results[k]['team'] + '</td>'
                        + '<td>' + results[k]['sport'] + '</td>'
                        + '<td>' + results[k]['event'] + '</td>'
                        + '<td>' + results[k]['medal'] + '</td>'
                        + '<td>' + results[k]['athlete'] + '</td>'
                        + '<td>' + results[k]['sex'] + '</td>'
                        + '<td>' + results[k]['height'] + '</td>'
                        + '<td>' + results[k]['weight'] + '</td>'
                        + '<td>' + results[k]['birth year'] + '</td>'
                        + '</tr>';
        }

        // Put the table body we just built inside the table that's already on the page.
		var resultsTableElement = document.getElementById('results');
		if (resultsTableElement) {
			resultsTableElement.innerHTML = tableBody;
		}

    })


    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });

}

function propogateGamesDropdown(){
    var url = getAPIBaseURL() + '/olympics/dropdowns/games';
    fetch(url, {method: 'get'})

//     When the results come back, transform them from a JSON string into
//     a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

//     Once you have your list of author dictionaries, use it to build
//     an HTML table displaying the author names and lifespan.
    .then(function(results){
        var dropdown_options = '';
        for (var k = 0; k < results.length; k++){
                games = results[k]['year'] + ' ' + results[k]['season'];
                dropdown_options += '<option value="'+games+'">';
        }

        var gamesDropdownElement = document.getElementById('games_dropdown');
		if (gamesDropdownElement) {
			gamesDropdownElement.innerHTML = dropdown_options;
		}

    })

    .catch(function(error) {
        console.log(error);
    });

}

function propogateDropdown(field){
    var url = getAPIBaseURL() + '/olympics/dropdowns/' + field;
    fetch(url, {method: 'get'})

//     When the results come back, transform them from a JSON string into
//     a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

//     Once you have your list of author dictionaries, use it to build
//     an HTML table displaying the author names and lifespan.
    .then(function(results){
        var dropdown_options = '';
        for (var k = 0; k < results.length; k++){
                dropdown_options += '<option value="'+results[k]+'">';
        }

        var dropdownElement = document.getElementById(field+'_dropdown');
		if (dropdownElement) {
			dropdownElement.innerHTML = dropdown_options;
		}

    })

    .catch(function(error) {
        console.log(error);
    });

}

function get_dropdown_values(){
	var games_value = document.getElementById('games_btn').value;
	var teams_value = document.getElementById('teams_btn').value;
	var sports_value = document.getElementById('sports_btn').value;
	var events_value = document.getElementById('events_btn').value;
	var athletes_value = document.getElementById('athletes_btn').value;

	var search_params = {'games': games_value, 'team': teams_value,
                    'sport': sports_value, 'event': events_value,
                    'athlete': athletes_value};

    var api_addition = '?';
    for (var param in search_params){
        if(param == 'games' && search_params[param]){
            api_addition += param + '=' + search_params[param].slice(0,4) + '&';
        }
        else if (param != 'games' && search_params[param]){
            api_addition += param + '=' + search_params[param] + '&';
        }
    }
    return api_addition;
}

function go_forward(){
	direction = 'forward';
	tableOnClicked();
}

function go_backward(){
	direction = 'backward';
	tableOnClicked();
}
