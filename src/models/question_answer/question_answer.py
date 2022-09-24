# -*- coding: utf-8 -*-
"""Module Containing the Question Answer Entity Model

This module contains the Model Definition for the Entity Representing a Question Answer in the Database

Typical usage example:

    ...
    import src.models.question_answer import question_answer

    {
        ### Other Model Definitions
        'QuestionAnswer' : question_answer.create_model(db)
    }
"""

import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID


def create_model(db: SQLAlchemy):
    class QuestionAnswer(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        acquired_score = db.Column(db.Integer, nullable=False)
        is_correct = db.Column(db.Boolean, nullable=False)

        test_attempt_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("test_attempt.id"), nullable=False
        )
        test_question_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("test_question.id"), nullable=True
        )
        selected_answer_alternatives = db.relationship(
            "SelectedAnswerAlternative",
            backref="question_answer",
            lazy="dynamic",
            cascade="all, delete-orphan",
        )
        UniqueConstraint(
            test_attempt_id,
            test_question_id,
            name="unique_question_answer",
            deferrable=True,
            initially="DEFERRED",
        )

    return QuestionAnswer
