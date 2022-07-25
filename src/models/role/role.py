# -*- coding: utf-8 -*-
"""Module Containing the Role Entity Model

This module contains the Model Definition for the Entity Representing a Role
in the Database

Typical usage example:

    ...
    import src.models.role import role

    {
        ### Other Model Definitions
        'Role' : role.create_model(db)
    }
"""

import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ENUM, UUID


def create_model(db: SQLAlchemy):
    class Role(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        role_name = db.Column(
            ENUM("student", "teacher", name="acc_role_enum"),
            default="student",
        )
        is_enabled = db.Column(db.Boolean, default=False)
        user_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False
        )

    return Role
