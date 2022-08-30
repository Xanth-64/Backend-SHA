# -*- coding: utf-8 -*-
"""Module Containing the Answer Alternative Entity Model

This module contains the Model Definition for the Entity Representing a Answer Alternative
in the Database

Typical usage example:

    ...
    import src.models.answer_alternative import answer_alternative

    {
        ### Other Model Definitions
        'AnswerAlternative' : answer_alternative.create_model(db)
    }
"""

import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID


def create_model(db: SQLAlchemy):
    class AnswerAlternative(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        alternative_text = db.Column(db.String(255), nullable=False)
        is_correct = db.Column(db.Boolean, default=False)
        test_question_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("test_question.id"), nullable=False
        )
        selected_answer_alternatives = db.relationship(
            "SelectedAnswerAlternative",
            backref="answer_alternative",
            lazy="dynamic",
            cascade="all, delete-orphan",
        )
        UniqueConstraint(
            alternative_text, test_question_id, name="unique_question_options"
        )

        def __repr__(self):
            return f"{self.alternative_text} : {self.is_correct}"

    return AnswerAlternative
