# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy


def test_question(db: SQLAlchemy):
    class TestQuestion(db.Model):
        pass

    return TestQuestion
