# -*- coding: utf-8 -*-
"""Module Containing the Test Attempt Entity Model

This module contains the Model Definition for the Entity Representing a Test Attempt in the Database

Typical usage example:

    ...
    import src.models.test_attempt import test_attempt

    {
        ### Other Model Definitions
        'TestAttempt' : test_attempt.create_model(db)
    }
"""

import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID


def create_model(db: SQLAlchemy):
    class TestAttempt(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        acquired_score = db.Column(db.Integer, nullable=False)

        user_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False
        )
        practice_test_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("practice_test.id"), nullable=False
        )
        question_answers = db.relationship(
            "QuestionAnswer",
            backref="test_attempt",
            lazy=True,
            uselist=True,
            cascade="all, delete-orphan",
        )

        UniqueConstraint(
            user_id,
            practice_test_id,
            name="unique_test_attempt",
            deferrable=True,
            initially="DEFERRED",
        )

    return TestAttempt
