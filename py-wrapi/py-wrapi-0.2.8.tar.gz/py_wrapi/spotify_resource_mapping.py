# coding: utf-8

RESOURCE_MAPPING = {
    'my_playlists': {
        'resource': 'me/playlists',
        'docs': 'https://developer.spotify.com/web-api/get-list-users-playlists/',
        'methods': ['GET'],
        'remarks': 'No request parameters required'
    },
    'my_profile': {
        'resource': 'me',
        'docs': 'https://developer.spotify.com/web-api/get-current-users-profile/',
        'methods': ['GET'],
        'remarks': 'No request parameters required'
    },
    'playlist_tracks': {
        'resource': 'users/{user_id}/playlists/{playlist_id}/tracks',
        'docs': 'https://developer.spotify.com/web-api/get-playlists-tracks/',
        'methods': ['GET'],
        'remarks': 'No request parameters required'
    }

}
