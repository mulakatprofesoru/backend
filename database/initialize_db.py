from database.models import db
from database import createApp


def createDB():
    app = createApp()

    with app.app_context():
        db.create_all()