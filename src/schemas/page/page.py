# -*- coding: utf-8 -*-
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model
from flask_marshmallow import Marshmallow
from typing import Dict


def create_page_inheritance_schema(
    ma: Marshmallow, schemas: Dict[str, Schema], models: Dict[str, Model]
) -> Schema:
    class PageInheritanceSchema(ma.SQLAlchemySchema):
        class Meta:
            model = models["Page"]

        id = ma.auto_field()
        created_at = ma.auto_field()
        relative_position = ma.auto_field()
        template_id = ma.auto_field()
        learning_content = ma.Nested(schemas["LearningContent_DefaultSchema"])
        practice_test = ma.Nested(schemas["PracticeTest_DefaultSchema"])

    return PageInheritanceSchema
