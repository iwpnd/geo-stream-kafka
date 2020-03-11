var map = new L.Map('map');
var markersLayer = new L.LayerGroup();
var ws = new WebSocket("ws://127.0.0.1:8003/consumer/geostream");

var osmUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    osmAttribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    osm = new L.tileLayer(osmUrl, {maxZoom: 18, attribution: osmAttribution});

map.setView([52.521677, 13.391777], 15).addLayer(osm);

mapmarkers = {};

ws.onmessage = function(event) {
    console.log(event.data)
    console.log(mapmarkers)
    obj = JSON.parse(event.data)

    if(!(obj.name in mapmarkers)) {
      mapmarkers[obj.name] = [];
      mapmarkers[obj.name].push([obj.lat, obj.lon]);
    }
    else {
      mapmarkers[obj.name].push([obj.lat, obj.lon]);
    }

    marker = L.polyline(mapmarkers[obj.name], {color: 'blue', radius: 100}).addTo(map);

};
