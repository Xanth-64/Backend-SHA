# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy


def answer_alternative(db: SQLAlchemy):
    class AnswerAlternative(db.Model):
        pass

    return AnswerAlternative
