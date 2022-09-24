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
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from src.models.topic_predence import topic_precedence


def create_model(db: SQLAlchemy):
    class Topic(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        relative_position = db.Column(db.Integer(), nullable=False)
        db.UniqueConstraint(relative_position, deferrable=True, initially="DEFERRED")

        title = db.Column(db.String(255), unique=True, nullable=False)
        icon_name = db.Column(db.String(255), nullable=True)
        default_knowledge = db.Column(db.Integer(), default=50)
        leak_parameter = db.Column(db.Float(), default=0.0)

        successors = db.relationship(
            "TopicPrecedence",
            back_populates="predecessor",
            primaryjoin="TopicPrecedence.predecessor_id == Topic.id",
        )

        predecessors = db.relationship(
            "TopicPrecedence",
            back_populates="successor",
            primaryjoin="TopicPrecedence.successor_id == Topic.id",
        )

        adaptative_object_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("adaptative_object.id"), nullable=False
        )

        templates = db.relationship(
            "Template",
            backref="topic",
            lazy="dynamic",
            uselist=True,
            cascade="all, delete-orphan",
        )

    return Topic
