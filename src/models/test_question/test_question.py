# -*- coding: utf-8 -*-
"""Module Containing the Test Question Entity Model

This module contains the Model Definition for the Entity Representing a Test Question
in the Database

Typical usage example:

    ...
    import src.models.test_question import test_question

    {
        ### Other Model Definitions
        'TestQuestion' : test_question.create_model(db)
    }
"""


import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, UUID


def create_model(db: SQLAlchemy):
    class TestQuestion(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        question_type = db.Column(
            ENUM("multiple_selection", "simple_selection", name="question_type_enum"),
            default="simple_selection",
        )
        question_prompt = db.Column(db.Text(), nullable=False)
        relative_position = db.Column(db.Integer(), nullable=False)
        question_score = db.Column(db.Integer(), default=1)
        practice_test_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("practice_test.id"), nullable=False
        )
        question_hint = db.Column(db.String(255), default="")

        answer_alternatives = db.relationship(
            "AnswerAlternative",
            backref="test_question",
            lazy="dynamic",
            uselist=True,
            cascade="all, delete-orphan",
        )
        question_answers = db.relationship(
            "QuestionAnswer",
            backref="test_question",
            lazy="dynamic",
            uselist=True,
            cascade="all, delete-orphan",
        )

        adaptative_object_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("adaptative_object.id"), nullable=False
        )

        UniqueConstraint(
            relative_position, practice_test_id, name="unique_question_position"
        )

        def __repr__(self):
            return f"{self.relative_position} : {self.question_prompt}"

    return TestQuestion
