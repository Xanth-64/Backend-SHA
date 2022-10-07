# -*- coding: utf-8 -*-
"""Test case suite for the Practice Test model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestPracticeTestModel:
    """Test suite for the Practice Test model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Practice Test model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "PracticeTest" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Practice Test model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["PracticeTest"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "title")
        assert hasattr(model, "show_on_init")
        assert hasattr(model, "adaptation_weight")
        assert hasattr(model, "approval_score")
        assert hasattr(model, "page_id")
        assert hasattr(model, "total_score")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Practice Test model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["PracticeTest"]
        assert hasattr(model, "test_questions")
        assert hasattr(model, "test_attempts")

    def test_model_has_correct_attribute_types(self, mock_practice_test: Model):
        """Test case to assert that the Practice Test model has the correct attribute types

        Args:
            mock_practice_test (Model): Mock PracticeTest
        """
        assert isinstance(mock_practice_test.id, uuid.UUID)
        assert isinstance(mock_practice_test.created_at, datetime)
        assert isinstance(mock_practice_test.title, str)
        assert isinstance(mock_practice_test.show_on_init, bool)
        assert isinstance(mock_practice_test.adaptation_weight, int)
        assert isinstance(mock_practice_test.approval_score, int)
        assert isinstance(mock_practice_test.page_id, uuid.UUID)
        assert isinstance(mock_practice_test.total_score, int)

    def test_model_has_correct_relationship_types(self, mock_practice_test: Model):
        """Test case to assert that the Practice Test model has the correct
        relationship types

        Args:
            mock_practice_test (Model): Mock PracticeTest
        """
        assert isinstance(mock_practice_test.test_questions.all(), list)
        assert isinstance(mock_practice_test.test_attempts.all(), list)
        assert isinstance(mock_practice_test.page, Model)
