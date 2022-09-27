# -*- coding: utf-8 -*-
"""Test case suite for the Adaptation Condition model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestAdaptationConditionModel:
    """Test suite for the Adaptation Condition model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the adaptation condition model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "AdaptationCondition" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the adaptation condition model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["AdaptationCondition"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "value_to_compare")
        assert hasattr(model, "comparation_condition")
        assert hasattr(model, "variable_to_compare")
        assert hasattr(model, "adaptative_event_id")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the adaptation condition model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["AdaptationCondition"]

    def test_model_has_correct_attribute_types(self, mock_adaptation_condition: Model):
        """Test case to assert that the adaptation condition model has the correct attribute types

        Args:
            mock_adaptation_condition (Model): Mock Adaptation Condition
        """
        assert isinstance(mock_adaptation_condition.id, uuid.UUID)
        assert isinstance(mock_adaptation_condition.created_at, datetime)
        assert isinstance(mock_adaptation_condition.value_to_compare, int)
        assert isinstance(mock_adaptation_condition.comparation_condition, str)
        assert isinstance(mock_adaptation_condition.variable_to_compare, str)
        assert isinstance(mock_adaptation_condition.adaptative_event_id, uuid.UUID)

    def test_model_has_correct_relationship_types(
        self, mock_adaptation_condition: Model
    ):
        """Test case to assert that the adaptation condition model has the correct
        relationship types

        Args:
            mock_adaptation_condition (Model): Mock Adaptation Condition
        """
        assert isinstance(mock_adaptation_condition.adaptative_event, object)
