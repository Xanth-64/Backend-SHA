# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy


def topic(db: SQLAlchemy):
    class Topic(db.Model):
        pass

    return Topic
