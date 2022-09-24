# -*- coding: utf-8 -*-
from marshmallow import Schema, fields


def create_topic_precedence_schema() -> Schema:
    """Helper Function that Creates a Default Schema for a Topic Precedence

    Returns:
        Schema: Topic Precedence Schema
    """

    class TopicPrecedenceSchema(Schema):
        """Topic Precedence Schema"""

        predecessor = fields.UUID()
        successor = fields.UUID()
        created_at = fields.DateTime()
        knowledge_weight = fields.Integer()

    return TopicPrecedenceSchema
