# coding: utf-8

from flask import Flask, jsonify
from mongoengine.errors import DoesNotExist

from twitprof.models import TwitterUser, connect_to_database
from twitprof.tasks.tasks import store_twitter_user


def create_flask_app():
    app = Flask(__name__)
    app.config.from_envvar('TWITPROF_API_SETTINGS')
    connect_to_database(app.config['DATABASE_NAME'])
    return app


twitterapp = create_flask_app()


@twitterapp.route('/profile/<int:user_id>', methods=['GET'])
def twitter_profile(user_id):
    try:
        user = TwitterUser.objects.get(_id=user_id)
    except DoesNotExist:
        store_twitter_user.delay(user_id)
        response = jsonify(message="Processing request")
        status = 202
        headers = {"Content-Type": "application/json; charset=utf-8"}
        return response, status, headers
    else:
        response = jsonify({"name": user.name,
                            "id": user.id,
                            "description": user.description,
                            "image_url": user.image_url,
                            "popularity": user.popularity})
        status = 200
        headers = {"Content-Type": "application/json; charset=utf-8"}
        return response, status, headers


if __name__ == '__main__':
    twitterapp.run()
