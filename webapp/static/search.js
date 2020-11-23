/* Alison Cameron and Adam Nik
   CS257 Software Design
   Carleton College
*/

var pageNum = 1;
var pageIndeces = {};
window.onload = initialize;

function initialize() {
    /*Auto-loads a table with no filters.

    If this page is loaded from clicking on a country from the map in index.html,
    the table is automatically filtered by that country.*/
	propogateDropdown('games');
	propogateDropdown('teams');
	propogateDropdown('sports');
	propogateDropdown('events');
	propogateDropdown('athletes');
    var fullLocationURL = window.location.href;
    var URLparts = fullLocationURL.split('=');

    //Check for navigation from index.html
    if (URLparts.length == 1){
        //Default load
    	newQuery();
    } else if (URLparts.length == 2){
        //Filter by country
    	document.getElementById('teams_btn').value = URLparts[1];
    	newQuery();
    }

	var submit = document.getElementById('search_submit');
	submit.onclick = newQuery;
	var back = document.getElementById('back');
	var forward = document.getElementById('forward');
	forward.onclick = goForward;
	back.onclick = goBackward;
}


function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function tableOnClicked(pageNum) {
    /*Gets table data from API and constructs HTML element*/
	var url = getAPIBaseURL() + '/olympics/search';
    var addition = getDropdownValues();
    url += addition;

    //Pagination
    if (pageNum in pageIndeces){
        var indeces = pageIndeces[pageNum];
        if (indeces[0] != null){
            url += '&first_entry=' + indeces[0];
        }
        if (indeces[1] != null){
            url += '&last_entry=' + indeces[1];
        }
    } else {
        if (pageNum != 1){
            prevIndeces = pageIndeces[pageNum - 1];
            prevLast = prevIndeces[1];
            url += '&prev_last_entry=' + prevLast;
        }
    }

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(results) {
        var lastEntry = results[0];
        var firstEntry = results[1];

        //Store indeces of table page for future use
        if (!(pageNum in pageIndeces)){
            pageIndeces[pageNum] = [firstEntry, lastEntry];
        }

        var tableBody = '<tr><th>Games</th><th>Team</th><th>Sport</th><th>Event</th><th>Medal</th><th>Athlete</th><th>Sex</th><th>Height</th><th>Weight</th><th>Birth Year</th></tr>';
        for (var k = 2; k < results.length; k++) {
            tableBody += '<tr>' + '<td>' + results[k]['games'] + '</td>'
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

		var resultsTableElement = document.getElementById('results');
		if (resultsTableElement) {
			resultsTableElement.innerHTML = tableBody;
		}

    })

    .catch(function(error) {
        console.log(error);
    });

}

function propogateDropdown(field){
    var url = getAPIBaseURL() + '/olympics/dropdowns?field=' + field;
    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(results){
        var dropdownOptions = '';
        for (var k = 0; k < results.length; k++){
        	if (field == 'games'){
        		games = results[k]['year'] + ' ' + results[k]['season'];
                dropdownOptions += '<option value="'+games+'">';
            } else{
                dropdownOptions += '<option value="'+results[k]+'">';
            }
        }

        var dropdownElement = document.getElementById(field+'_dropdown');
		if (dropdownElement) {
			dropdownElement.innerHTML = dropdownOptions;
		}

    })

    .catch(function(error) {
        console.log(error);
    });

}

function getDropdownValues(){
	var gamesValue = document.getElementById('games_btn').value;
	var teamsValue = document.getElementById('teams_btn').value;
	var sportsValue = document.getElementById('sports_btn').value;
	var eventsValue = document.getElementById('events_btn').value;
	var athletesValue = document.getElementById('athletes_btn').value;

	var searchParams = {'games': gamesValue, 'team': teamsValue,
                    'sport': sportsValue, 'event': eventsValue,
                    'athlete': athletesValue};

    var apiAddition = '?';
    for (var param in searchParams){
        if(param == 'games' && searchParams[param]){
            apiAddition += param + '=' + searchParams[param].slice(0,4) + '&';
        }
        else if (param != 'games' && searchParams[param]){
            apiAddition += param + '=' + searchParams[param] + '&';
        }
    }
    return apiAddition;
}

function goForward(){
    pageNum ++;
	tableOnClicked(pageNum);
}

function goBackward(){
    pageNum --;
    if (pageNum < 1){
    	pageNum = 1;
    }
	tableOnClicked(pageNum);
}

function newQuery(){
    pageNum = 1;
    pageIndeces = {};
    tableOnClicked(pageNum);
}
