# -*- coding: utf-8 -*-
"""Module Containing the Page Entity Model

This module contains the Model Definition for the Entity Representing a Page in the Database

Typical usage example:

    ...
    import src.models.page import page

    {
        ### Other Model Definitions
        'Page' : page.create_model(db)
    }
"""
import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID


def create_model(db: SQLAlchemy):
    class Page(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        relative_position = db.Column(db.Integer(), nullable=False)

        template_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("template.id"), nullable=False
        )

        practice_test = db.relationship(
            "PracticeTest",
            backref="page",
            lazy=True,
            uselist=False,
            cascade="all, delete-orphan",
        )

        learning_content = db.relationship(
            "LearningContent",
            backref="page",
            lazy=True,
            uselist=False,
            cascade="all, delete-orphan",
        )

        adaptative_object_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("adaptative_object.id"), nullable=False
        )

        UniqueConstraint(
            relative_position,
            template_id,
            name="unique_page_position",
            deferrable=True,
            initially="DEFERRED",
        )

    return Page
