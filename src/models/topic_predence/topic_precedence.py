# -*- coding: utf-8 -*-
"""Module Containing the Topic Precedence Helper Table

This module contains the Helper Table Definition for the Relation of Topic Precedence
in the Database

Typical usage example:

    ...
    import src.models.many_to_many import topic_precedence

    class Model:
        ### Other Model Params
        relationship = db.relationship('relationship_name',
        secondary=topic_precedence.get_helper_table(db),
        lazy=True,backref=db.backref('relationship_backname', lazy=True))
"""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import UUID
import uuid


def create_model(db: SQLAlchemy):
    class TopicPrecedence(db.Model):
        __tablename__ = "topic_precedence"
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        knowledge_weight = db.Column(db.Integer(), nullable=False, default=50)

        predecessor_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("topic.id"), nullable=False
        )
        successor_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("topic.id"), nullable=False
        )

        predecessor = db.relationship(
            "Topic",
            back_populates="successors",
            lazy=True,
            uselist=False,
            foreign_keys=[predecessor_id],
        )
        successor = db.relationship(
            "Topic",
            back_populates="predecessors",
            lazy=True,
            uselist=False,
            foreign_keys=[successor_id],
        )

    return TopicPrecedence
