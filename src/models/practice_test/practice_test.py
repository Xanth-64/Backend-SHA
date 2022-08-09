# -*- coding: utf-8 -*-
"""Module Containing the Practice Test Entity Model

This module contains the Model Definition for the Entity Representing a Practice Test
in the Database

Typical usage example:

    ...
    import src.models.practice_test import practice_test

    {
        ### Other Model Definitions
        'PracticeTest' : practice_test.create_model(db)
    }
"""

import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID


def create_model(db: SQLAlchemy):
    class PracticeTest(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        title = db.Column(db.String(255), unique=True, nullable=False)
        show_on_init = db.Column(db.Boolean, default=False)

        page_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("page.id"), nullable=False
        )

        test_questions = db.relationship(
            "TestQuestion",
            backref="practice_test",
            lazy=True,
            uselist=True,
            cascade="all, delete-orphan",
        )

    return PracticeTest
