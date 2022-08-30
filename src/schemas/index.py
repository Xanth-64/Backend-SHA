# -*- coding: utf-8 -*-
"""Module Containing the API Schemas Index

This module groups all of the Schema Definitions  for the Backend.
Aggregating them under the same object.

Typical usage example:"""
from typing import Dict

from flask_marshmallow import Marshmallow
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model
from src.schemas.answer_alternative.answer_alternative import (
    create_answer_alternative_student_schema,
)
from src.schemas.practice_test.practice_test import (
    create_test_with_answer_alternatives_schema,
)
from src.schemas.question_answer.question_answer import (
    create_question_answer_complete_schema,
)
from src.schemas.test_attempt.test_attempt import create_test_attempt_complete_schema
from src.schemas.test_question.test_question import (
    create_test_question_inheritance_schema,
)
from src.schemas.topic.topic import create_topic_precedence_schema
from src.schemas.topic_precedence.topic_precedence import (
    create_topic_precedence_relation_schema,
)
from src.schemas.user.user import (
    create_current_user_schema,
    create_user_and_role_schema,
)
from src.services.utils.schemas.create_default_schema import create_default_schema

from .page.page import create_page_inheritance_schema


def create_schemas(ma: Marshmallow, models: Dict[str, Model]) -> Dict[str, Schema]:
    """Function to create all of the Schemas in the API"""
    schemas = {}
    # NOTE Creation of the Default Schemas (Containing all of the Properties in the Model)
    for model_name, model in models.items():
        schemas[f"{model_name}_DefaultSchema"] = create_default_schema(
            ma=ma,
            db_model=model,
            config_include_fk=True,
            config_include_relationships=False,
        )
    # Create Schema for Representing the Current User Object
    schemas["User_CurrentUserSchema"] = create_current_user_schema(
        ma=ma, schemas=schemas, db_model=models["User"]
    )
    # Create Schemas for the Different ways of presenting Answer Alternatives
    schemas[
        "AnswerAlternative_StudentSchema"
    ] = create_answer_alternative_student_schema(ma, models)

    # Create Schemas for the Different ways of presenting Test Questions
    schemas[
        "TestQuestion_WithoutAnswersSchema"
    ] = create_test_question_inheritance_schema(
        ma, schemas["AnswerAlternative_StudentSchema"], models
    )
    schemas["TestQuestion_WithAnswersSchema"] = create_test_question_inheritance_schema(
        ma, schemas["AnswerAlternative_DefaultSchema"], models
    )
    # Create Schemas for the Different ways of presenting Practice Tests
    schemas[
        "PracticeTest_WithoutAnswers"
    ] = create_test_with_answer_alternatives_schema(
        ma, schemas["TestQuestion_WithoutAnswersSchema"], models
    )
    schemas["PracticeTest_WithAnswers"] = create_test_with_answer_alternatives_schema(
        ma, schemas["TestQuestion_WithAnswersSchema"], models
    )
    # Create a Schema for Page Inheritance (Containing all of the Properties in the Models Child Classes)
    schemas["Page_PageInheritanceSchema"] = create_page_inheritance_schema(
        ma, schemas, models
    )
    # Create a Schema for Topic Precedence
    schemas[
        "TopicPrecedence_TopicPrecedenceRelationSchema"
    ] = create_topic_precedence_relation_schema(ma, schemas, models)

    # Create a Schema for a Question Answer
    schemas["QuestionAnswer_CompleteSchema"] = create_question_answer_complete_schema(
        ma, schemas, models
    )
    # Create a Schema for a Test Attempt
    schemas["TestAttempt_CompleteSchema"] = create_test_attempt_complete_schema(
        ma, schemas, models
    )

    # Create a Schema for including a user and their role
    schemas["User_UserAndRoleSchema"] = create_user_and_role_schema(ma, schemas, models)
    return schemas
