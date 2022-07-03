# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy


def role(db: SQLAlchemy):
    class Role(db.Model):
        pass

    return Role
