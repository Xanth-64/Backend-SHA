# -*- coding: utf-8 -*-
"""Module Containing the Learning Content Entity Model

This module contains the Model Definition for the Entity Representing a Learning Content
in the Database

Typical usage example:

    ...
    import src.models.learning_content import learning_content

    {
        ### Other Model Definitions
        'LearningContent' : learning_content.create_model(db)
    }
"""

import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID


def create_model(db: SQLAlchemy):
    class LearningContent(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        title = db.Column(db.String(255), unique=True, nullable=False)
        content = db.Column(db.Text(), nullable=False)

        page_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("page.id"), nullable=False
        )

        measurable_interactions = db.relationship(
            "MeasurableInteraction",
            backref="learning_content",
            lazy="dynamic",
            uselist=True,
            cascade="all, delete-orphan",
        )

    return LearningContent
