# -*- coding: utf-8 -*-
"""Test case suite for the Adaptative Object model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestAdaptativeObjectModel:
    """Test suite for the Adaptative Object model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Adaptative Object model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "AdaptativeObject" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Adaptative Object model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["AdaptativeObject"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Adaptative Object model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["AdaptativeObject"]
        assert hasattr(model, "topic")
        assert hasattr(model, "template")
        assert hasattr(model, "page")
        assert hasattr(model, "test_question")
        assert hasattr(model, "adaptative_events")

    def test_model_has_correct_attribute_types(self, mock_adaptative_object: Model):
        """Test case to assert that the Adaptative Object model has the correct attribute types

        Args:
            mock_adaptative_object (Model): Mock Adaptative Object
        """
        assert isinstance(mock_adaptative_object.id, uuid.UUID)
        assert isinstance(mock_adaptative_object.created_at, datetime)

    def test_model_has_correct_relationship_types(self, mock_adaptative_object: Model):
        """Test case to assert that the Adaptative Object model has the correct
        relationship types

        Args:
            mock_adaptative_object (Model): Mock Adaptative Object
        """
        assert isinstance(mock_adaptative_object.topic, object)
        assert isinstance(mock_adaptative_object.template, object)
        assert isinstance(mock_adaptative_object.page, object)
        assert isinstance(mock_adaptative_object.test_question, object)
        assert isinstance(mock_adaptative_object.adaptative_events.all(), list)
