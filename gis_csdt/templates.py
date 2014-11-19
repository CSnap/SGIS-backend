from django.template import Template, Context
from gis_csdt.settings import GOOGLE_API_KEY
from gis_csdt.models import MapPoint
from gis_csdt.geometry_tools import circle_as_polygon
from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.contrib.gis.measure import Distance

def AroundPointView(request, mappoint_id = None):
	current_site = Site.objects.get_current()
	context = {'key': GOOGLE_API_KEY,
			   'zoom_level': 12,
			   'lat': 1,
			   'lon': 45,
			   'width': 500,
			   'height': 380,
			   'root': current_site.domain + '/'}
	if 'lat' in request.GET:
		context['lat'] = request.GET['lat']
	if 'lon' in request.GET:
		context['lon'] = request.GET['lon']
	if mappoint_id:
		try:
			mappoint = MapPoint.objects.get(id = mappoint_id)
			if mappoint.point.x != 0:
				context['lon'] = mappoint.point.x
			if mappoint.point.y != 0:
				context['lat'] = mappoint.point.y
		except Exception as e:
			pass

	if context['root'] == 'example.com/':
		context['root'] = 'http://127.0.0.1:8000/'
	context['circle']=''
	for d in [1,3,5]:
		circle = circle_as_polygon(lat = context['lat'], lon = context['lon'], distance = Distance(km=d))
		text = ''
		for coord in circle[0]: #external ring
			text = text + ',new google.maps.LatLng(%f, %f)\n' %(coord[1], coord[0])
		context['circle'] = context['circle'] + ',['+text.strip(',')+']'
	context['circle'] = '[' + context['circle'].strip(',') + ']'
	context = Context(context)
	template = """<!DOCTYPE HTML>
	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
	<script src="http://maps.googleapis.com/maps/api/js?key={{ key }}&sensor=false">
	</script>

	<script>
	var map;
	function initialize() {
		function add_circles(){
		  	var center = new google.maps.LatLng({{ lat }}, {{ lon }});
		  	for (var i=5;i>0;i-=2){
			  	var circleOptions = {
			      strokeColor: '#000000',
			      strokeOpacity: 0.8,
			      strokeWeight: 2,
			      fillColor: '#FF0000',
			      fillOpacity: 0.35,
			      map: map,
			      center: center,
			      radius: i * 1000
			    };
			    // Add the circle for this city to the map.
			    circle = new google.maps.Circle(circleOptions);
			}
		}
		function add_polygons(){
		  var polygon = new google.maps.Polygon({
		    paths: {{ circle }},
		    strokeColor: '#FF0000',
		    strokeOpacity: 0.8,
		    strokeWeight: 2,
		    fillColor: '#FF0000',
		    fillOpacity: 0.35
		  });
		  polygon.setMap(map);
		}
		function set_height(){
			var h = $(window).height();
		$('#googleMap').css('height', h);
		}
		$(window).resize(set_height());
		set_height();
		// Create a simple map.
		map = new google.maps.Map(document.getElementById('googleMap'), {
			zoom: {{ zoom_level }},
			center: {lat: {{ lat }}, lng:{{ lon }}}
		});

  		add_polygons();
	  // Load a GeoJSON from the same server as our demo.
	  google.maps.event.addListener(map, 'bounds_changed', function() {
	  	load_polys("{{ root }}api-poly/?max_lat=" + map.getBounds().getNorthEast().lat() + "&max_lon=" + map.getBounds().getNorthEast().lng() + "&min_lat=" + map.getBounds().getSouthWest().lat() + "&min_lon="+ map.getBounds().getSouthWest().lng());

		
		function load_polys(json_next) {
			$.getJSON(json_next)
			.done(function(data){
				for (var i = 0; i < data.results.length; i++){
					map.data.addGeoJson(data.results[i]);
				}
				json_next = data.next;
				if (data.next != null){
					load_polys(data.next);
				}
			});
		}	
		var featureStyle = {
    fillOpacity: 0,
    strokeWeight: 1
  }
  map.data.setStyle(featureStyle);

	  });

	}

	$( document ).ready(google.maps.event.addDomListener(window, 'load', initialize));

	</script>
	<div id="googleMap" style="width:100%;height:0px;"></div>
"""
	template = Template(template)
	return HttpResponse(template.render(context))