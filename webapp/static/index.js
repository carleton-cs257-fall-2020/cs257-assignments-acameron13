// Alison Cameron and Adam Nik

var extraCountryInfo = {};
var searchByNoc;
window.onload = initialize;

function initialize() {
	get_extra_country_info();
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function get_extra_country_info(){

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
        	var medal_count = results[country].medal_count;
        	var fill_color = '#e6e7ed';

        	if (medal_count > 0 && medal_count <= 1250){
        		fill_color = range1Fill;
        	} else if (medal_count > 1250 && medal_count <= 2500){
        		fill_color = range2Fill;
        	} else if (medal_count > 2500 && medal_count <= 3750){
        		fill_color = range3Fill;
        	} else if (medal_count > 3750 && medal_count <= 5000){
        		fill_color = range4Fill;
        	} else if (medal_count > 5000){
        		fill_color = range5Fill;
        	}

            extraCountryInfo[country] = {medalCount: medal_count, fillColor: fill_color};

            if (results[country].games_list){
                extraCountryInfo[country].games_list = results[country].games_list;
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

    if(data && extraCountryInfo[geography.id].games_list){
    	template += '<br>\n<strong>Hosted Games in:</strong><br>\n';
        games_list = extraCountryInfo[geography.id].games_list;
        for (i in games_list){
            games = games_list[i];
            template += games.year + ' ' + games.season + ', ' + games.city + '<br>\n';
        }
    }

    template += '</div>';
    return template;
}

function onCountryClick(geography) {
    // geography.properties.name will be the state/country name (e.g. 'Minnesota')
    // geography.id will be the state/country name (e.g. 'MN')
    // var countrySummaryElement = document.getElementById('country-summary');
    // if (countrySummaryElement) {
    //     var summary = '<p><strong>Country:</strong> ' + geography.properties.name + '</p>\n'
    //                 + '<p><strong>Abbreviation:</strong> ' + geography.id + '</p>\n';
    //     if (geography.id in extraCountryInfo) {
    //         var info = extraCountryInfo[geography.id];
    //         summary += '<p><strong>Population:</strong> ' + info.population + '</p>\n';
    //     }
    //
    //     countrySummaryElement.innerHTML = summary;
    // }
    noc = geography.id;
    // searchTeam(noc);
    console.log(noc);
    console.log(searchByNoc);
    //navigateAndSearch(noc);
    window.location.href = 'search.html?team=' + noc;
}
