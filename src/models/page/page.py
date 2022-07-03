# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy


def page(db: SQLAlchemy):
    class Page(db.Model):
        pass

    return Page
