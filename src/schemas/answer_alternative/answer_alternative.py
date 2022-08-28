# -*- coding: utf-8 -*-
from typing import Dict

from flask_marshmallow import Marshmallow
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model


def create_answer_alternative_student_schema(
    ma: Marshmallow, models: Dict[str, Model]
) -> Schema:
    class AnswerAlternativeStudent(ma.SQLAlchemySchema):
        class Meta:
            model = models["AnswerAlternative"]

        id = ma.auto_field()
        created_at = ma.auto_field()
        alternative_text = ma.auto_field()
        test_question_id = ma.auto_field()

    return AnswerAlternativeStudent
