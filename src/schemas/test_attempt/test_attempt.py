# -*- coding: utf-8 -*-
from typing import Dict

from flask_marshmallow import Marshmallow
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model


def create_test_attempt_complete_schema(
    ma: Marshmallow, schemas: Dict[str, Schema], models: Dict[str, Model]
) -> Schema:
    class TestAttemptCompleteSchema(ma.SQLAlchemySchema):
        class Meta:
            model = models["TestAttempt"]

        id = ma.auto_field()
        created_at = ma.auto_field()
        acquired_score = ma.auto_field()
        user_id = ma.auto_field()
        practice_test = ma.Nested(schemas["PracticeTest_DefaultSchema"])
        question_answers = ma.Nested(
            schemas["QuestionAnswer_CompleteSchema"], many=True
        )

    return TestAttemptCompleteSchema
