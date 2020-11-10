// Alison Cameron and Adam Nik

window.onload = tableOnClicked;


function initialize() {
	var element = document.getElementById('search_submit');
	element.onclick = tableOnClicked;
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function tableOnClicked() {
// 	console.log('Hola amigo');
	var url = getAPIBaseURL() + '/olympics/search';
    
//     })
	
//     Send the request to the Books API /authors/ endpoint
    fetch(url, {method: 'get'})

//     When the results come back, transform them from a JSON string into
//     a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

//     Once you have your list of author dictionaries, use it to build
//     an HTML table displaying the author names and lifespan.
    .then(function(results) {
        // Build the table body.
        var tableBody = '<tr><th>Games</th><th>Team</th><th>Sport</th><th>Event</th><th>Medal</th><th>Athlete</th><th>Sex</th><th>Height</th><th>Weight</th><th>Birth Year</th></tr>';
        for (var k = 0; k < results.length; k++) {
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





