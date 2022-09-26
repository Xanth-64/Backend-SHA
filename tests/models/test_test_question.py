# -*- coding: utf-8 -*-
"""Test case suite for the Test Question model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestTestQuestionModel:
    """Test suite for the Test Question model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Test Question model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "TestQuestion" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Test Question model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["TestQuestion"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "question_type")
        assert hasattr(model, "question_prompt")
        assert hasattr(model, "relative_position")
        assert hasattr(model, "question_score")
        assert hasattr(model, "practice_test_id")
        assert hasattr(model, "question_hint")
        assert hasattr(model, "adaptative_object_id")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Test Question model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["TestQuestion"]
        assert hasattr(model, "answer_alternatives")
        assert hasattr(model, "question_answers")

    def test_model_has_correct_attribute_types(self, mock_test_question: Model):
        """Test case to assert that the Test Question model has the correct attribute types

        Args:
            mock_test_question (Model): Mock TestQuestion
        """
        assert isinstance(mock_test_question.id, uuid.UUID)
        assert isinstance(mock_test_question.created_at, datetime)
        assert isinstance(mock_test_question.question_type, str)
        assert isinstance(mock_test_question.question_prompt, str)
        assert isinstance(mock_test_question.relative_position, int)
        assert isinstance(mock_test_question.question_score, int)
        assert isinstance(mock_test_question.practice_test_id, uuid.UUID)
        assert isinstance(mock_test_question.question_hint, str)
        assert isinstance(mock_test_question.adaptative_object_id, uuid.UUID)

    def test_model_has_correct_relationship_types(self, mock_test_question: Model):
        """Test case to assert that the Test Question model has the correct
        relationship types

        Args:
            mock_test_question (Model): Mock TestQuestion
        """
        assert isinstance(mock_test_question.answer_alternatives.all(), list)
        assert isinstance(mock_test_question.question_answers.all(), list)
        assert isinstance(mock_test_question.practice_test, Model)
        assert isinstance(mock_test_question.adaptative_object, Model)
