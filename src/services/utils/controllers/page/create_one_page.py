# -*- coding: utf-8 -*-
from typing import Dict
from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from src.services.utils.middleware.auth_middleware import auth_middleware


def create_one_page_controller_factory(
    db: SQLAlchemy,
    models: Dict[str, Model],
    page_schema: Schema,
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    @blueprint.route("/", methods=["POST"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def create_one_page(current_user=None):
        """Controller function to Create an Instance of a given Model.

        Returns:
            dict: Dictionary Containing the Newly Created Model Instance.
        """
        req_data = request.get_json()
        template = models["Template"].query.get(req_data["template_id"])
        if template is None:
            return {
                "success": False,
                "message": f"template_id {req_data['template_id']} not found",
                "data": {
                    "error": "TEMPLATE_NOT_FOUND",
                    "message": f"template_id {req_data['template_id']} not found",
                },
            }
        relative_position = (
            db.session.query(func.max(models["Page"].relative_position))
            .filter(models["Page"].template_id == req_data.get("template_id"))
            .scalar()
        )
        relative_position = relative_position + 1 if relative_position else 1
        new_instance = models["Page"](
            relative_position=relative_position, template_id=req_data["template_id"]
        )
        if req_data.get("learning_content"):
            new_instance.learning_content = models["LearningContent"](
                **req_data.get("learning_content")
            )
        if req_data.get("practice_test"):
            practice_test = req_data.get("practice_test")
            new_instance.practice_test = models["PracticeTest"](
                title=practice_test.get("title"),
                show_on_init=practice_test.get("show_on_init"),
            )
            total_score = 0
            for i, test_question in enumerate(
                practice_test.get("test_questions"), start=1
            ):
                new_test_question = models["TestQuestion"](
                    question_type=test_question.get("question_type"),
                    question_prompt=test_question.get("question_prompt"),
                    relative_position=i,
                    question_score=test_question.get("question_score"),
                )
                for answer_alternative in test_question.get("answer_alternatives"):
                    new_test_question.answer_alternatives.append(
                        models["AnswerAlternative"](**answer_alternative)
                    )
                new_instance.practice_test.test_questions.append(new_test_question)
                total_score += new_test_question.question_score
            new_instance.practice_test.total_score = total_score
        try:
            db.session.add(new_instance)
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
            "message": "Model Data Created Successfully",
            "data": page_schema().dump(obj=new_instance, many=False),
        }, 200
