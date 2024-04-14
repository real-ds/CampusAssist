// Function to handle marker click events
function onMarkerClick(e) {
    var markerTitle = e.target.getPopup().getContent(); // Get marker title
    var columnIndex = e.target.options.column; // Get associated column index
    fetch(csvUrl) // Construct URL using baseUrl
        .then(response => response.text()) // Get response as text
        .then(data => {
            // Parse the CSV data
            var rows = data.split('\n');
            var columnData = '';
            // Extract the items from the desired column
            for (var i = 1; i < rows.length; i++) {
                var columns = rows[i].split(',');
                if (columns.length >= columnIndex) {
                    columnData += columns[columnIndex - 1] + '<br>'; // Extract item from the specified column
                }
            }
            // Display the list of items in the 'event-list' div
            var content = '<h2>' + markerTitle + '</h2><p>' + columnData + '</p>';
            content += '<button onclick="closeEventList()">Close</button>'; // Add close button
            document.getElementById('event-list').innerHTML = content;
            document.getElementById('event-list').classList.add('open');
        });
}

// Function to close the event list segment
function closeEventList() {
    document.getElementById('event-list').innerHTML = ''; // Clear the content
    document.getElementById('event-list').classList.remove('open'); // Remove the 'open' class
}

// Create the map object
var map = L.map('map', {
    maxZoom: 18, // Set maximum zoom level to 18
    zoomControl: false, // Disable zoom control
    scrollWheelZoom: false // Disable scroll wheel zooming
}).setView([12.842666, 80.154612], 17);

// Add the tile layer from OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Add custom markers with popups
var customIcon = L.icon({
    iconUrl: iconUrl,
    iconSize: [45, 60],
    iconAnchor: [16, 32],
    popupAnchor: [0, 0]
});

var markers = [
    L.marker([12.843995, 80.153438], {icon: customIcon, column: 1}).bindPopup("AB1"),
    L.marker([12.842947, 80.156505], {icon: customIcon, column: 2}).bindPopup("AB2"),
    L.marker([12.839659, 80.155106], {icon: customIcon, column: 4}).bindPopup("MG Auditorium"),
    L.marker([12.841641, 80.153817], {icon: customIcon, column: 6}).bindPopup("MBA Amphitheatre"),
    L.marker([12.841489, 80.154588], {icon: customIcon, column: 5}).bindPopup("Clock Tower"),
    L.marker([12.843622, 80.154640], {icon: customIcon, column: 3}).bindPopup("AB3")
];

// Add click event listeners to markers
markers.forEach(function(marker) {
    marker.on('click', onMarkerClick);
    marker.addTo(map);
});

// Resize map height dynamically based on viewport size
function resizeMap() {
    var mapElement = document.getElementById('map');
    mapElement.style.height =100;
}

// Trigger the resize event initially to set the correct height
window.addEventListener('resize', resizeMap);
window.addEventListener('DOMContentLoaded', resizeMap);
