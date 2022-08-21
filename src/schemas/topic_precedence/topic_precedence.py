# -*- coding: utf-8 -*-
from typing import Dict

from flask_marshmallow import Marshmallow
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model


def create_topic_precedence_relation_schema(
    ma: Marshmallow, schemas: Dict[str, Schema], models: Dict[str, Model]
) -> Schema:
    class TopicPrecedenceRelationSchema(ma.SQLAlchemySchema):
        class Meta:
            model = models["TopicPrecedence"]

        id = ma.auto_field()
        created_at = ma.auto_field()
        knowledge_weight = ma.auto_field()
        predecessor = ma.Nested(schemas["Topic_DefaultSchema"])
        successor = ma.Nested(schemas["Topic_DefaultSchema"])

    return TopicPrecedenceRelationSchema
