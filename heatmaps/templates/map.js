google.charts.load('current', {
  'packages':['geochart'],
  'mapsApiKey': '{{ key }}'
});
google.charts.setOnLoadCallback(drawRegionsMap);

function drawRegionsMap() {
  var data = google.visualization.arrayToDataTable([
    ['Country', 'Value'],
  ]);

  var options = {};

  var chart = new google.visualization.GeoChart(document.getElementById('map'));

  chart.draw(data, options);
}
