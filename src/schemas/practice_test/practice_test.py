# -*- coding: utf-8 -*-
from typing import Dict

from flask_marshmallow import Marshmallow
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model


def create_test_with_answer_alternatives_schema(
    ma: Marshmallow,
    test_question_schema,
    models: Dict[str, Model],
) -> Schema:
    class TestWithAnswersSchema(ma.SQLAlchemySchema):
        class Meta:
            model = models["PracticeTest"]

        id = ma.auto_field()
        created_at = ma.auto_field()
        title = ma.auto_field()
        show_on_init = ma.auto_field()
        total_score = ma.auto_field()
        page_id = ma.auto_field()
        test_questions = ma.Nested(test_question_schema, many=True)

    return TestWithAnswersSchema
