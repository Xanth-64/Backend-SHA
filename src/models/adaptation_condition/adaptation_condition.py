# -*- coding: utf-8 -*-
"""Module Containing the Adaptation Condition Entity Model

This module contains the Model Definition for the Entity Representing a Adaptation Condition
in the Database

Typical usage example:

    ...
    import src.models.adaptation_condition import adaptation_condition

    {
        ### Other Model Definitions
        'AdaptationCondition' : adaptation_condition.create_model(db)
    }
"""

import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ENUM, UUID


def create_model(db: SQLAlchemy):
    class AdaptationCondition(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        value_to_compare = db.Column(db.Integer, nullable=False)
        comparation_condition = db.Column(
            ENUM("lte", "gte", name="comparation_condition_enum"),
        )
        variable_to_compare = db.Column(
            ENUM(
                "TOPIC_KNOWLEDGE",
                "TEMPLATE_KNOWLEDGE",
                "LEARNING_STYLE_AURAL_AFFINITY",
                "LEARNING_STYLE_VISUAL_AFFINITY",
                "LEARNING_STYLE_READING_AFFINITY",
                "LEARNING_STYLE_KINESTHETIC_AFFINITY",
                name="variable_to_compare_enum",
            ),
            nullable=False,
        )
        adaptative_event_id = db.Column(
            UUID(as_uuid=True),
            db.ForeignKey("adaptative_event.id"),
            nullable=False,
        )

    return AdaptationCondition
