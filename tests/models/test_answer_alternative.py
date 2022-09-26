# -*- coding: utf-8 -*-
"""Test case suite for the Answer Alternative model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestAnswerAlternativeModel:
    """Test suite for the Answer Alternative model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Answer Alternative model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "AnswerAlternative" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Answer Alternative model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["AnswerAlternative"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "alternative_text")
        assert hasattr(model, "is_correct")
        assert hasattr(model, "test_question_id")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Answer Alternative model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["AnswerAlternative"]
        assert hasattr(model, "selected_answer_alternatives")

    def test_model_has_correct_attribute_types(self, mock_answer_alternative: Model):
        """Test case to assert that the Answer Alternative model has the correct attribute types

        Args:
            mock_answer_alternative (Model): Mock Answer Alternative
        """
        assert isinstance(mock_answer_alternative.id, uuid.UUID)
        assert isinstance(mock_answer_alternative.created_at, datetime)
        assert isinstance(mock_answer_alternative.alternative_text, str)
        assert isinstance(mock_answer_alternative.is_correct, bool)
        assert isinstance(mock_answer_alternative.test_question_id, uuid.UUID)

    def test_model_has_correct_relationship_types(self, mock_answer_alternative: Model):
        """Test case to assert that the Answer Alternative model has the correct
        relationship types

        Args:
            mock_answer_alternative (Model): Mock Answer Alternative
        """
        assert isinstance(
            mock_answer_alternative.selected_answer_alternatives.all(), list
        )
        assert isinstance(mock_answer_alternative.test_question, Model)
