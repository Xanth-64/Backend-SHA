# -*- coding: utf-8 -*-
"""Test case suite for the User model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestUserModel:
    """Test suite for the User model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the user model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "User" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the user model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["User"]
        assert hasattr(model, "id")
        assert hasattr(model, "email")
        assert hasattr(model, "first_name")
        assert hasattr(model, "last_name")
        assert hasattr(model, "image_url")
        assert hasattr(model, "vark_completed")
        assert hasattr(model, "created_at")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the user model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["User"]
        assert hasattr(model, "role")
        assert hasattr(model, "learning_style")
        assert hasattr(model, "test_attempts")
        assert hasattr(model, "interactions_fired")

    def test_model_has_correct_attribute_types(self, mock_user: Model):
        """Test case to assert that the user model has the correct attribute types

        Args:
            mock_user (Model): Mock User
        """
        assert isinstance(mock_user.id, uuid.UUID)
        assert isinstance(mock_user.email, str)
        assert isinstance(mock_user.first_name, str)
        assert isinstance(mock_user.last_name, str)
        assert isinstance(mock_user.image_url, str)
        assert isinstance(mock_user.vark_completed, bool)
        assert isinstance(mock_user.created_at, datetime)

    def test_model_has_correct_relationship_types(self, mock_user: Model):
        """Test case to assert that the user model has the correct relationship types

        Args:
            mock_user (Model): Mock User
        """
        assert isinstance(mock_user.role, list)
        assert isinstance(mock_user.learning_style, object)
        assert isinstance(mock_user.test_attempts, list)
        assert isinstance(mock_user.interactions_fired.all(), list)
