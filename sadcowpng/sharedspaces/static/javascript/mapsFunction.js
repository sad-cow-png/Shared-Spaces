// whoa momma, a js file for my stuff!

// create some variables!
let map;
let infoWindow1, infoWindow2;
let my_counter = 0;
const umbcLatLng = {lat: 39.254, lng: -76.711};
const mapOptions = {
    // we can edit this to change map options that
    // we pass in to create the map
    center: umbcLatLng, // create map at UMBC lat/long (as a starting point)
    mapTypeId: 'roadmap',
    zoom: 15,
};

// Map initializes centered over UMBC.
// Map options fields alter appearance and interactive functionality of the embedded map.


function initMap() {
    // The map is embedded in the 'map' div found in index.html.
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
    infoWindow1 = new google.maps.InfoWindow( {
        content: 'Default text - window1',
        position : umbcLatLng, // use this as default position
        map:map,
    }); // done initializing infoWindow1
    // below we do the same

    infoWindow2 = new google.maps.InfoWindow( {
        content: 'Default text - window2',
        position : umbcLatLng, // use this as default position
        map:map,
    });  // this will be a test window

    const moveToCurrentLocation = document.createElement("button");
    moveToCurrentLocation.textContent = "Move to Current Location";
    moveToCurrentLocation.classList.add("custom-map-control-button");
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(moveToCurrentLocation);

    // below is some semi-complicated move to user position
    // code that works on the button
    moveToCurrentLocation.addEventListener("click", () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };
                    infoWindow1.setPosition(pos);
                    infoWindow1.setContent("Location found.");
                    infoWindow.open(map);
                    map.setCenter(pos);
                },
                () => {
                    handleLocationError(true, infoWindow, map.getCenter());
                }
            );
        } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, infoWindow, map.getCenter());
        }
    });




    // Enables users to place markers on the map.
    // addListener event just lets us listen for a "click" event
    // we will use addListener to the markers as well
    // note the mapListener is currently just a debug, we may not need it
    // and it will likely end up in a comment graveyard
    map.addListener('click', (event) => {
        // below we create a marker
        const marker = new google.maps.Marker({
            position: {lat: event.latLng.lat(), lng: event.latLng.lng()},
            map: map
        });
        // now I want this marker to have a listener to a click, so I can
        // click on it to see infoWindow 1
        marker.addListener('click', (event)=> {
            // this function is new, and is only called when
            // the marker we created with a click is clicked again
            // here I want to move the info window to open on the marker
            temp_marker_listener(my_counter);
            infoWindow2.open(map, marker);
            my_counter = my_counter+1;
        })
    });

    // TODO: When it is determined how the Space model will contain its location, you
    //       can then loop over those locations in the SQL database and add them as
    //       markers here.
    //       Using a google.maps.InfoWindow for each of these markers is likely the
    //       most efficient way to display the Space information when a user clicks
    //       on a space.

    function temp_marker_listener (counter) {
        if (typeof data != 'object') {
            infoWindow2.content = "There was a problem with the data";
        }
        if (typeof counter == 'number') {
            // so we have a number, and probably an array
            // lets print it out
            if (counter < data.length) {
                infoWindow2.content = make_html_content_from_array_element([counter])
            }
        }
    }

    function make_html_content_from_array_element (element) {
        // this takes the element (which should be just a space)
        // and makes a nice little html to shove in the infoWindow
        // elements are spaces, so they should have our
        //space_name and space_description
        // also, it is ugly, just let it be that way
        return "<div id=\"content\">" +
            "<div id=\"siteNotice\"></div>" +
            "<h1 id=\"firstHeading\" class=\"firstHeading\">"
        + element.space_name + "</h1>" + "<div id=\"bodyContent\">\n" +
            "    <p>" + element.space_description + "</p>\n" +
            "    </div>\n" +
            "</div>";
    }

}



// If google.maps.InfoWindows are decided to be used to display space information, additional wrapper
// functions similar to the one above will need to be placed here.



