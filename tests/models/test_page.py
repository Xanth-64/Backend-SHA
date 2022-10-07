# -*- coding: utf-8 -*-
"""Test case suite for the Page model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestPageModel:
    """Test suite for the Page model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Page model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "Page" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Page model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["Page"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "relative_position")
        assert hasattr(model, "template_id")
        assert hasattr(model, "adaptative_object_id")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Page model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["Page"]
        assert hasattr(model, "learning_content")
        assert hasattr(model, "practice_test")

    def test_model_has_correct_attribute_types(self, mock_page: Model):
        """Test case to assert that the Page model has the correct attribute types

        Args:
            mock_page (Model): Mock Page
        """
        assert isinstance(mock_page.id, uuid.UUID)
        assert isinstance(mock_page.created_at, datetime)
        assert isinstance(mock_page.relative_position, int)
        assert isinstance(mock_page.template_id, uuid.UUID)
        assert isinstance(mock_page.adaptative_object_id, uuid.UUID)

    def test_model_has_correct_relationship_types(self, mock_page: Model):
        """Test case to assert that the Page model has the correct
        relationship types

        Args:
            mock_page (Model): Mock Page
        """
        assert isinstance(mock_page.learning_content, (Model, type(None)))
        assert isinstance(mock_page.practice_test, (Model, type(None)))
        assert isinstance(mock_page.template, Model)
        assert isinstance(mock_page.adaptative_object, Model)
