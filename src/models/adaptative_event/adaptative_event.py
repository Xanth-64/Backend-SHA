# -*- coding: utf-8 -*-
"""Module Containing the Adaptative Event Entity Model

This module contains the Model Definition for the Entity Representing a Adaptative Event
in the Database

Typical usage example:

    ...
    import src.models.adaptative_event import adaptative_event

    {
        ### Other Model Definitions
        'AdaptativeEvent' : adaptative_event.create_model(db)
    }
"""

import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy import UniqueConstraint


def create_model(db: SQLAlchemy):
    class AdaptativeEvent(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        triggered_change = db.Column(
            ENUM(
                "HIGHLIGHT",
                "OBSCURE",
                "DISABLE",
                "HIDE",
                "NOTIFY_POSITIVE",
                "NOTIFY_NEGATIVE",
                "DISPLAY_HINT",
                "REDUCE_ALTERNATIVES",
                name="triggered_change_enum",
            ),
            nullable=False,
        )
        relative_position = db.Column(db.Integer, nullable=False)
        condition_aggregator = db.Column(
            ENUM("AND", "OR", name="condition_aggregator_enum"), nullable=True
        )
        adaptative_object_id = db.Column(
            UUID(as_uuid=True),
            db.ForeignKey("adaptative_object.id"),
            nullable=False,
        )
        adaptation_conditions = db.relationship(
            "AdaptationCondition",
            backref="adaptative_event",
            lazy="dynamic",
            cascade="all, delete-orphan",
            uselist=True,
        )
        UniqueConstraint(
            relative_position,
            adaptative_object_id,
            name="unique_adaptative_event_position",
            deferrable=True,
            initially="DEFERRED",
        )

    return AdaptativeEvent
