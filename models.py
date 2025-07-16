# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TicketRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    fixture_url = db.Column(db.String(500))
    blocks = db.Column(db.String(100))
    prices = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    headless = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
