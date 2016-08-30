from rest_framework import status, viewsets
from rest_framework.response import Response

from utm_zone_info.coordinate_reference_system import utm_zones_for_representing
from utm_zone_info.serializers import GeometrySerializer


class UTMZoneInfoViewSet(viewsets.ViewSet):
    """
    A simple ViewSet accepting a geometry and returning SRIDs of UTM Zones that can represent this geometry.
    """

    serializer_class = GeometrySerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            geometry = serializer.validated_data['geom']
            geometry.srid = serializer.validated_data['srid']
            data = dict(
                utm_zone_srids=[zone.srid for zone in utm_zones_for_representing(geometry)]
            )
            return Response(data=data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
