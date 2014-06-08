var initialLocation;
var singapore = new google.maps.LatLng(1.297553,103.849495);
var browserSupportFlag = new Boolean();

var xmlhttp;
//if (str=="")
//  {
//  document.getElementById("txtHint").innerHTML="";
//  return;
//  }
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp=new XMLHttpRequest();
  }
else
  {// code for IE6, IE5
  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }

xmlhttp.open('GET','/getpost',true)
xmlhttp.send()

var places = [];

xmlhttp.onreadystatechange=function() {
	if (xmlhttp.readyState==4 && xmlhttp.status==200) {
	    var posts=xmlhttp.responseText;
	    posts = posts.split('), (');
	    for (post in posts) {
		places.push(posts[post].split(', '));
	    }
	}
    }


function initialize() {
	var mapOptions = {
		zoom: 15,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	var map = new google.maps.Map(document.getElementById("map-canvas"),
		mapOptions);

	// Try W3C Geolocation (Preferred)
	if(navigator.geolocation) {
	browserSupportFlag = true;
	navigator.geolocation.getCurrentPosition(function(position) {
	  initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
	  map.setCenter(initialLocation);
	}, function() {
	  handleNoGeolocation(browserSupportFlag);
	});
	}
	// Browser doesn't support Geolocation
	else {
	browserSupportFlag = false;
	handleNoGeolocation(browserSupportFlag);
	}

	function handleNoGeolocation(errorFlag) {
	if (errorFlag == true) {
	  alert("Geolocation service failed.");
	  initialLocation = singapore;
	} else {
	  alert("Your browser doesn't support geolocation.");
	  initialLocation = singapore;
	}
	map.setCenter(initialLocation);
	}
	setMarkers(map,places);
	function setMarkers(map, places) {
		for (var i = 0; i < places.length; i++) {
			var place = places[i];
			var name = place[0].slice(2,-1);
			var myLatLng = new google.maps.LatLng(parseFloat(place[1]), parseFloat(place[2]));
			var rating = parseInt(places[3]);
			var marker = new google.maps.Marker({
				position: myLatLng,
				labelContent: rating,
				labelAnchor: new google.maps.Point(22, 0),
				labelInBackground: false,
				icon: ['/static/img/marker-green.png','/static/img/marker-yellow.png','/static/img/marker-red.png'][Math.floor(Math.random() * 3)],
				map: map,
				title: place[0].slice(2,-1),
				url: '/#'+ name +'_locationPage'
			});
			google.maps.event.addListener(marker, 'click', function() {
				window.location.href = this.url;
			});
		}
	}
}

google.maps.event.addDomListener(window, 'load', initialize);