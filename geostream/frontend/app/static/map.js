var map = new L.Map('map');
var linesLayer = new L.LayerGroup();
var ws = new WebSocket("ws://127.0.0.1:8003/consumer/geostream");

var osmUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    osmAttribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    osm = new L.tileLayer(osmUrl, {maxZoom: 18, attribution: osmAttribution});

map.setView([52.521677, 13.391777], 15).addLayer(osm);

lines = {};

map.on("zoomend", function (e) { linesLayer.clearLayers() });

ws.onmessage = function(event) {
    console.log(event.data)
    obj = JSON.parse(event.data)

    if(!(obj.name in lines)) {
      lines[obj.name] = [];
      lines[obj.name].push([obj.lat, obj.lon]);
    }
    else {
      lines[obj.name].push([obj.lat, obj.lon]);
    }

    line = L.polyline(lines[obj.name], {color: 'blue', radius: 100})
    linesLayer.addLayer(line)
    map.addLayer(linesLayer);

};
