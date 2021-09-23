from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db:"SQLAlchemy" = SQLAlchemy()

class AgentChangePasswordOtp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contactnumber = db.Column(db.String(100))
    otp = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now())