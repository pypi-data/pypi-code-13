import math

EARTH_RADIUS = 6378137.0  # max elipsoid radius of earth


def _deg2rad(deg):
    return deg * (math.pi/180)


class MapPoint:
    def __init__(self, latitude, longitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def __repr__(self):
        return '<%s: %.3f, %.3f>' % (self.__class__.__name__, self.latitude, self.longitude)

    def distance(self, point_b):
        """
        Calculate the distance between two MapPoints in meters.

        >>> MapPoint(0, 0).distance(MapPoint(0, 0))
        0.0

        >>> round(MapPoint(0, 0).distance(MapPoint(100, 0)), 2)
        11131949.08

        >>> round(MapPoint(0, 0).distance(MapPoint(0, 50)), 2)
        5565974.54

        >>> round(MapPoint(24, 74).distance(MapPoint(-30, 50)), 2)
        6535444.46

        >>> round(MapPoint(24, 74).distance(MapPoint(30, 50)), 2)
        2467027.04
        """
        d_lat = _deg2rad(point_b.latitude - self.latitude)
        d_lng = _deg2rad(point_b.longitude - self.longitude)

        a = (pow(math.sin(d_lat/2), 2) +
             math.cos(_deg2rad(self.latitude)) *
             math.cos(_deg2rad(point_b.latitude)) *
             pow(math.sin(d_lng/2), 2))

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return EARTH_RADIUS * c

    def to_dict(self):
        return {'latitude': self.latitude, 'longitude': self.longitude}


class MapTile:
    def __init__(self, x, y, map_tiler):
        """

        :type x: int
        :type y: int
        :type map_tiler: MapTiler
        :return:
        """
        self.map_tiler = map_tiler
        self.x = int(x)
        self.y = int(y)
        self.bounds = self._bounds()
        self.latitude = self.bounds[0].latitude
        self.longitude = self.bounds[0].longitude
        self.hash = self._hash()

    def __repr__(self):
        return '<%s: %d, %d>' % (self.__class__.__name__, self.x, self.y)

    def _bounds(self):
        """
        Calculate the bounding box corners of this tile.

        >>> MapTile(130, 20, MapTiler(square_size=1500000)).bounds
        [<MapPoint: 269.495, -198583.765>, <MapPoint: 269.495, -200111.333>, <MapPoint: 282.969, -200111.333>, <MapPoint: 282.969, -198583.765>]

        >>> MapTile(-130, 20, MapTiler(square_size=1500000)).bounds
        [<MapPoint: 269.495, 197056.198>, <MapPoint: 269.495, 198583.765>, <MapPoint: 282.969, 198583.765>, <MapPoint: 282.969, 197056.198>]

        >>> MapTile(-130, -20, MapTiler(square_size=1500000)).bounds
        [<MapPoint: -256.020, 7195.130>, <MapPoint: -256.020, 7250.907>, <MapPoint: -269.495, 7250.907>, <MapPoint: -269.495, 7195.130>]
        """
        x_neg = self.x < 0
        y_neg = self.y < 0

        if x_neg:
            x_pos = -self.x - 1
        else:
            x_pos = self.x

        if y_neg:
            y_pos = -self.y - 1
        else:
            y_pos = self.y

        latitude = y_pos * self.map_tiler.angle_step_deg

        # calculate the earth circumference at this latitude
        longitude_circumference = math.cos(y_pos * self.map_tiler.angle_step_rad) * EARTH_RADIUS * 2 * math.pi
        longitude_angle_step_deg = self.map_tiler.square_size / longitude_circumference * 360

        longitude = x_pos * longitude_angle_step_deg
        # latitude_b

        if x_neg:
            longitude = -longitude
            longitude_b = longitude - longitude_angle_step_deg
        else:
            longitude_b = longitude + longitude_angle_step_deg

        if y_neg:
            latitude = -latitude
            latitude_b = latitude - self.map_tiler.angle_step_deg
        else:
            latitude_b = latitude + self.map_tiler.angle_step_deg

        return [MapPoint(latitude, longitude), MapPoint(latitude, longitude_b),
                MapPoint(latitude_b, longitude_b), MapPoint(latitude_b, longitude)]

    def _hash(self):
        if None in (self.map_tiler.hash_min_x, self.map_tiler.hash_min_y):
            return None
        width = -self.map_tiler.hash_min_x * 2 - 1
        height = -self.map_tiler.hash_min_y * 2 - 1
        x = (self.x - self.map_tiler.hash_min_x) % width
        y = (self.y - self.map_tiler.hash_min_y) % height
        return y * width + x

    def to_dict(self):
        return {'x': self.x, 'y': self.y, 'bounds': [bound.to_dict() for bound in self.bounds]}


class MapTiler:
    def __init__(self, square_size=None):
        if square_size is None:
            square_size = 200 * 1000
        self.square_size = float(square_size)
        self.earth_circumference = 2 * math.pi * EARTH_RADIUS
        self.angle_fraction = self.square_size / self.earth_circumference
        self.angle_step_rad = self.angle_fraction * 2 * math.pi
        self.angle_step_deg = self.angle_fraction * 360
        self.hash_min_x = None
        self.hash_min_y = None
        self.hash_min_x = self.tile(MapPoint(0, -180)).x
        self.hash_min_y = self.tile(MapPoint(-90, 0)).y

    def tile(self, point):
        """
        Get the MapTile for given map point.

        :type point: MapPoint
        :rtype :MapTile
        >>> MapTiler(square_size=1500000).tile(MapPoint(0, 0))
        <MapTile: 0, 0>

        >>> MapTiler(square_size=1500000).tile(MapPoint(-40, 80))
        <MapTile: 5, -3>

        >>> MapTiler(square_size=1500000).tile(MapPoint(40, 80))
        <MapTile: 5, 2>

        >>> MapTiler(square_size=1500000).tile(MapPoint(200, 200))
        <MapTile: -15, 14>

        >>> MapTiler(square_size=200000).tile(MapPoint(200, 200))
        <MapTile: -105, 111>
        """
        latitude = point.latitude
        longitude = point.longitude

        x_neg = longitude < 0
        y_neg = latitude < 0

        if x_neg:
            longitude = -longitude

        if y_neg:
            latitude = -latitude

        y_pos = math.floor(latitude/self.angle_step_deg)

        # calculate the earth circumference at this latitude
        longitude_circumference = math.cos(y_pos * self.angle_step_rad) * EARTH_RADIUS * 2 * math.pi

        # calculate the step size in degrees at this latitude
        longitude_angle_step_deg = self.square_size / longitude_circumference * 360

        x_pos = math.floor(longitude/longitude_angle_step_deg)

        if x_neg:
           x_pos = -x_pos - 1

        if y_neg:
            y_pos = -y_pos - 1

        return MapTile(x_pos, y_pos, self)

    def tiles_for_point(self, point, radius):
        """
        Get the tiles that are withing the radius at point
        :type point: MapPoint
        :type radius: float

        >>> MapTiler(square_size=2000).tiles_for_point(MapPoint(50, 50), 2000)
        [<MapTile: 1789, 2782>, <MapTile: 1790, 2782>, <MapTile: 1788, 2782>, <MapTile: 1788, 2783>, <MapTile: 1789, 2783>, <MapTile: 1787, 2783>]

        >>> MapTiler(square_size=2000).tiles_for_point(MapPoint(-50, -50), 2000)
        [<MapTile: -1790, -2783>, <MapTile: -1789, -2783>, <MapTile: -1791, -2783>, <MapTile: -1789, -2784>, <MapTile: -1788, -2784>, <MapTile: -1790, -2784>]

        >>> MapTiler(square_size=2000).tiles_for_point(MapPoint(-80, 100), 2000)[:3]
        [<MapTile: 967, -4453>, <MapTile: 968, -4453>, <MapTile: 966, -4453>]

        >>> MapTiler(square_size=2000).tiles_for_point(MapPoint(-80, 100), 2000)[3:6]
        [<MapTile: 969, -4452>, <MapTile: 970, -4452>, <MapTile: 968, -4452>]

        >>> MapTiler(square_size=2000).tiles_for_point(MapPoint(-80, 100), 2000)[6:9]
        [<MapTile: 966, -4454>, <MapTile: 967, -4454>, <MapTile: 965, -4454>]

        """

        center_tile = self.tile(point)

        found_tiles = []

        def _find_tiles_horizontally(tile):
            for bound_h in tile.bounds:
                if point.distance(bound_h) < radius:
                    found_tiles.append(tile)
                    return True
            return False

        def _find_tiles_vertically(tile):
            for bound_v in tile.bounds:
                if point.distance(bound_v) < radius:
                    found_tiles.append(tile)

                    # go horizontally through space(x coord of tile) and find tiles that are within radius
                    # we don't need to check center tile again
                    for horizontal in range(1, int(radius/self.square_size + 2), 1):
                        found = False
                        # go east from center
                        horizontal_tile = MapTile(tile.x + horizontal, tile.y, map_tiler=self)
                        found = _find_tiles_horizontally(tile=horizontal_tile)

                        # go west from center
                        horizontal_tile = MapTile(tile.x - horizontal, tile.y, map_tiler=self)
                        found = _find_tiles_horizontally(tile=horizontal_tile) or found

                        # if nothing found, we don't need to keep looking, since we would go further away
                        if not found:
                            break
                    return True
            return False

        # go vertically through space(latitude) and find tiles that are within radius
        for vertical in range(0, int(radius/self.square_size + 2), 1):
            # go north from center
            vertical_tile = self.tile(MapPoint(point.latitude + self.angle_step_deg * vertical, point.longitude))
            found = _find_tiles_vertically(vertical_tile)

            if vertical > 0:
                # go south
                vertical_tile = self.tile(MapPoint(point.latitude - self.angle_step_deg * vertical, point.longitude))
                found = _find_tiles_vertically(vertical_tile) or found

            # if nothing found, we don't need to keep looking, since we would go further away
            if not found:
                break
        if not found_tiles:
            found_tiles = [center_tile]
        return found_tiles


