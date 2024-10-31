from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    gardens = db.relationship('Garden', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    category = db.Column(db.String(50))
    attributes = db.Column(db.String(200))
    gardens = db.relationship('Garden', secondary='garden_plants')

class Garden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    plants = db.relationship('Plant', secondary='garden_plants')

# Association table for Garden-Plant many-to-many relationship
garden_plants = db.Table('garden_plants',
    db.Column('garden_id', db.Integer, db.ForeignKey('garden.id')),
    db.Column('plant_id', db.Integer, db.ForeignKey('plant.id'))
)