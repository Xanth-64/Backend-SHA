# -*- coding: utf-8 -*-
"""Test case suite for the Topic model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestTopicModel:
    """Test suite for the Topic model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Topic model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "Topic" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Topic model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["Topic"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "relative_position")
        assert hasattr(model, "title")
        assert hasattr(model, "icon_name")
        assert hasattr(model, "default_knowledge")
        assert hasattr(model, "leak_parameter")
        assert hasattr(model, "adaptative_object_id")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Topic model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["Topic"]
        assert hasattr(model, "successors")
        assert hasattr(model, "predecessors")
        assert hasattr(model, "templates")

    def test_model_has_correct_attribute_types(self, mock_topic: Model):
        """Test case to assert that the Topic model has the correct attribute types

        Args:
            mock_topic (Model): Mock Topic
        """
        assert isinstance(mock_topic.id, uuid.UUID)
        assert isinstance(mock_topic.created_at, datetime)
        assert isinstance(mock_topic.relative_position, int)
        assert isinstance(mock_topic.title, str)
        assert isinstance(mock_topic.icon_name, str)
        assert isinstance(mock_topic.default_knowledge, int)
        assert isinstance(mock_topic.leak_parameter, float)
        assert isinstance(mock_topic.adaptative_object_id, uuid.UUID)

    def test_model_has_correct_relationship_types(self, mock_topic: Model):
        """Test case to assert that the Topic model has the correct
        relationship types

        Args:
            mock_topic (Model): Mock Topic
        """
        assert isinstance(mock_topic.successors, list)
        assert isinstance(mock_topic.predecessors, list)
        assert isinstance(mock_topic.templates.all(), list)
