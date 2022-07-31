# -*- coding: utf-8 -*-
"""Module Containing the Topic Entity Model

This module contains the Model Definition for the Entity Representing a Topic in the Database

Typical usage example:

    ...
    import src.models.topic import topic

    {
        ### Other Model Definitions
        'Topic' : topic.create_model(db)
    }
"""
import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

from src.models.many_to_many import topic_precedence


def create_model(db: SQLAlchemy):
    secondary_table = topic_precedence.get_helper_table(db)

    class Topic(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        relative_position = db.Column(db.Integer(), nullable=False, unique=True)

        title = db.Column(db.String(255), unique=True, nullable=False)
        icon_name = db.Column(db.String(255), nullable=True)
        default_knowledge = db.Column(db.Integer(), default=50)

        successors = db.relationship(
            "Topic",
            secondary=secondary_table,
            foreign_keys=[secondary_table.c.predecessor],
            lazy=True,
            backref=db.backref("predecessors", lazy=True),
        )

    return Topic
