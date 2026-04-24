import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from eralchemy2 import render_er

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(50), nullable=False, unique=True)
    firstname = Column(db.String(50), nullable=False)
    lastname = Column(db.String(50), nullable=False)
    email = Column(db.String(120), unique=True, nullable=False)
    password = Column(db.String(80), nullable=False)
    subscription_date = Column(db.DateTime, default=datetime.utcnow)

    favorites = db.relationship('Favorite', back_populates='user')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname

        }

    def __repr__(self):
        return self.username


class Character(db.Model):
    __tablename__ = 'character'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(100), nullable=False)
    birth_year = Column(db.String(20))
    gender = Column(db.String(20))
    height = Column(db.String(20))
    skin_color = Column(db.String(20))
    eye_color = Column(db.String(20))

    favorites = db.relationship('Favorite', back_populates='character')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "eye_color": self.eye_color
        }

    def __repr__(self):
        return self.name


class Planet(db.Model):
    __tablename__ = 'planet'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(100), nullable=False)
    climate = Column(db.String(50))
    terrain = Column(db.String(50))
    population = Column(db.String(50))
    diameter = Column(db.String(50))

    favorites = db.relationship('Favorite', back_populates='planet')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(
        db.Integer, db.ForeignKey('character.id'), nullable=True)
    planet_id = db.Column(
        db.Integer, db.ForeignKey('planet.id'), nullable=True)

    user = db.relationship('User', back_populates='favorites')
    character = db.relationship('Character', back_populates='favorites')
    planet = db.relationship('Planet', back_populates='favorites')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "character_name": self.character.name if self.character else None,
            "planet_name": self.planet.name if self.planet else None
        }

    def __repr__(self):
        return f'<Favorite {self.id}>'


try:
    result = render_er(db, 'diagram.png')
    print("¡Éxito! El archivo diagram.png ha sido generado.")
except Exception as e:
    print("Hubo un error al generar el diagrama:", e)

    # try/except
