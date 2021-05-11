let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 2,
    minZoom: 2,
    maxZoom: 4
  });
}