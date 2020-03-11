var map = new L.Map('map');
var linesLayer = new L.LayerGroup();
var ws = new WebSocket("ws://127.0.0.1:8003/consumer/geostream");

var osmUrl = 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
    osmAttribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    osm = new L.tileLayer(osmUrl, {maxZoom: 18, attribution: osmAttribution});

var colors = ["#8be9fd", "#50fa7b", "#ffb86c", "#ff79c6", "#bd93f9", "#ff5555", "#f1fa8c"];

map.setView([52.521677, 13.391777], 15).addLayer(osm);

lines = {};

map.on("zoomend", function (e) { linesLayer.clearLayers() });

ws.onmessage = function(event) {
    console.log(event.data)
    obj = JSON.parse(event.data)

    if(!(obj.name in lines)) {
      lines[obj.name] = {"latlon": []};
      lines[obj.name]["latlon"].push([obj.lat, obj.lon]);
      lines[obj.name]["config"] = {"color": colors[Math.floor(Math.random()*colors.length)]};
    }
    else {
      lines[obj.name]["latlon"].push([obj.lat, obj.lon]);
    }

    line = L.polyline(lines[obj.name]["latlon"], {color: lines[obj.name]["config"]["color"]})
    linesLayer.addLayer(line)
    map.addLayer(linesLayer);

};
