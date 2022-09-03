# -*- coding: utf-8 -*-
"""Module Containing the Database Models Index

This module groups all of the Model Definitions  for the Backend.
Aggregating them under the same object.

Typical usage example:

    ...
    from models.index import create_models

    ...

    models = create_models(db)

    ...
"""
from typing import Dict

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from src.models.answer_alternative import answer_alternative
from src.models.interaction_fired import interaction_fired
from src.models.learning_content import learning_content
from src.models.learning_style import learning_style
from src.models.measurable_interaction import measurable_interaction
from src.models.page import page
from src.models.practice_test import practice_test
from src.models.question_answer import question_answer
from src.models.role import role
from src.models.selected_answer_alternatives import selected_answer_alternatives
from src.models.template import template
from src.models.test_attempt import test_attempt
from src.models.test_question import test_question
from src.models.topic import topic
from src.models.topic_predence import topic_precedence
from src.models.user import user


def create_models(db: SQLAlchemy) -> Dict[str, Model]:
    """Function to Create all of the Models in the database"""
    model_dict = {
        "AnswerAlternative": answer_alternative.create_model(db),
        "InteractionFired": interaction_fired.create_model(db),
        "LearningContent": learning_content.create_model(db),
        "LearningStyle": learning_style.create_model(db),
        "MeasurableInteraction": measurable_interaction.create_model(db),
        "Page": page.create_model(db),
        "PracticeTest": practice_test.create_model(db),
        "QuestionAnswer": question_answer.create_model(db),
        "Role": role.create_model(db),
        "SelectedAnswerAlternatives": selected_answer_alternatives.create_model(db),
        "Template": template.create_model(db),
        "TestAttempt": test_attempt.create_model(db),
        "TestQuestion": test_question.create_model(db),
        "Topic": topic.create_model(db),
        "TopicPrecedence": topic_precedence.create_model(db),
        "User": user.create_model(db),
    }
    return model_dict
