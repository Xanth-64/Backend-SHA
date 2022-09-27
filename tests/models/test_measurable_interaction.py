# -*- coding: utf-8 -*-
"""Test case suite for the Measurable Interaction model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestMeasurableInteractionModel:
    """Test suite for the Measurable Interaction model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Measurable Interaction model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "MeasurableInteraction" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Measurable Interaction model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["MeasurableInteraction"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "interaction_weight")
        assert hasattr(model, "interaction_threshold")
        assert hasattr(model, "interaction_trigger")
        assert hasattr(model, "learning_style_attribute")
        assert hasattr(model, "learning_content_id")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Measurable Interaction model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["MeasurableInteraction"]
        assert hasattr(model, "interactions_fired")

    def test_model_has_correct_attribute_types(
        self, mock_measurable_interaction: Model
    ):
        """Test case to assert that the Measurable Interaction model has the correct attribute types

        Args:
            mock_measurable_interaction (Model): Mock MeasurableInteraction
        """
        assert isinstance(mock_measurable_interaction.id, uuid.UUID)
        assert isinstance(mock_measurable_interaction.created_at, datetime)
        assert isinstance(mock_measurable_interaction.interaction_weight, int)
        assert isinstance(mock_measurable_interaction.interaction_threshold, int)
        assert isinstance(mock_measurable_interaction.interaction_trigger, str)
        assert isinstance(mock_measurable_interaction.learning_style_attribute, str)
        assert isinstance(mock_measurable_interaction.learning_content_id, uuid.UUID)

    def test_model_has_correct_relationship_types(
        self, mock_measurable_interaction: Model
    ):
        """Test case to assert that the Measurable Interaction model has the correct
        relationship types

        Args:
            mock_measurable_interaction (Model): Mock MeasurableInteraction
        """
        assert isinstance(mock_measurable_interaction.learning_content, Model)
        assert isinstance(mock_measurable_interaction.interactions_fired.all(), list)
