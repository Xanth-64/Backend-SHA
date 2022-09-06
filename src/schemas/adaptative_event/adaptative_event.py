# -*- coding: utf-8 -*-
from typing import Dict

from flask_marshmallow import Marshmallow
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model


def create_adaptative_event_complete_schema(
    ma: Marshmallow, schemas: Dict[str, Schema], models: Dict[str, Model]
) -> Schema:
    class AdaptativeEventCompleteSchema(ma.SQLAlchemySchema):
        class Meta:
            model = models["AdaptativeEvent"]

        id = ma.auto_field()
        created_at = ma.auto_field()
        triggered_change = ma.auto_field()
        condition_aggregator = ma.auto_field()
        relative_position = ma.auto_field()
        adaptative_object_id = ma.auto_field()
        adaptation_conditions = ma.Nested(
            schemas["AdaptationCondition_DefaultSchema"], many=True
        )

    return AdaptativeEventCompleteSchema
