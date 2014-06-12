from flask import Flask
from flask.ext.mongoengine import MongoEngine

from werkzeug.contrib.cache import MemcachedCache


app = Flask(__name__)

app.config.from_object('settings')

cache = MemcachedCache(['127.0.0.1:11211'])

db = MongoEngine()


import models
import views
