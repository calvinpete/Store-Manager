from flask import Flask
from instance.config import app_config


app = Flask(__name__)
app.config.from_object(app_config["development"])
