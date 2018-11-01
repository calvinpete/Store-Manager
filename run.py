import datetime
from app.api.v1 import app
from app.api.v1.database import DatabaseConnection
from werkzeug.security import generate_password_hash


db = DatabaseConnection()


if __name__ == "__main__":
    app.run()
    db.create_tables()
    db.default_admin_setup("store_owner", "admin@gmail.com", generate_password_hash("admin00"), "admin",
                           datetime.datetime.utcnow(), datetime.datetime.utcnow())
