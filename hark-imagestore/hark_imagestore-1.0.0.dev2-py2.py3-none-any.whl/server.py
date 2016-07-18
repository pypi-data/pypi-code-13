from flask import Flask, jsonify

from hark.models.image import Image
from hark_imagestore.lib.server import HTTPServer

from hark.imagestore import URLS


def make_app(image_cache):
    "Create an imagestore web app instance"
    app = Flask('hark_imagestore')

    @app.route('/')
    def index():
        return jsonify({
            URLS['index']: 'Show the API index',
            URLS['images']: 'Show all available images',
            URLS['image']: 'Get the URL for an image download'
        })

    @app.route('/images')
    def images():
        images = image_cache.images()
        return jsonify(images)

    @app.route('/image/<guest>/<driver>/<version>')
    def get_image_detail(guest, driver, version):
        # construct the image from the request
        im = Image(guest=guest, driver=driver, version=int(version))
        s3_path = image_cache.full_image_path(im)
        return jsonify({
            'url': s3_path,
        })

    return app


class ImagestoreServer(HTTPServer):
    "Subclasses HTTPServer to set the app to an imagestore app"
    def __init__(self, image_cache, port, workers):
        HTTPServer.__init__(self, make_app(image_cache), port, workers)
