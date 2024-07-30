from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    search_count = db.Column(db.Integer, default=0)
