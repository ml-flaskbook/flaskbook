import os

from flask import Flask

from flaskbook_api.api import api

app = Flask(__name__)
app.config.from_envvar("APPLICATION_SETTINGS")
# blueprintをアプリケーションに登録
app.register_blueprint(api)