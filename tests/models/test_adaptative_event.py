# -*- coding: utf-8 -*-
"""Test case suite for the Adaptative Event model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestAdaptativeEventModel:
    """Test suite for the Adaptative Event model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Adaptative Event model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "AdaptativeEvent" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Adaptative Event model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["AdaptativeEvent"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "triggered_change")
        assert hasattr(model, "relative_position")
        assert hasattr(model, "condition_aggregator")
        assert hasattr(model, "adaptative_object_id")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Adaptative Event model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["AdaptativeEvent"]
        assert hasattr(model, "adaptation_conditions")

    def test_model_has_correct_attribute_types(self, mock_adaptative_event: Model):
        """Test case to assert that the Adaptative Event model has the correct attribute types

        Args:
            mock_adaptative_event (Model): Mock Adaptative Event
        """
        assert isinstance(mock_adaptative_event.id, uuid.UUID)
        assert isinstance(mock_adaptative_event.created_at, datetime)
        assert isinstance(mock_adaptative_event.triggered_change, str)
        assert isinstance(mock_adaptative_event.relative_position, int)
        assert isinstance(mock_adaptative_event.condition_aggregator, str)
        assert isinstance(mock_adaptative_event.adaptative_object_id, uuid.UUID)

    def test_model_has_correct_relationship_types(self, mock_adaptative_event: Model):
        """Test case to assert that the Adaptative Event model has the correct
        relationship types

        Args:
            mock_adaptative_event (Model): Mock Adaptative Event
        """
        assert isinstance(mock_adaptative_event.adaptation_conditions.all(), list)
        assert isinstance(mock_adaptative_event.adaptative_object, object)
