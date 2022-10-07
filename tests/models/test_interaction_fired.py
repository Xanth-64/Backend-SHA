# -*- coding: utf-8 -*-
"""Test case suite for the Interaction Fired model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestInteractionFiredModel:
    """Test suite for the Interaction Fired model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Interaction Fired model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "InteractionFired" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Interaction Fired model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["InteractionFired"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "user_id")
        assert hasattr(model, "measurable_interaction_id")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Interaction Fired model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["InteractionFired"]

    def test_model_has_correct_attribute_types(self, mock_interaction_fired: Model):
        """Test case to assert that the Interaction Fired model has the correct attribute types

        Args:
            mock_interaction_fired (Model): Mock Interaction Fired
        """
        assert isinstance(mock_interaction_fired.id, uuid.UUID)
        assert isinstance(mock_interaction_fired.created_at, datetime)
        assert isinstance(mock_interaction_fired.user_id, uuid.UUID)
        assert isinstance(mock_interaction_fired.measurable_interaction_id, uuid.UUID)

    def test_model_has_correct_relationship_types(self, mock_interaction_fired: Model):
        """Test case to assert that the Interaction Fired model has the correct
        relationship types

        Args:
            mock_interaction_fired (Model): Mock Interaction Fired
        """
        assert isinstance(mock_interaction_fired.user, Model)
        assert isinstance(mock_interaction_fired.measurable_interaction, Model)
