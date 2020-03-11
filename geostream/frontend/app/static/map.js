var map = L.map('map').setView([52.531677, 13.381777], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

mapmarkers = {};

var ws = new WebSocket("ws://127.0.0.1:8003/consumer/geostream");
ws.onmessage = function(event) {
    console.log(event.data)
    obj = JSON.parse(event.data)

    if(!(obj.name in mapmarkers)) {
      mapmarkers[obj.name] = [];
      console.log(mapmarkers)
      mapmarkers[obj.name].push([obj.lat, obj.lon]);
    }
    else {
      console.log(mapmarkers)
      mapmarkers[obj.name].push([obj.lat, obj.lon]);
    }

    marker = L.polyline(mapmarkers[obj.name], {color: 'blue', radius: 100}).addTo(map);

};
