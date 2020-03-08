var map = L.map('map').setView([52.531677, 13.381777], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

mapMarkers1 = [];

var source = new EventSource('http://127.0.0.1:8003/consumer/geostream'); //ENTER YOUR TOPICNAME HERE
source.addEventListener('message', function(e){

  console.log('Message' + e);
  obj = JSON.parse(e);
  console.log(obj);

  if(obj.name) {
    for (var i = 0; i < mapMarkers1.length; i++) {
      mymap.removeLayer(mapMarkers1[i]);
    }
    marker1 = L.marker([obj.lat, obj.lon]).addTo(map);
    mapMarkers1.push(marker1);
  }}, false);
