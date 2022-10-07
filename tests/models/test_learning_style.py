# -*- coding: utf-8 -*-
"""Test case suite for the Learning Style model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestLearningStyleModel:
    """Test suite for the Learning Style model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Learning Style model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "LearningStyle" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Learning Style model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["LearningStyle"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "visual")
        assert hasattr(model, "aural")
        assert hasattr(model, "kinesthetic")
        assert hasattr(model, "textual")
        assert hasattr(model, "user_id")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Learning Style model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["LearningStyle"]

    def test_model_has_correct_attribute_types(self, mock_learning_style: Model):
        """Test case to assert that the Learning Style model has the correct attribute types

        Args:
            mock_learning_style (Model): Mock LearningStyle
        """
        assert isinstance(mock_learning_style.id, uuid.UUID)
        assert isinstance(mock_learning_style.created_at, datetime)
        assert isinstance(mock_learning_style.visual, int)
        assert isinstance(mock_learning_style.aural, int)
        assert isinstance(mock_learning_style.kinesthetic, int)
        assert isinstance(mock_learning_style.textual, int)
        assert isinstance(mock_learning_style.user_id, uuid.UUID)

    def test_model_has_correct_relationship_types(self, mock_learning_style: Model):
        """Test case to assert that the Learning Style model has the correct
        relationship types

        Args:
            mock_learning_style (Model): Mock LearningStyle
        """
        assert isinstance(mock_learning_style.user, object)
