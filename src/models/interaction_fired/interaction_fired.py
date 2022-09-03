# -*- coding: utf-8 -*-
"""Module Containing the Interaction Fired Entity Model

This module contains the Model Definition for the Entity Representing a Interaction Fired in the Database

Typical usage example:

    ...
    import src.models.interaction_fired import interaction_fired

    {
        ### Other Model Definitions
        'InteractionFired' : interaction_fired.create_model(db)
    }
"""

import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID


def create_model(db: SQLAlchemy):
    class InteractionFired(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        user_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False
        )
        measurable_interaction_id = db.Column(
            UUID(as_uuid=True),
            db.ForeignKey("measurable_interaction.id"),
            nullable=False,
        )

        UniqueConstraint(
            user_id,
            measurable_interaction_id,
            name="unique_interaction_fired",
            deferrable=True,
            initially="DEFERRED",
        )

    return InteractionFired
