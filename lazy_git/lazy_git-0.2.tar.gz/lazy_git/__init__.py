import os
from flask import Flask, jsonify
from tornado.options import options

__version__ = "0.2"

def create_app(config=None, repo_dir=None):
    app = Flask(__name__)

    # Grab configuration
    app.config.from_object('lazy_git.default_settings.{}Config'.format(
        os.environ.get('LAZY_GIT_MODE', 'Default')))
    if 'LAZY_GIT_CONFIG' in os.environ:
        assert os.path.isfile(os.environ['LAZY_GIT_CONFIG'])
        app.config.from_envvar('LAZY_GIT_CONFIG')
    if config is not None:
        assert os.path.isfile(config)
        app.config.from_pyfile(config)

    # Override REPO_DIR if passed explicitly
    if repo_dir:
        app.config['REPO_DIR'] = repo_dir

    # Expand ~ in REPO_DIR
    app.config['REPO_DIR'] = os.path.expanduser(app.config['REPO_DIR'])

    # Server status route
    @app.route("/info", methods=['GET'])
    def server_info():
        return jsonify({
            'version': __version__,
            'prefix': '{}/v{}'.format(app.config['URL_PREFIX'], __version__),
            'repo_dir': app.config['REPO_DIR']
        })

    # Allow cross-origin access to API
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Headers'] = \
            'Origin, X-Requested-With, Content-Type, Accept'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    app.after_request(add_cors_headers)

    # Register API blueprint
    from .api import browse_api
    app.register_blueprint(browse_api, url_prefix='{}/v{}/browse'.format(
        app.config['URL_PREFIX'], __version__))

    return app
