# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy


def user(db: SQLAlchemy):
    class User(db.Model):
        pass

    return User
