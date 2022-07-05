# -*- coding: utf-8 -*-
"""Module Containing the Topic Precedence Helper Table

This module contains the Helper Table Definition for the Relation of Topic Precedence
in the Database

Typical usage example:

    ...
    import src.models.many_to_many import topic_precedence

    class Model:
        ### Other Model Params
        relationship = db.relationship('relationship_name',
        secondary=topic_precedence.get_helper_table(db),
        lazy=True,backref=db.backref('relationship_backname', lazy=True))
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import UUID


def get_helper_table(db: SQLAlchemy) -> Table:
    return db.Table(
        "topic_precedence",
        db.Column(
            "predecessor",
            UUID(as_uuid=True),
            db.ForeignKey("topic.id"),
            primary_key=True,
        ),
        db.Column(
            "successor",
            UUID(as_uuid=True),
            db.ForeignKey("topic.id"),
            primary_key=True,
        ),
    )
