# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy


def practice_test(db: SQLAlchemy):
    class PracticeTest(db.Model):
        pass

    return PracticeTest
