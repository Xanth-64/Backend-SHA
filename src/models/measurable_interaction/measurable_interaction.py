# -*- coding: utf-8 -*-
"""Module Containing the Measurable Interaction Entity Model

This module contains the Model Definition for the Entity Representing a Measurable Interaction in the Database

Typical usage example:

    ...
    import src.models.measurable_interaction import measurable_interaction

    {
        ### Other Model Definitions
        'MeasurableInteraction' : measurable_interaction.create_model(db)
    }
"""
import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ENUM, UUID


def create_model(db: SQLAlchemy):
    class MeasurableInteraction(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        interaction_weight = db.Column(db.Integer(), nullable=False, default=1)
        interaction_threshold = db.Column(db.Integer(), nullable=False, default=1)
        interaction_trigger = db.Column(
            ENUM("click", "observe", "idle_observe", name="interaction_trigger_enum"),
            nullable=False,
        )
        learning_style_attribute = db.Column(
            ENUM(
                "VISUAL",
                "AURAL",
                "KINESTHETIC",
                "TEXTUAL",
                name="learning_style_attribute_enum",
            ),
            nullable=True,
        )

        learning_content_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("learning_content.id"), nullable=False
        )
        interactions_fired = db.relationship(
            "InteractionFired",
            backref="measurable_interaction",
            lazy="dynamic",
            uselist=True,
            cascade="all, delete-orphan",
        )

    return MeasurableInteraction
