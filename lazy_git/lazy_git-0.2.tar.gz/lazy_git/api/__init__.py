from flask import Blueprint
from .browse_api import BrowseApi

browse_api = Blueprint('browse_api', __name__)
browse_view = BrowseApi.as_view('browse')

browse_api.add_url_rule('/<repo_name>/', defaults={'obj_path': 'HEAD:'},
    view_func=browse_view)
browse_api.add_url_rule('/<repo_name>/<path:obj_path>',
    view_func=browse_view)
