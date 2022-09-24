# -*- coding: utf-8 -*-
from typing import Dict

from flask_marshmallow import Marshmallow
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model


def create_learning_content_with_page_schema(
    ma: Marshmallow,
    schemas: Dict[str, Schema],
    models: Dict[str, Model],
) -> Schema:
    class LearningContentWithPageSchema(ma.SQLAlchemySchema):
        class Meta:
            model = models["LearningContent"]

        id = ma.auto_field()
        created_at = ma.auto_field()
        title = ma.auto_field()
        content = ma.auto_field()
        page = ma.Nested(schemas["Page_DefaultSchema"], many=False)

    return LearningContentWithPageSchema
