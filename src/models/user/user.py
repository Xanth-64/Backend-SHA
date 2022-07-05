# -*- coding: utf-8 -*-
"""Module Containing the User Entity Model

This module contains the Model Definition for the Entity Representing a User in the Database

Typical usage example:

    ...
    import src.models.user import user

    {
        ### Other Model Definitions
        'User' : user.create_model(db)
    }
"""

import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID


def create_model(db: SQLAlchemy):
    class User(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        email = db.Column(db.String(255), nullable=False,unique=True)
        first_name = db.Column(db.String(255), nullable=True)
        last_name = db.Column(db.String(255), nullable=True)
        image_url = db.Column(db.String(255), nullable=True)

        pages = db.relationship(
            "Role",
            backref="user",
            lazy=True,
            uselist=True,
            cascade="all, delete-orphan",
        )
    return User
