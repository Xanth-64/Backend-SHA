# -*- coding: utf-8 -*-
from typing import Dict

from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy.exc import IntegrityError
from src.services.utils.middleware.auth_middleware import auth_middleware


def update_one_practice_test_controller_factory(
    db: SQLAlchemy,
    models: Dict[str, Model],
    practice_test_schema: Schema,
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    @blueprint.route("/<string:uuid>", methods=["PUT", "PATCH"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def update_one_practice_test(uuid: str, current_user=None):
        """Controller function to Create an Instance of a given Model.

        Returns:
            dict: Dictionary Containing the Newly Created Model Instance.
        """
        req_data = request.get_json()
        old_data = models["PracticeTest"].query.get(uuid)

        if old_data is None:
            return {
                "success": False,
                "message": f"uuid {uuid} not found",
                "data": {
                    "error": "MODEL_NOT_FOUND",
                    "message": f"uuid {uuid} not found",
                },
            }, 400
        if len(old_data.test_attempts.all()) > 0:
            return {
                "success": False,
                "message": f"uuid {uuid} has test attempts",
                "data": {
                    "error": "MODEL_HAS_TEST_ATTEMPTS",
                    "message": f"uuid {uuid} has test attempts",
                },
            }, 400
        if req_data.get("title"):
            old_data.title = req_data.get("title")
        if req_data.get("show_on_init"):
            old_data.show_on_init = req_data.get("show_on_init")
        if req_data.get("test_questions"):
            for test_question in old_data.test_questions:
                db.session.delete(test_question)
            db.session.commit()
            old_data.test_questions = []
            total_score = 0
            for i, test_question in enumerate(req_data.get("test_questions"), start=1):
                new_test_question = models["TestQuestion"](
                    question_type=test_question.get("question_type"),
                    question_prompt=test_question.get("question_prompt"),
                    relative_position=i,
                    question_score=test_question.get("question_score"),
                    question_hint=test_question.get("question_hint"),
                )
                for answer_alternative in test_question.get("answer_alternatives"):
                    new_test_question.answer_alternatives.append(
                        models["AnswerAlternative"](**answer_alternative)
                    )
                new_test_question.adaptative_object = models["AdaptativeObject"]()
                old_data.test_questions.append(new_test_question)
                total_score += new_test_question.question_score
            old_data.total_score = total_score
        try:
            db.session.commit()

        except IntegrityError:
            return {
                "success": False,
                "data": {
                    "error": "UNIQUE_VIOLATION",
                    "message": "Database Constraint Violation",
                },
                "message": "Database Integrity Error",
            }, 400
        return {
            "success": True,
            "message": "Model Data Updated Successfully",
            "data": practice_test_schema().dump(obj=old_data, many=False),
        }, 200
