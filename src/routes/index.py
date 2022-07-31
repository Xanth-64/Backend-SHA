# -*- coding: utf-8 -*-
"""Module Containing the Database Routes Index

This module groups all of the Route Definitions  for the Backend.

Typical usage example:

    ...
    from routes.index import create_blueprints

    ...

    create_blueprints(db, models, schemas, app)

    ...
"""
from firebase_admin import App
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.routes.answer_alternative.answer_alternative_blueprint import (
    create_answer_alternative_blueprint,
)
from src.routes.auth.auth_blueprint import create_auth_blueprint
from src.routes.learning_content.learning_content_blueprint import (
    create_learning_content_blueprint,
)
from src.routes.page.page_blueprint import create_page_blueprint
from src.routes.practice_test.practice_test_blueprint import (
    create_practice_test_blueprint,
)
from src.routes.role.role_blueprint import create_role_blueprint
from src.routes.template.template_blueprint import create_template_blueprint
from src.routes.test_question.test_question_blueprint import (
    create_test_question_blueprint,
)
from src.routes.topic.topic_blueprint import create_topic_blueprint
from src.routes.user.user_blueprint import create_user_blueprint


def create_blueprints(
    db: SQLAlchemy, models, schemas, app: Flask, firebase_app: App
) -> None:
    """Function to Instantiate all of the Blueprints in the API (v1)

    Args:
        db (SQLAlchemy): Database connection object.
        models (dict): Dictionary Containing all of the Models in the API.
        schemas (dict): Dictionary Containing all of the Schemas in the API.
        app (Flask): Flask Application Object.
        firebase_app (App): Firebase App Object.
    """
    app.register_blueprint(
        blueprint=create_answer_alternative_blueprint(db, models, schemas, firebase_app)
    )
    app.register_blueprint(
        blueprint=create_auth_blueprint(db, models, schemas, firebase_app)
    )
    app.register_blueprint(
        blueprint=create_learning_content_blueprint(db, models, schemas, firebase_app)
    )
    app.register_blueprint(
        blueprint=create_page_blueprint(db, models, schemas, firebase_app)
    )
    app.register_blueprint(
        blueprint=create_practice_test_blueprint(db, models, schemas, firebase_app)
    )
    app.register_blueprint(
        blueprint=create_role_blueprint(db, models, schemas, firebase_app)
    )
    app.register_blueprint(
        blueprint=create_template_blueprint(db, models, schemas, firebase_app)
    )
    app.register_blueprint(
        blueprint=create_test_question_blueprint(db, models, schemas, firebase_app)
    )
    app.register_blueprint(
        blueprint=create_topic_blueprint(db, models, schemas, firebase_app)
    )

    app.register_blueprint(
        blueprint=create_user_blueprint(db, models, schemas, firebase_app)
    )
