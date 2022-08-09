# -*- coding: utf-8 -*-
"""Module Containing the Template Entity Model

This module contains the Model Definition for the Entity Representing a Template in the Database

Typical usage example:

    ...
    import src.models.template import template

    {
        ### Other Model Definitions
        'Template' : template.create_model(db)
    }
"""

import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID


def create_model(db: SQLAlchemy):
    class Template(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        relative_position = db.Column(db.Integer(), nullable=False)

        title = db.Column(db.String(255), unique=True, nullable=False)
        description = db.Column(db.Text(), nullable=True)
        image_url = db.Column(db.String(255), nullable=True)

        default_knowledge = db.Column(db.Integer(), nullable=False, default=100)

        knowledge_weight = db.Column(db.Integer(), nullable=False, default=100)

        topic_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("topic.id"), nullable=False
        )

        pages = db.relationship(
            "Page",
            backref="template",
            lazy=True,
            uselist=True,
            cascade="all, delete-orphan",
        )

        UniqueConstraint(relative_position, topic_id, name="unique_template_position")

    return Template
