/* Alison Cameron and Adam Nik
   CS257 Software Design
   Carleton College

   Datamaps is Copyright (c) 2012 Mark DiMarco
   https://github.com/markmarkoh/datamaps

   Datamaps is edited in this repository so that the country id's
   match the ids in our dataset.
*/

var extraCountryInfo = {};
window.onload = initialize;

function initialize() {
	getExtraCountryInfo();
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function getExtraCountryInfo(){
	var range1Fill = '#b5b7ca';
	var range2Fill = '#8487a7';
	var range3Fill = '#535784';
	var range4Fill = '#3b3f73';
	var range5Fill = '#0a0f50';
	var url = getAPIBaseURL() + '/olympics/countries';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(results) {
        for(var country in results){
        	var countryMedalCount = results[country].medal_count;
        	var countryFillColor = '#e6e7ed';

        	if (countryMedalCount > 0 && countryMedalCount <= 1250){
        		countryFillColor = range1Fill;
        	} else if (countryMedalCount > 1250 && countryMedalCount <= 2500){
        		countryFillColor = range2Fill;
        	} else if (countryMedalCount > 2500 && countryMedalCount <= 3750){
        		countryFillColor = range3Fill;
        	} else if (countryMedalCount > 3750 && countryMedalCount <= 5000){
        		countryFillColor = range4Fill;
        	} else if (countryMedalCount > 5000){
        		countryFillColor = range5Fill;
        	}

            extraCountryInfo[country] = {medalCount: countryMedalCount, fillColor: countryFillColor};
            if (results[country].games_list){
                extraCountryInfo[country].gamesList = results[country].games_list;
            }
        }
    	initializeMap();
    })

    .catch(function(error) {
        console.log(error);
    });
}

function initializeMap() {
    var map = new Datamap({ element: document.getElementById('map-container'),
                            scope: 'world',
                            projection: 'equirectangular',
                            done: onMapDone,
                            data: extraCountryInfo,
                            fills: { defaultFill: '#e6e7ed' },
                            geographyConfig: {
                                popupTemplate: hoverPopupTemplate,
                                borderColor: '#eeeeee',
                                highlightFillColor: '#FFC300',
                                highlightBorderColor: '#000000',
                            }
                          });
}

function onMapDone(dataMap) {
    dataMap.svg.selectAll('.datamaps-subunit').on('click', onCountryClick);
}

function hoverPopupTemplate(geography, data) {
    var medals;
    if (data == null) {
        medals = 0;
    } else {
        medals = data.medalCount;
    }

    var template = '<div class="hoverpopup"><strong>' + geography.properties.name + '</strong><br>\n'
                    + '<strong>Total Medals:</strong> ' + medals + '<br>\n';

    if(data && extraCountryInfo[geography.id].gamesList){
    	template += '<br>\n<strong>Hosted Games in:</strong><br>\n';
        countryGamesList = extraCountryInfo[geography.id].gamesList;
        for (i in countryGamesList){
            games = countryGamesList[i];
            template += games.year + ' ' + games.season + ', ' + games.city + '<br>\n';
        }
    }

    template += '</div>';
    return template;
}

function onCountryClick(geography) {
    /*When a country in the map is clicked, onCountryClick will navigate to
    search.html and automatically filter by said country.*/
    noc = geography.id;
    window.location.href = 'search.html?team=' + noc;
}
