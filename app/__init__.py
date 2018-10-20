from flask import Flask
from instance.config import app_config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config["development"])

from app.account import views
from app.product import views
from app.register import views
from app.sale import views
