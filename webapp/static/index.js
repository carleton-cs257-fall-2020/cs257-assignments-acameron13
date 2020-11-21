/*
 * map-sample-world.js
 * Jeff Ondich
 * 11 November 2020
 *
 * Simple sample using the Datamaps library to show how to incorporate
 * a US map in your project.
 *
 * Datamaps is Copyright (c) 2012 Mark DiMarco
 * https://github.com/markmarkoh/datamaps
 */
var extraCountryInfo = {};
window.onload = initialize;

// This is example data that gets used in the click-handler below. Also, the fillColor
// specifies the color those countries should be. There's also a default color specified
// in the Datamap initializer below.


function initialize() {
	get_extra_country_info();
    // initializeMap();
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
        for(var country in results){
        	var medal_count = results[country].medal_count;
        	var fill_color = null;

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

			// console.log(country, medal_count, fill_color)
            if (results[country].games_list){
                extraCountryInfo[country].games_list = results[country].games_list;
            }
    		// console.log(country_info.country);
        }
    	console.log(extraCountryInfo)
    	initializeMap();
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

function initializeMap() {
    var map = new Datamap({ element: document.getElementById('map-container'), // where in the HTML to put the map
                            scope: 'world', // which map?
                            projection: 'equirectangular', // what map projection? 'mercator' is also an option
                            done: onMapDone, // once the map is loaded, call this function
                            data: extraCountryInfo, // here's some data that will be used by the popup template
                            fills: { defaultFill: '#e6e7ed' },
                            geographyConfig: {
                                //popupOnHover: false, // You can disable the hover popup
                                //highlightOnHover: false, // You can disable the color change on hover
                                popupTemplate: hoverPopupTemplate, // call this to obtain the HTML for the hover popup
                                borderColor: '#eeeeee', // state/country border color
                                highlightFillColor: '#FFC300', // color when you hover on a state/country
                                highlightBorderColor: '#000000', // border color when you hover on a state/country
                            }
                          });
}

// This gets called once the map is drawn, so you can set various attributes like
// state/country click-handlers, etc.
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
    var countrySummaryElement = document.getElementById('country-summary');
    if (countrySummaryElement) {
        var summary = '<p><strong>Country:</strong> ' + geography.properties.name + '</p>\n'
                    + '<p><strong>Abbreviation:</strong> ' + geography.id + '</p>\n';
        if (geography.id in extraCountryInfo) {
            var info = extraCountryInfo[geography.id];
            summary += '<p><strong>Population:</strong> ' + info.population + '</p>\n';
        }

        countrySummaryElement.innerHTML = summary;
    }
}
