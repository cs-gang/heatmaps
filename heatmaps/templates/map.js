let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 2,
    minZoom: 2,
    maxZoom: 3,
    mapTypeControl: false,
    streetViewControl: false,
    zoomControlOptions: {
      position: google.maps.ControlPosition.BOTTOM_CENTER
    },
    fullscreenControlOptions: {
      position: google.maps.ControlPosition.BOTTOM_CENTER
    }
  });
}