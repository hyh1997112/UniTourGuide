function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), { zoom: 4, center: { lat: 40.7052967, lng: -74.0130652 } });
    $("input[name='school_positions']").each(function () {
        var position = this.value;
        var name = position.split("#")[0];
        var lat = parseFloat(position.split("#")[1]);
        var lng = parseFloat(position.split("#")[2]);
        var description = position.split("#")[3];
        var url = position.split("#")[4];
        var marker = new google.maps.Marker({ position: { lat: lat, lng: lng }, map: map });
        var contentString = '<div id="content">' +
            '<div id="siteNotice">' +
            '</div>' +
            '<p><b>' + name + '</b></p>' +
            '<p>' + description + '</p>' +
            '<div id="bodyContent">' +
            '<a href="' + url + '">View Guides</a> ' +
            '</div>' +
            '</div>';
        var infowindow = new google.maps.InfoWindow({
            content: contentString
        });
        marker.addListener('click', function () {
            infowindow.open(map, marker);
        });
    });
}