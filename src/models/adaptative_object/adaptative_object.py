# -*- coding: utf-8 -*-
"""Module Containing the Adaptative Object Entity Model

This module contains the Model Definition for the Entity Representing a Adaptative Object
in the Database

Typical usage example:

    ...
    import src.models.adaptative_object import adaptative_object

    {
        ### Other Model Definitions
        'AdaptativeObject' : adaptative_object.create_model(db)
    }
"""

import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID


def create_model(db: SQLAlchemy):
    class AdaptativeObject(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        topic = db.relationship(
            "Topic",
            backref="adaptative_object",
            lazy=True,
            uselist=False,
            cascade="all, delete-orphan",
        )
        template = db.relationship(
            "Template",
            backref="adaptative_object",
            lazy=True,
            uselist=False,
            cascade="all, delete-orphan",
        )
        page = db.relationship(
            "Page",
            backref="adaptative_object",
            lazy=True,
            uselist=False,
            cascade="all, delete-orphan",
        )
        test_question = db.relationship(
            "TestQuestion",
            backref="adaptative_object",
            lazy=True,
            uselist=False,
            cascade="all, delete-orphan",
        )
        adaptative_events = db.relationship(
            "AdaptativeEvent",
            backref="adaptative_object",
            lazy="dynamic",
            uselist=True,
            cascade="all, delete-orphan",
        )

    return AdaptativeObject
