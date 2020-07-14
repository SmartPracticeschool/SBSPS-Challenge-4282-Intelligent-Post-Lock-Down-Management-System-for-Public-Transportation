var infoWindow = new google.maps.InfoWindow;

function initMap() {
  var directionsService = new google.maps.DirectionsService();
  var directionsRenderer = new google.maps.DirectionsRenderer();
  var mumbai = new google.maps.LatLng(19.082439, 72.808222);
  var mapOptions = {
    zoom:11,
    center: mumbai
  }

  var map = new google.maps.Map(document.getElementById('map'), mapOptions);
  directionsRenderer.setMap(map);
  
  downloadUrl('/static/xml/loc.xml', function(data) {
    var xml = data.responseXML;
    var markers = xml.getElementsByTagName("item")
    Array.prototype.forEach.call(markers, function(markerElem) {
      var id = markerElem.getElementsByTagName("STOP_ID")[0].childNodes[0].nodeValue;
      var name = markerElem.getElementsByTagName("NAME")[0].childNodes[0].nodeValue;
      var address = markerElem.getElementsByTagName("ADDRESS")[0].childNodes[0].nodeValue;
      var type  = markerElem.getElementsByTagName("TYPE")[0].childNodes[0].nodeValue;
      var point = new google.maps.LatLng(
        parseFloat(markerElem.getElementsByTagName("LAT")[0].childNodes[0].nodeValue),
        parseFloat(markerElem.getElementsByTagName("LNG")[0].childNodes[0].nodeValue));
        
        var infowincontent = document.createElement('div');
        var strong = document.createElement('strong');
        strong.textContent = name
        infowincontent.appendChild(strong);
        infowincontent.appendChild(document.createElement('br'));
        
        var text = document.createElement('text');
        text.textContent = address
        infowincontent.appendChild(text);
        
        var marker = null;
        
        var icons = { 
          icon: '/static/images/stop.png'
        };
        
        marker = new google.maps.Marker({
          map: map,
          position: point,
          icon : icons.icon
        });
        
        marker.addListener('click', function() {
          infoWindow.setContent(infowincontent);
          infoWindow.open(map, marker);
        });
      });
    });
    
    document.getElementById('submit').addEventListener('click', function() {
      calcRoute(directionsService, directionsRenderer);
    });
  }
  function calcRoute(directionsService, directionsRenderer) {
    var start = document.getElementById('origin').value;
    var end = document.getElementById('destination').value;
    
    var request = {
      origin: start,
      destination: end,
      travelMode: 'TRANSIT',
      drivingOptions: {
        departureTime: new Date(Date.now()), 
        trafficModel: 'optimistic'
      },
      transitOptions: {
        // modes: ['BUS','TRAIN'],
        // routingPreference: 'FEWER_TRANSFERS',
        routingPreference: 'LESS_WALKING',
      },
    };
    directionsService.route(request, function(result, status) {
      if (status == 'OK') {
        directionsRenderer.setDirections(result);
      }
      else if( status == 'ZERO_RESULTS') {
        alert("No data found");
      }
    });
  }
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };              
      infoWindow.setPosition(pos);
      infoWindow.setContent('Location found.');
      infoWindow.open(map);
      map.setCenter(pos);
    }, 
    function() {
      handleLocationError(true, infoWindow, map.getCenter());
    });
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, map.getCenter());
  }    
  function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
      'Error: The Geolocation service failed.' :
      'Error: Your browser doesn\'t support geolocation.');
      infoWindow.open(map);
    }
    
    function downloadUrl(url, callback) {
      var request = window.ActiveXObject ?
      new ActiveXObject('Microsoft.XMLHTTP') :
      new XMLHttpRequest;
      
      request.onreadystatechange = function() {
        if (request.readyState == 4) {
          request.onreadystatechange = doNothing;
          callback(request, request.status);
        }
      };
      
      request.open('GET', url, true);
      request.send(null);
    }
    
    function doNothing() {}