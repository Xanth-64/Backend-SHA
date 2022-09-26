# -*- coding: utf-8 -*-
"""Test case suite for the Test Attempt model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestTestAttemptModel:
    """Test suite for the Test Attempt model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Test Attempt model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "TestAttempt" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Test Attempt model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["TestAttempt"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "acquired_score")
        assert hasattr(model, "user_id")
        assert hasattr(model, "practice_test_id")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Test Attempt model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["TestAttempt"]
        assert hasattr(model, "question_answers")

    def test_model_has_correct_attribute_types(self, mock_test_attempt: Model):
        """Test case to assert that the Test Attempt model has the correct attribute types

        Args:
            mock_test_attempt (Model): Mock TestAttempt
        """
        assert isinstance(mock_test_attempt.id, uuid.UUID)
        assert isinstance(mock_test_attempt.created_at, datetime)
        assert isinstance(mock_test_attempt.acquired_score, int)
        assert isinstance(mock_test_attempt.user_id, uuid.UUID)
        assert isinstance(mock_test_attempt.practice_test_id, uuid.UUID)

    def test_model_has_correct_relationship_types(self, mock_test_attempt: Model):
        """Test case to assert that the Test Attempt model has the correct
        relationship types

        Args:
            mock_test_attempt (Model): Mock TestAttempt
        """
        assert isinstance(mock_test_attempt.question_answers, list)
        assert isinstance(mock_test_attempt.practice_test, Model)
        assert isinstance(mock_test_attempt.user, Model)
