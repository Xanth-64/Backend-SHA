# -*- coding: utf-8 -*-
from typing import Dict

from flask_marshmallow import Marshmallow
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model


def create_question_answer_complete_schema(
    ma: Marshmallow, schemas: Dict[str, Schema], models: Dict[str, Model]
) -> Schema:
    class QuestionAnswerCompleteSchema(ma.SQLAlchemySchema):
        class Meta:
            model = models["QuestionAnswer"]

        id = ma.auto_field()
        created_at = ma.auto_field()
        acquired_score = ma.auto_field()
        is_correct = ma.auto_field()
        test_attempt_id = ma.auto_field()
        test_question = ma.Nested(schemas["TestQuestion_WithAnswersSchema"])
        selected_answer_alternatives = ma.Nested(
            schemas["SelectedAnswerAlternatives_DefaultSchema"], many=True
        )

    return QuestionAnswerCompleteSchema
