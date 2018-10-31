import datetime
from app.api.v1 import app
from app.api.v1.database import DatabaseConnection


db = DatabaseConnection()


if __name__ == "__main__":
    app.run()
    db.create_tables()
    db.default_admin_setup("store_owner", "admin@gmail.com", "admin00", "admin", datetime.datetime.utcnow(),
                           datetime.datetime.utcnow())
