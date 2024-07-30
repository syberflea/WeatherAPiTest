from flask import Flask
from weather import pages
# from models import db
# from routes import main

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)

# with app.app_context():
#     db.create_all()


def create_app():
    app = Flask(__name__)
    app.register_blueprint(pages.bp)

    return app
