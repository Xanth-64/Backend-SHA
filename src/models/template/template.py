# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy


def template(db: SQLAlchemy):
    class Template(db.Model):
        pass

    return Template
