from time_aware_polyline import decode_time_aware_polyline, encode_time_aware_polyline


gpx_logs = [
    [19.13626, 72.92506, '2016-07-21T05:43:09+00:00'],
    [19.13597, 72.92495, '2016-07-21T05:43:15+00:00'],
    [19.13553, 72.92469, '2016-07-21T05:43:21+00:00'],
]


time_aware_polyline = 'spxsBsdb|Lymo`qvAx@TKvAr@K'


def test_if_decoded_correctly():
    decoded = decode_time_aware_polyline(time_aware_polyline)
    assert decoded == gpx_logs


def test_if_encoded_correctly():
    encoded = encode_time_aware_polyline(gpx_logs)
    assert encoded == time_aware_polyline
