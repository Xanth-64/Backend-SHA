# -*- coding: utf-8 -*-
"""Test case suite for the Non Default Schemas."""

from typing import Dict

from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model
from marshmallow_sqlalchemy.schema import SQLAlchemyAutoSchema


class TestNonDefaultSchemas:
    """Test suite for the Default Schemas"""

    def test_schemas_exist(self, schemas: Dict[str, SQLAlchemyAutoSchema]):
        """Test that all of the Schemas are created"""
        assert "User_CurrentUserSchema" in schemas
        assert "AdaptativeEvent_CompleteSchema" in schemas
        assert "AdaptativeObject_CompleteSchema" in schemas
        assert "AnswerAlternative_StudentSchema" in schemas
        assert "TestQuestion_WithoutAnswersSchema" in schemas
        assert "TestQuestion_WithAnswersSchema" in schemas
        assert "PracticeTest_WithoutAnswers" in schemas
        assert "PracticeTest_WithAnswers" in schemas
        assert "Page_PageInheritanceSchema" in schemas
        assert "LearningContent_WithPageSchema" in schemas
        assert "TopicPrecedence_TopicPrecedenceRelationSchema" in schemas
        assert "QuestionAnswer_CompleteSchema" in schemas
        assert "TestAttempt_CompleteSchema" in schemas
        assert "User_UserAndRoleSchema" in schemas

    def test_schemas_are_correct_type(self, schemas: Dict[str, SQLAlchemyAutoSchema]):
        """Test that all of the Schemas are of the correct type"""
        assert isinstance(schemas["User_CurrentUserSchema"](), Schema)
        assert isinstance(schemas["AdaptativeEvent_CompleteSchema"](), Schema)
        assert isinstance(schemas["AdaptativeObject_CompleteSchema"](), Schema)
        assert isinstance(schemas["AnswerAlternative_StudentSchema"](), Schema)
        assert isinstance(schemas["TestQuestion_WithoutAnswersSchema"](), Schema)
        assert isinstance(schemas["TestQuestion_WithAnswersSchema"](), Schema)
        assert isinstance(schemas["PracticeTest_WithoutAnswers"](), Schema)
        assert isinstance(schemas["PracticeTest_WithAnswers"](), Schema)
        assert isinstance(schemas["Page_PageInheritanceSchema"](), Schema)
        assert isinstance(schemas["LearningContent_WithPageSchema"](), Schema)
        assert isinstance(
            schemas["TopicPrecedence_TopicPrecedenceRelationSchema"](), Schema
        )
        assert isinstance(schemas["QuestionAnswer_CompleteSchema"](), Schema)
        assert isinstance(schemas["TestAttempt_CompleteSchema"](), Schema)
        assert isinstance(schemas["User_UserAndRoleSchema"](), Schema)

    def test_schemas_have_correct_fields(
        self, schemas: Dict[str, SQLAlchemyAutoSchema]
    ):
        assert set(schemas["User_CurrentUserSchema"]().fields.keys()) == {
            "id",
            "created_at",
            "email",
            "first_name",
            "last_name",
            "image_url",
            "vark_completed",
            "learning_style",
        }
        assert set(schemas["AdaptativeEvent_CompleteSchema"]().fields.keys()) == {
            "id",
            "created_at",
            "triggered_change",
            "condition_aggregator",
            "relative_position",
            "adaptative_object_id",
            "adaptation_conditions",
        }

        assert set(schemas["AdaptativeObject_CompleteSchema"]().fields.keys()) == {
            "id",
            "created_at",
            "adaptative_events",
        }

        assert set(schemas["AnswerAlternative_StudentSchema"]().fields.keys()) == {
            "id",
            "created_at",
            "alternative_text",
            "test_question_id",
        }

        assert set(schemas["TestQuestion_WithoutAnswersSchema"]().fields.keys()) == {
            "id",
            "created_at",
            "question_type",
            "question_prompt",
            "relative_position",
            "question_score",
            "practice_test_id",
            "question_hint",
            "answer_alternatives",
            "adaptative_object",
            "adaptative_object_id",
        }

        assert set(schemas["TestQuestion_WithAnswersSchema"]().fields.keys()) == {
            "id",
            "created_at",
            "question_type",
            "question_prompt",
            "relative_position",
            "question_score",
            "practice_test_id",
            "question_hint",
            "answer_alternatives",
            "adaptative_object",
            "adaptative_object_id",
        }

        assert set(schemas["PracticeTest_WithoutAnswers"]().fields.keys()) == {
            "id",
            "created_at",
            "title",
            "show_on_init",
            "total_score",
            "page_id",
            "approval_score",
            "adaptation_weight",
            "test_questions",
            "page",
        }

        assert set(schemas["PracticeTest_WithAnswers"]().fields.keys()) == {
            "id",
            "created_at",
            "title",
            "show_on_init",
            "total_score",
            "page_id",
            "approval_score",
            "adaptation_weight",
            "test_questions",
            "page",
        }

        assert set(schemas["Page_PageInheritanceSchema"]().fields.keys()) == {
            "id",
            "created_at",
            "relative_position",
            "template_id",
            "learning_content",
            "practice_test",
            "adaptative_object_id",
        }

        assert set(schemas["LearningContent_WithPageSchema"]().fields.keys()) == {
            "id",
            "created_at",
            "title",
            "content",
            "page",
        }

        assert set(
            schemas["TopicPrecedence_TopicPrecedenceRelationSchema"]().fields.keys()
        ) == {
            "id",
            "created_at",
            "knowledge_weight",
            "predecessor",
            "successor",
        }

        assert set(schemas["QuestionAnswer_CompleteSchema"]().fields.keys()) == {
            "id",
            "created_at",
            "acquired_score",
            "is_correct",
            "test_attempt_id",
            "test_question",
            "selected_answer_alternatives",
        }

        assert set(schemas["TestAttempt_CompleteSchema"]().fields.keys()) == {
            "id",
            "created_at",
            "acquired_score",
            "user_id",
            "practice_test",
            "question_answers",
        }

        assert set(schemas["User_UserAndRoleSchema"]().fields.keys()) == {
            "id",
            "created_at",
            "email",
            "first_name",
            "last_name",
            "image_url",
            "vark_completed",
            "role",
        }
