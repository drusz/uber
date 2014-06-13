from flask.ext.mongoengine import MongoEngine
from werkzeug.contrib.cache import MemcachedCache

cache = MemcachedCache(['127.0.0.1:11211'])

db = MongoEngine()
