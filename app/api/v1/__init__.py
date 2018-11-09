from flask import Flask
from flask_cors import CORS
from instance.config import app_config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config["development"])
CORS(app)

from app.api.v1 import product, register, sale, account
