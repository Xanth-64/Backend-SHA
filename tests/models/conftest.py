# -*- coding: utf-8 -*-
import uuid
from typing import Dict

import pytest
from flask_sqlalchemy.model import Model


@pytest.fixture(scope="session")
def mock_user(models: Dict[str, Model], db):
    """Fixture to create a mock User

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection

    Returns:
        Model: Mock User
    """
    model = models["User"]
    # Create a New Mock User with a Random email
    new_instance = model(
        email=f"{uuid.uuid4()}@example.com",
        first_name="Example",
        last_name="User",
        image_url="https://example.com/image.png",
        vark_completed=True,
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_learning_style(models: Dict[str, Model], db, mock_user):
    """Fixture to create a mock Learning Style

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection

    Returns:
        Model: Mock Learning Style
    """
    model = models["LearningStyle"]
    # Create a New Mock Learning Style
    new_instance = model(
        visual=5,
        aural=5,
        kinesthetic=5,
        textual=5,
        user=mock_user,
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_role(models: Dict[str, Model], db, mock_user):
    """Fixture to create a mock Role

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection

    Returns:
        Model: Mock Role
    """
    model = models["Role"]
    # Create a New Mock Learning Style
    new_instance = model(
        role_name="teacher",
        is_enabled=True,
        user=mock_user,
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_adaptative_object(models: Dict[str, Model], db):
    """Fixture to create a mock Adaptative Object

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection

    Returns:
        Model: Mock Adaptative Object
    """
    model = models["AdaptativeObject"]
    # Create a New Mock Adaptative Object
    new_instance = model()
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_adaptative_event(models: Dict[str, Model], db, mock_adaptative_object):
    """Fixture to create a mock Adaptative Event

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection

    Returns:
        Model: Mock AdaptativeEvent
    """
    model = models["AdaptativeEvent"]
    # Create a New Mock Adaptative Event
    new_instance = model(
        triggered_change="HIGHLIGHT",
        relative_position=1,
        condition_aggregator="AND",
        adaptative_object=mock_adaptative_object,
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_adaptation_condition(models: Dict[str, Model], db, mock_adaptative_event):
    """Fixture to create a mock Adaptation Condition

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection

    Returns:
        Model: Mock AdaptationCondition
    """
    model = models["AdaptationCondition"]
    # Create a New Mock Adaptation Condition
    new_instance = model(
        value_to_compare=50,
        comparation_condition="lte",
        variable_to_compare="TOPIC_KNOWLEDGE",
        adaptative_event=mock_adaptative_event,
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_topic(models: Dict[str, Model], db):
    """Fixture to create a mock Topic

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection
    """
    model = models["Topic"]
    # Create a New Mock Topic
    new_instance = model(
        relative_position=1,
        title="Example Topic",
        icon_name="example-icon",
        default_knowledge=50,
        leak_parameter=0.5,
        adaptative_object=models["AdaptativeObject"](),
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_template(models: Dict[str, Model], db, mock_topic):
    """Fixture to create a mock Template

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection
    """
    model = models["Template"]
    # Create a New Mock Template
    new_instance = model(
        relative_position=1,
        title="Example Template",
        description="Example Description",
        image_url="https://example.com/image.png",
        default_knowledge=50,
        knowledge_weight=50,
        leak_parameter=0.5,
        adaptative_object=models["AdaptativeObject"](),
        topic=mock_topic,
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_page(models: Dict[str, Model], db, mock_template):
    """Fixture to create a mock Page

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection
    """
    model = models["Page"]
    # Create a New Mock Page
    new_instance = model(
        relative_position=1,
        template=mock_template,
        adaptative_object=models["AdaptativeObject"](),
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_learning_content(models: Dict[str, Model], db, mock_template):
    """Fixture to create mock Learning Content

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection
    """
    model = models["LearningContent"]
    # Create a New Mock Learning Content
    new_instance = model(
        title="Example Learning Content",
        content="Example Content",
        page=models["Page"](
            relative_position=2,
            template=mock_template,
            adaptative_object=models["AdaptativeObject"](),
        ),
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_measurable_interaction(models: Dict[str, Model], db, mock_learning_content):
    """Fixture to create mock Measurable Interaction

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection
    """
    model = models["MeasurableInteraction"]
    # Create a New Mock Measurable Interaction
    new_instance = model(
        interaction_weight=50,
        interaction_threshold=5,
        interaction_trigger="click",
        learning_style_attribute="VISUAL",
        learning_content=mock_learning_content,
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_interaction_fired(
    models: Dict[str, Model], db, mock_measurable_interaction, mock_user
):
    """Fixture to create mock Interaction Fired

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection
    """
    model = models["InteractionFired"]
    # Create a New Mock Interaction Fired
    new_instance = model(
        measurable_interaction=mock_measurable_interaction,
        user=mock_user,
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_practice_test(models: Dict[str, Model], db, mock_template):
    """Fixture to create mock Practice Test

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection
    """
    model = models["PracticeTest"]
    # Create a New Mock Practice Test
    new_instance = model(
        title="Example Practice Test",
        show_on_init=False,
        adaptation_weight=50,
        approval_score=1,
        total_score=1,
        page=models["Page"](
            relative_position=3,
            template=mock_template,
            adaptative_object=models["AdaptativeObject"](),
        ),
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_test_question(models: Dict[str, Model], db, mock_practice_test):
    """Fixture to create mock Practice Test Question

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection
    """
    model = models["TestQuestion"]
    # Create a New Mock Practice Test Question
    new_instance = model(
        question_type="simple_selection",
        question_prompt="Example Question Prompt",
        relative_position=1,
        question_score=1,
        question_hint="Example Hint",
        practice_test=mock_practice_test,
        adaptative_object=models["AdaptativeObject"](),
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_answer_alternative(models: Dict[str, Model], db, mock_test_question):
    """Fixture to create mock Answer Alternative

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection
    """
    model = models["AnswerAlternative"]
    # Create a New Mock Answer Alternative
    new_instance = model(
        alternative_text="Example Answer Text",
        is_correct=True,
        test_question=mock_test_question,
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_test_attempt(models: Dict[str, Model], db, mock_practice_test, mock_user):
    """Fixture to create mock Test Attempt

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection
    """
    model = models["TestAttempt"]
    # Create a New Mock Test Attempt
    new_instance = model(
        practice_test=mock_practice_test,
        user=mock_user,
        acquired_score=1,
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_question_answer(
    models: Dict[str, Model], db, mock_test_attempt, mock_test_question
):
    """Fixture to create mock Question Answer

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection
    """
    model = models["QuestionAnswer"]
    # Create a New Mock Question Answer
    new_instance = model(
        acquired_score=1,
        is_correct=True,
        test_attempt=mock_test_attempt,
        test_question=mock_test_question,
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance


@pytest.fixture(scope="session")
def mock_selected_answer_alternatives(
    models: Dict[str, Model], db, mock_question_answer, mock_answer_alternative
):
    """Fixture to create mock Selected Answer Alternative

    Args:
        models (Dict[str, Model]): Dictionary of all of the models
        db (DB): Database connection
    """
    model = models["SelectedAnswerAlternatives"]
    # Create a New Mock Selected Answer Alternative
    new_instance = model(
        question_answer=mock_question_answer,
        answer_alternative=mock_answer_alternative,
    )
    db.session.add(new_instance)
    db.session.commit()
    return new_instance
