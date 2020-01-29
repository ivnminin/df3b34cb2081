from datetime import datetime

from app import app, db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer(), primary_key=True)
    function = db.Column(db.String(100), nullable=False)
    interval = db.Column(db.Integer(), nullable=False)
    step = db.Column(db.Integer(), nullable=False)

    image_hash = db.Column(db.String(255))
    image_data = db.Column(db.LargeBinary)

    error = db.Column(db.Boolean, default=False)
    error_msg = db.Column(db.String())

    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)
