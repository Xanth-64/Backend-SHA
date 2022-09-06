# -*- coding: utf-8 -*-
from typing import Dict

from flask_marshmallow import Marshmallow
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model


def create_test_question_inheritance_schema(
    ma: Marshmallow,
    answer_alternative_schema: Schema,
    adaptative_object_schema: Schema,
    models: Dict[str, Model],
) -> Schema:
    class TestQuestionInheritanceSchema(ma.SQLAlchemySchema):
        class Meta:
            model = models["TestQuestion"]

        id = ma.auto_field()
        created_at = ma.auto_field()
        question_type = ma.auto_field()
        question_prompt = ma.auto_field()
        relative_position = ma.auto_field()
        question_score = ma.auto_field()
        practice_test_id = ma.auto_field()
        question_hint = ma.auto_field()
        answer_alternatives = ma.Nested(answer_alternative_schema, many=True)
        adaptative_object = ma.Nested(adaptative_object_schema)

    return TestQuestionInheritanceSchema
