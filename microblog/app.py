from flask import Flask
from flask.ext.cache import Cache
import os

SECRET_KEY = os.urandom(24)

app = Flask(__name__)
app.config.from_object(__name__)
cache = Cache(app)
