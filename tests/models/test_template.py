# -*- coding: utf-8 -*-
"""Test case suite for the Template model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestTemplateModel:
    """Test suite for the Template model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Template model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "Template" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Template model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["Template"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "relative_position")
        assert hasattr(model, "title")
        assert hasattr(model, "description")
        assert hasattr(model, "image_url")
        assert hasattr(model, "default_knowledge")
        assert hasattr(model, "knowledge_weight")
        assert hasattr(model, "leak_parameter")
        assert hasattr(model, "topic_id")
        assert hasattr(model, "adaptative_object_id")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Template model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["Template"]
        assert hasattr(model, "pages")

    def test_model_has_correct_attribute_types(self, mock_template: Model):
        """Test case to assert that the Template model has the correct attribute types

        Args:
            mock_template (Model): Mock Template
        """
        assert isinstance(mock_template.id, uuid.UUID)
        assert isinstance(mock_template.created_at, datetime)
        assert isinstance(mock_template.relative_position, int)
        assert isinstance(mock_template.title, str)
        assert isinstance(mock_template.description, str)
        assert isinstance(mock_template.image_url, str)
        assert isinstance(mock_template.default_knowledge, int)
        assert isinstance(mock_template.knowledge_weight, int)
        assert isinstance(mock_template.leak_parameter, float)
        assert isinstance(mock_template.topic_id, uuid.UUID)
        assert isinstance(mock_template.adaptative_object_id, uuid.UUID)

    def test_model_has_correct_relationship_types(self, mock_template: Model):
        """Test case to assert that the Template model has the correct
        relationship types

        Args:
            mock_template (Model): Mock Template
        """
        assert isinstance(mock_template.adaptative_object, object)
        assert isinstance(mock_template.pages, list)
        assert isinstance(mock_template.topic, object)
