from flask.ext.mongoengine import MongoEngine

from werkzeug.contrib.cache import MemcachedCache

import factory


cache = MemcachedCache(['127.0.0.1:11211'])


db = MongoEngine()


def create_app(settings_override=None):
    from emailer import app as emailer

    app = factory.create_app(__name__, settings_override=settings_override)

    app.register_blueprint(emailer)

    return app


import models
import views
