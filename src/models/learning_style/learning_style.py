# -*- coding: utf-8 -*-
"""Module Containing the Learning Style Entity Model

This module contains the Model Definition for the Entity Representing a Learning Style
in the Database

Typical usage example:

    ...
    import src.models.learning_style import.learning_style

    {
        ### Other Model Definitions
        'Role' : learning_style.create_model(db)
    }
"""

import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID


def create_model(db: SQLAlchemy):
    class LearningStyle(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        visual = db.Column(db.Integer, default=1, nullable=False)
        aural = db.Column(db.Integer, default=1, nullable=False)
        kinesthetic = db.Column(db.Integer, default=1, nullable=False)
        textual = db.Column(db.Integer, default=1, nullable=False)

        user_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False
        )

    return LearningStyle
