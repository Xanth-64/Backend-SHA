# -*- coding: utf-8 -*-
from typing import Dict

from flask_marshmallow import Marshmallow
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model


def create_adaptative_object_complete_schema(
    ma: Marshmallow, schemas: Dict[str, Schema], models: Dict[str, Model]
) -> Schema:
    class AdaptativeObjectCompleteSchema(ma.SQLAlchemySchema):
        class Meta:
            model = models["AdaptativeObject"]

        id = ma.auto_field()
        created_at = ma.auto_field()
        adaptative_events = ma.Nested(
            schemas["AdaptativeEvent_CompleteSchema"], many=True
        )

    return AdaptativeObjectCompleteSchema
