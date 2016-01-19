$(function() {
	var servs = $("#nvoserv");
	function buscarte() {
		if (window.navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(geo, errorcito);
		} else {
			alert("Su navegador no tiene funciones para la GeoLocalzación");
		}
	}

	function geo(position) {
		var latitud = position.coords.latitude;
		var longitud = position.coords.longitude;
		alert(latitud, longitud);
		$.ajax({
			url: ubicacion,
			type: 'POST',
			dataType: "json",
			data: { "lon": longitud, "lat": lattitud, csrfmiddlewaretoken : csrf},
			error: function(a,b,c){
				alert("ERROR: "+JSON.stringify(a)+'--->'+b+'--->'+c);
			},
			success: function(datos){
				alert(datos);
				servs.empty();
				servs.append(datos);
				/*
					$.each(datos.features, function(index, val) {
						console.log(val.properties.nombre);
						var name = val.properties.nombre;
						var description = val.properties.url;
						servs.append(name);
						servs.append(description);
					}
				*/
			}
		}); 
	}
	function errorcito(errores){
		alert(JSON.stringify(errores));
	}
	buscarte();
});