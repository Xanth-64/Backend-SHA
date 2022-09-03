# -*- coding: utf-8 -*-
"""Module Containing the Selected Answer Alternative Entity Model

This module contains the Model Definition for the Entity Representing a Selected Answer Alternative in the Database

Typical usage example:

    ...
    import src.models.selected_answer_alternative import selected_answer_alternative

    {
        ### Other Model Definitions
        'SelectedAnswerAlternative' : selected_answer_alternative.create_model(db)
    }
"""

import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID


def create_model(db: SQLAlchemy):
    class SelectedAnswerAlternative(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        question_answer_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("question_answer.id"), nullable=False
        )
        answer_alternative_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("answer_alternative.id"), nullable=False
        )

        UniqueConstraint(
            question_answer_id,
            answer_alternative_id,
            name="unique_selected_answer_alternative",
            deferrable=True,
            initially="DEFERRED",
        )

    return SelectedAnswerAlternative
