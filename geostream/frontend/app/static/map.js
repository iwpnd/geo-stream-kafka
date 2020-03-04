var map = L.map('map').setView([52.531677, 13.381777], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

L.marker([52.531677, 13.381777]).addTo(map)
    .bindPopup('im a placeholder')
    .openPopup();
