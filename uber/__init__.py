from flask import Flask

from werkzeug.contrib.cache import MemcachedCache


app = Flask(__name__)

app.config.from_object('settings')

cache = MemcachedCache(['127.0.0.1:11211'])


import models
import views
