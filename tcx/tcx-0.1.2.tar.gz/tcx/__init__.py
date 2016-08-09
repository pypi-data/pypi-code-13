import xml.etree.ElementTree as ET
import re
import iso8601
from .__version__ import get_versions

__version__ = get_versions()['version']
del get_versions


def camel_to_snake(camel):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class TCX:
    namespaces = {
        'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
        'user_profile_v2': 'http://www.garmin.com/xmlschemas/UserProfile/v2',
        'profile_extension_v1': 'http://www.garmin.com/xmlschemas/ProfileExtension/v1',
        'activity_goals_v1': 'http://www.garmin.com/xmlschemas/ActivityGoals/v1',
        'activitiy_extension_v2': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2',
    }

    default_namespace = namespaces['tcx']

    trackpoint_properties = (
        ('tcx:Time', iso8601.parse_date),
        ('tcx:DistanceMeters', float),
        ('tcx:HeartRateBpm/tcx:Value', int, 'heart_rate_bpm'),
        ('tcx:Cadence', int),
        ('tcx:SensorState', str),
    )

    def __init__(self):
        pass

    def _xyz(self, trackpoint):
        xyz = [
            trackpoint.find('./tcx:Position/tcx:LongitudeDegrees', self.namespaces),
            trackpoint.find('./tcx:Position/tcx:LatitudeDegrees', self.namespaces),
            trackpoint.find('./tcx:AltitudeMeters', self.namespaces)]
        return [float(v.text) for v in xyz if v is not None]

    def _halfpoint(self, a, b):
        return [(a[i] + b[i]) / 2 for i in range(len(a))]

    def parse(self, tcx_data):
        root = ET.fromstring(tcx_data)
        activity = root.find('tcx:Activities/tcx:Activity', self.namespaces)

        fc = {
            'type': 'FeatureCollection',
            'features': [],
            'properties': {
                'totalMeters': 0.0,
                'totalSeconds': 0,
                'startTime': None,
                'sport': activity.get('sport', None)
            }
        }

        laps = activity.findall('tcx:Lap', self.namespaces)
        if len(laps):
            startTime = laps[0].get('StartTime', None)
            fc['properties']['startTime'] = iso8601.parse_date(startTime) if startTime else None

        for lap in laps:
            distance = lap.find('tcx:DistanceMeters', self.namespaces)
            distance = 0.0 if distance is None else float(distance.text)
            fc['properties']['totalMeters'] += distance

            duration = lap.find('tcx:TotalTimeSeconds', self.namespaces)
            duration = 0.0 if duration is None else float(duration.text)
            fc['properties']['totalSeconds'] += duration

            trackpoints = lap.findall('./tcx:Track/tcx:Trackpoint', self.namespaces)
            xyzs = [self._xyz(trackpoint) for trackpoint in trackpoints]
            for i in range(len(trackpoints)):
                line = None

                if i == 0:
                    line = [xyzs[0], self._halfpoint(xyzs[0], xyzs[1])]
                elif i == len(trackpoints) - 1:
                    line = [self._halfpoint(xyzs[-2], xyzs[-1]), xyzs[-1]]
                else:
                    line = [
                        self._halfpoint(xyzs[i - 1], xyzs[i]),
                        xyzs[i],
                        self._halfpoint(xyzs[i], xyzs[i + 1])]

                properties = {}

                ns_tag_re = re.compile(r'(?:{(?P<namespace>.+)})?(?P<tag>.+)')
                for item in self.trackpoint_properties:
                    element = trackpoints[i].find(item[0], self.namespaces)
                    if element is not None:
                        ns_tag = ns_tag_re.search(element.tag)
                        prefix = None
                        if ns_tag.group('namespace') != self.default_namespace:
                            prefix = next((prefix for (prefix, ns) in self.namespaces.items()))

                        tag = camel_to_snake(ns_tag.group('tag'))
                        name = item[2] if len(item) == 3 else tag
                        property_name = '%s__%s' % (prefix, name) if prefix else name
                        properties[property_name] = item[1](element.text)

                f = {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': line
                    },
                    'properties': properties
                }

                fc['features'].append(f)
        return fc
