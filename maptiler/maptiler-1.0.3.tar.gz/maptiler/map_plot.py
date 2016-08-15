import json

from maptiler import MapPoint


class Map:
    def __init__(self, google_api_key=None):
        self.google_api_key = google_api_key
        self._entities = []

    def add_entity(self, entity):
        self._entities.append(entity)

    def to_file(self, file_path, **kwargs):
        html = self.draw(**kwargs)
        with open(file_path, 'w') as out_file:
            out_file.write(html)

    def draw(self, focus, zoom, map_styles=None):
        """
        :type focus: MapPoint
        :type zoom: float
        :type map_styles: dict
        :rtype: str
        """
        map_styles = map_styles or {}
        map_styles['center'] = '{center}'
        map_styles['zoom'] = zoom
        center = 'new google.maps.LatLng({focus}.latitude, {focus}.longitude)'.format(focus=focus.to_dict())
        draw_code = ''
        for entity in self._entities:
            draw_code += entity.draw()

        html = ("""
            <!DOCTYPE html>
            <html>
                <head>
                    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
                    <style type="text/css">
                        html { height: 100% }
                        body { height: 100%; margin: 0; padding: 0 }
                        #map-canvas { height: 100% }
                    </style>
                    <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js{google_api_key}"></script>
                    <script type="text/javascript">
                        function initialize() {
                            var mapOptions = {map_options};
                            map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
                            var markers = [];
                            {draw_code}
                        }
                        google.maps.event.addDomListener(window, 'load', initialize);
                    </script>
                </head>
                <body>
                    <div id="map-canvas"/>
                </body>
            </html>
        """ .replace('{map_options}', json.dumps(map_styles))
            .replace('"{center}"', center)
            .replace('{draw_code}', draw_code)
            .replace('{google_api_key}', ('?key={}'.format(self.google_api_key)) if self.google_api_key else ''))

        return html


class MapRect:
    def __init__(self, top_left, bottom_right, style=None):
        """
        Create a rectangle

        :type map_point_a: MapPoint
        :type map_point_b: MapPoint
        :type style: dict
        """

        self.top_left = top_left
        self.bottom_right = bottom_right
        self.style = style

    def draw(self):
        """
        >>> MapRect(MapPoint(10, 10), MapPoint(10, 20)).draw()
        """

        rect = self.style or {}
        rect['map'] = 'map'

        top_left = self.top_left.to_dict()
        bottom_right = self.bottom_right.to_dict()

        if top_left['longitude'] > bottom_right['longitude']:
            tmp = bottom_right['longitude']
            bottom_right['longitude'] = top_left['longitude']
            top_left['longitude'] = tmp

        if top_left['latitude'] < bottom_right['latitude']:
            tmp = bottom_right['latitude']
            bottom_right['latitude'] = top_left['latitude']
            top_left['latitude'] = tmp

        rect['map'] = '{map}'
        rect['bounds'] = "{bounds}"
        bounds = """
            new google.maps.LatLngBounds(
                new google.maps.LatLng({top_left}.latitude, {top_left}.longitude),
                new google.maps.LatLng({bottom_right}.latitude, {bottom_right}.longitude)
            )
        """.format(top_left=json.dumps(top_left), bottom_right=json.dumps(bottom_right), )

        output = """
            var rectangle = new google.maps.Rectangle({rect});
            markers.push(rectangle);
        """.replace('{rect}', json.dumps(rect)).replace('"{map}"', 'map').replace('"{bounds}"', bounds)
        return output


class MapCircle:
    def __init__(self, center, radius, style=None):
        """
        Create a circle.

        :type center: MapPoint
        :type radius: float
        :type style: dict
        """

        self.center = center
        self.radius = radius
        self.style = style

    def draw(self):
        circle = self.style or {}
        circle['map'] = '{map}'

        center = self.center.to_dict()

        circle['center'] = "{center}"
        circle['radius'] = self.radius
        lat_lon = """
            new google.maps.LatLng({center}.latitude, {center}.longitude)
        """.format(center=json.dumps(center))

        output = """
            var circle = new google.maps.Circle({circle});
            markers.push(circle);
        """.replace('{circle}', json.dumps(circle)).replace('"{map}"', 'map').replace('"{center}"', lat_lon)

        return output


class MapMarker:
    def __init__(self, position, style=None):
        """Create a rectangle

        :type position: MapPoint
        :type style: dict
        """
        self.position = position
        self.style = style

    def draw(self):
        marker = self.style or {}
        marker['map'] = '{map}'

        position = self.position.to_dict()

        marker['position'] = "{position}"
        lat_lon = """
            new google.maps.LatLng({center}.latitude, {center}.longitude)
        """.format(center=json.dumps(position))

        output = """
            var marker = new google.maps.Marker({marker});
            markers.push(marker);
        """.replace('{marker}', json.dumps(marker)).replace('"{map}"', 'map').replace('"{position}"', lat_lon)

        return output
