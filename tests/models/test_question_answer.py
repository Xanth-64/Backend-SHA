# -*- coding: utf-8 -*-
"""Test case suite for the Question Answer model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestQuestionAnswerModel:
    """Test suite for the Question Answer model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Question Answer model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "QuestionAnswer" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Question Answer model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["QuestionAnswer"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "acquired_score")
        assert hasattr(model, "is_correct")
        assert hasattr(model, "test_attempt_id")
        assert hasattr(model, "test_question_id")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Question Answer model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["QuestionAnswer"]
        assert hasattr(model, "selected_answer_alternatives")

    def test_model_has_correct_attribute_types(self, mock_question_answer: Model):
        """Test case to assert that the Question Answer model has the correct attribute types

        Args:
            mock_question_answer (Model): Mock QuestionAnswer
        """
        assert isinstance(mock_question_answer.id, uuid.UUID)
        assert isinstance(mock_question_answer.created_at, datetime)
        assert isinstance(mock_question_answer.acquired_score, int)
        assert isinstance(mock_question_answer.is_correct, bool)
        assert isinstance(mock_question_answer.test_attempt_id, uuid.UUID)
        assert isinstance(mock_question_answer.test_question_id, uuid.UUID)

    def test_model_has_correct_relationship_types(self, mock_question_answer: Model):
        """Test case to assert that the Question Answer model has the correct
        relationship types

        Args:
            mock_question_answer (Model): Mock QuestionAnswer
        """
        assert isinstance(mock_question_answer.selected_answer_alternatives.all(), list)
        assert isinstance(mock_question_answer.test_attempt, Model)
        assert isinstance(mock_question_answer.test_question, Model)
