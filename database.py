from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100))
    ingredients = db.Column(db.Text, nullable=False)
    health_score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
