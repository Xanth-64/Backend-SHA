# -*- coding: utf-8 -*-
"""Test case suite for the Learning Content model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestLearningContentModel:
    """Test suite for the Learning Content model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Learning Content model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "LearningContent" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Learning Content model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["LearningContent"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "title")
        assert hasattr(model, "content")
        assert hasattr(model, "page_id")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Learning Content model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["LearningContent"]
        assert hasattr(model, "measurable_interactions")

    def test_model_has_correct_attribute_types(self, mock_learning_content: Model):
        """Test case to assert that the Learning Content model has the correct attribute types

        Args:
            mock_learning_content (Model): Mock Learning Content
        """
        assert isinstance(mock_learning_content.id, uuid.UUID)
        assert isinstance(mock_learning_content.created_at, datetime)
        assert isinstance(mock_learning_content.title, str)
        assert isinstance(mock_learning_content.content, str)
        assert isinstance(mock_learning_content.page_id, uuid.UUID)

    def test_model_has_correct_relationship_types(self, mock_learning_content: Model):
        """Test case to assert that the Learning Content model has the correct
        relationship types

        Args:
            mock_learning_content (Model): Mock Learning Content
        """
        assert isinstance(mock_learning_content.measurable_interactions.all(), list)
        assert isinstance(mock_learning_content.page, Model)
