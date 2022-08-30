# -*- coding: utf-8 -*-
from typing import Dict
from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy.exc import IntegrityError
from src.services.utils.middleware.auth_middleware import auth_middleware


def create_one_test_attempt_controller_factory(
    db: SQLAlchemy,
    models: Dict[str, Model],
    schemas: Dict[str, Schema],
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    @blueprint.route("/", methods=["POST"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def create_one_test_attempt(current_user=None):
        """Controller function to Create an Instance of a given Model.

        Returns:
            dict: Dictionary Containing the Newly Created Model Instance.
        """
        req_data = request.get_json()
        # Get the corresponding practice test instance.
        practice_test = models["PracticeTest"].query.get(
            req_data.get("practice_test_id")
        )

        # Check if the practice test instance exists.
        if practice_test is None:
            return {
                "message": f"Practice Test with ID {req_data.get('practice_test_id')} does not exist.",
                "success": False,
                "data": {
                    "error": "TEST_NOT_FOUND",
                    "message": f"Practice Test with ID {req_data.get('practice_test_id')} does not exist.",
                },
            }, 400

        # Check if the practice test instance has test attempts by the current user.
        test_attempts = practice_test.test_attempts.filter_by(
            user_id=current_user.id
        ).first()
        if test_attempts is not None:
            return {
                "message": f"Practice Test with ID {req_data.get('practice_test_id')} has test attempts.",
                "success": False,
                "data": {
                    "error": "MODEL_HAS_TEST_ATTEMPTS",
                    "message": f"Practice Test with ID {req_data.get('practice_test_id')} has test attempts.",
                },
            }, 400

        # Create the test attempt instance
        test_attempt = models["TestAttempt"](
            user_id=current_user.id, practice_test_id=practice_test.id
        )
        # Initialize the test attempt score to 0.
        test_attempt_score = 0
        # Add the question answers to the test attempt instance.
        for question_answer in req_data.get("question_answers"):
            # Check if the test_question_id provided in the question_answer exists.
            test_question = practice_test.test_questions.filter_by(
                id=question_answer.get("test_question_id")
            ).first()
            if test_question is None:
                return {
                    "message": f"Test Question with ID {question_answer.get('test_question_id')} does not exist.",
                    "success": False,
                    "data": {
                        "error": "QUESTION_NOT_FOUND",
                        "message": f"Test Question with ID {question_answer.get('test_question_id')} does not exist.",
                    },
                }, 400

            new_question_answer = models["QuestionAnswer"](
                test_question_id=test_question.id
            )
            # Create a temporal array to store the question answer alternatives.
            answer_alternatives = []
            # Add the Selected Answer Alternatives to the Question Answer Instance.
            for selected_answer_alternative in question_answer.get(
                "selected_answer_alternatives"
            ):
                # Check if the selected answer alternative exists.
                answer_alternative = test_question.answer_alternatives.filter_by(
                    id=selected_answer_alternative
                ).first()
                if answer_alternative is None:
                    return {
                        "message": f"Answer Alternative with ID {selected_answer_alternative} does not exist.",
                        "success": False,
                        "data": {
                            "error": "ANSWER_ALTERNATIVE_NOT_FOUND",
                            "message": f"Answer Alternative with ID {selected_answer_alternative} does not exist.",
                        },
                    }, 400
                new_question_answer.selected_answer_alternatives.append(
                    models["SelectedAnswerAlternatives"](
                        answer_alternative_id=answer_alternative.id,
                        question_answer=new_question_answer,
                    )
                )
                answer_alternatives.append(answer_alternative)
            # Check if the selected answer alternatives are correct, depending if question is simple_selection or multiple_selection.
            if test_question.question_type == "simple_selection":
                # Check if the selected answer alternative is correct.
                new_question_answer.is_correct = answer_alternative.is_correct
            elif test_question.question_type == "multiple_selection":
                # Check if the selected answer alternatives are correct and that all correct answers were selected.
                new_question_answer.is_correct = all(
                    answer_alternative.is_correct
                    for answer_alternative in answer_alternatives
                ) and all(
                    answer_alternative in answer_alternatives
                    for answer_alternative in test_question.answer_alternatives.filter_by(
                        is_correct=True
                    ).all()
                )
            # Set the Question Answer Score depending if it was correct or not.
            new_question_answer.acquired_score = (
                test_question.question_score if new_question_answer.is_correct else 0
            )
            # Add the Question Answer acquired score to the test attempt score.
            test_attempt_score += new_question_answer.acquired_score

            # Add the Question Answer to the Test Attempt instance.
            test_attempt.question_answers.append(new_question_answer)
        # Add the Question Answer to the Test Attempt Instance.
        test_attempt.question_answers.append(new_question_answer)

        # Set the Test Attempt Score.
        test_attempt.acquired_score = test_attempt_score

        # Add the Test Attempt to the Database and commit the changes.
        try:
            db.session.add(test_attempt)
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
            "data": schemas["TestAttempt_CompleteSchema"]().dump(
                obj=test_attempt, many=False
            ),
        }, 200
