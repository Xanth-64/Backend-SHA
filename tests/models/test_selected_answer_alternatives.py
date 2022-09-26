# -*- coding: utf-8 -*-
"""Test case suite for the Selected Answer Alternatives model."""

import uuid
from datetime import datetime
from typing import Dict

from flask_sqlalchemy.model import Model


class TestSelectedAnswerAlternativesModel:
    """Test suite for the Selected Answer Alternatives model's methods"""

    def test_model_exists(self, models: Dict[str, Model]):
        """Test case to assert that the Selected Answer Alternatives model exists

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        assert "SelectedAnswerAlternatives" in models

    def test_model_has_correct_fields(self, models: Dict[str, Model]):
        """Test case to assert that the Selected Answer Alternatives model has the correct fields

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["SelectedAnswerAlternatives"]
        assert hasattr(model, "id")
        assert hasattr(model, "created_at")
        assert hasattr(model, "question_answer_id")
        assert hasattr(model, "answer_alternative_id")

    def test_model_has_correct_relationships(self, models: Dict[str, Model]):
        """Test case to assert that the Selected Answer Alternatives model has the correct relationships

        Args:
            models (Dict[str, Model]): Dictionary of all of the models
        """
        model = models["SelectedAnswerAlternatives"]

    def test_model_has_correct_attribute_types(
        self, mock_selected_answer_alternatives: Model
    ):
        """Test case to assert that the Selected Answer Alternatives model has the correct attribute types

        Args:
            mock_selected_answer_alternatives (Model): Mock SelectedAnswerAlternatives
        """
        assert isinstance(mock_selected_answer_alternatives.id, uuid.UUID)
        assert isinstance(mock_selected_answer_alternatives.created_at, datetime)
        assert isinstance(
            mock_selected_answer_alternatives.question_answer_id, uuid.UUID
        )
        assert isinstance(
            mock_selected_answer_alternatives.answer_alternative_id, uuid.UUID
        )

    def test_model_has_correct_relationship_types(
        self, mock_selected_answer_alternatives: Model
    ):
        """Test case to assert that the Selected Answer Alternatives model has the correct
        relationship types

        Args:
            mock_selected_answer_alternatives (Model): Mock SelectedAnswerAlternatives
        """
        assert isinstance(mock_selected_answer_alternatives.question_answer, Model)
        assert isinstance(mock_selected_answer_alternatives.answer_alternative, Model)
