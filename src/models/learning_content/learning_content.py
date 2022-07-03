# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy


def learning_content(db: SQLAlchemy):
    class LearningContent(db.Model):
        pass

    return LearningContent
