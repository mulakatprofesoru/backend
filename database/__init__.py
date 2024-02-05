from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def createApp():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:postgres@localhost:5432/mulakatprofesorum"  # Burada postgresql kullanıcam diyorum ilk. Sonra ilk postgres username diğeri password. localhost nerede çalıştıracağım. 5432 portum. flasktutorial da veritabanı ismi.
    )

    db.init_app(app)

    return app
