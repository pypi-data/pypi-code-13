# coding: utf-8

RESOURCE_MAPPING = {
    'get_spreadsheet': {
        'resource': 'spreadsheets/{spreadsheet_id}',
        'docs': 'https://developers.google.com/sheets/reference/rest/v4/spreadsheets/get',
        'path_params': ['spreadsheet_id'],
        'methods': ['GET'],
        'remarks': 'No request parameters required'
    },
    'get_cells': {
        'resource': 'spreadsheets/{spreadsheet_id}/values/{range}',
        'docs': 'https://developers.google.com/sheets/reference/rest/v4/spreadsheets.values/get',
        'path_params': ['spreadsheet_id', 'range'],
        'methods': ['GET'],
        'remarks': 'No request parameters required'
    },
    'update_cells': {
        'resource': 'spreadsheets/{spreadsheet_id}/values/{range}',
        'docs': 'https://developers.google.com/sheets/reference/rest/v4/spreadsheets.values/update',
        'path_params': ['spreadsheet_id', 'range'],
        'methods': ['PUT'],
        'remarks': 'Request body to contain ValueRange object'
    }

}
