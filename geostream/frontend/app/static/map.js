var map = L.map('map').setView([52.531677, 13.381777], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

mapMarkers1 = [];

var ws = new WebSocket("ws://127.0.0.1:8003/consumer/geostream");
ws.onmessage = function(event) {
    console.log(event.data)

    obj = JSON.parse(event.data)

    if(obj.name) {
      for (var i = 0; i < mapMarkers1.length; i++) {
        map.removeLayer(mapMarkers1[i]);
      }
      marker1 = L.marker([obj.lat, obj.lon]).addTo(map);
      mapMarkers1.push(marker1);
    }

};
