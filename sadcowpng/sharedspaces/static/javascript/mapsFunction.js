// whoa momma, a js file for my stuff!

// create some variables!


const umbcLatLng = {lat: 39.256, lng: -76.717};
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
            content: "nothing",
    });
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
                    infoWindow1.open(map);
                    map.setCenter(pos);
                },
                () => {
                    handleLocationError(true, infoWindow1, map.getCenter());
                }
            );
        } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, infoWindow1, map.getCenter());
        }
    });

    // We have a button that centers you on your location
    // we should now try to loop through out data
    for (var i = 0; i < data.length; i++) {
        create_marker(data[i]);
    }




/* Comment graveyard here, if you want you can let the map's clicks spawn markers
that don't do anything
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

 */

    // TODO: When it is determined how the Space model will contain its location, you
    //       can then loop over those locations in the SQL database and add them as
    //       markers here.
    //       Using a google.maps.InfoWindow for each of these markers is likely the
    //       most efficient way to display the Space information when a user clicks
    //       on a space.
/*
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
*/

}

function make_html_from_obj (obj) {
    // this takes the element (which should be just a space)
    // and makes a nice little html to shove in the infoWindow
    // elements are spaces, so they should have our
    // space_name and space_description
    // also, it is ugly, just let it be that way
    //return "obj.spc_name";
    return "<div> <h1>" + obj["spc_name"] + "</h1> <div> <p>" + obj["spc_desc"]+ "</p></div> </div>";
}

function create_marker(obj) {
    // no error checking here, we raw dogging
    var pos;
    // here we take the object and get a pos out of it
    pos = obj_to_pos(obj);
    // now we create a marker
    var marker = new google.maps.Marker({
        position: {lat: pos.lat, lng: pos.lng},
        map: map, // default map
        });
    marker.addListener('click', (event)=> {
        infoWindow2 = new google.maps.InfoWindow( {
            content: make_html_from_obj(obj),
        });
        infoWindow2.open(map,marker);
    });
}

function obj_to_pos(obj) {
    return umbcLatLng; // temp value to put markers on the map
}




function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );
  infoWindow.open(map);
}
// If google.maps.InfoWindows are decided to be used to display space information, additional wrapper
// functions similar to the one above will need to be placed here.



