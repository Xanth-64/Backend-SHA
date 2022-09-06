# -*- coding: utf-8 -*-
"""Module containing the Controller for Reading Triggered Adaptative Events by Topic ID.

Returns:
    function: Read Function for the Specific Model & Schema
"""
from typing import Dict
from firebase_admin import App
from flask import Blueprint
from flask_marshmallow.schema import Schema
from flask_sqlalchemy.model import Model
from src.services.utils.helpers.learning_style_bayesian_network_constructor.learning_style_bayesian_network_constructor import (
    learning_style_bayesian_network_constructor,
)
from src.services.utils.middleware.auth_middleware import auth_middleware
from src.services.utils.helpers.knowledge_bayesian_network_constructor.knowledge_bayesian_network_constructor import (
    knowledge_bayesian_network_constructor,
)


def get_triggered_adaptative_events_by_topic_controller_factory(
    models: Dict[str, Model],
    schemas: Dict[str, Schema],
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    """Creates a Function that Finds all of the adaptative events triggered by the current user for a specific topic.

    Args:
        models (Dict[str,Model]): Dictionary containing all models defined in the Database.
        schema (Dict[str,Schema]): Dictionary containing all schemas defined in the API.
        blueprint (Blueprint): Blueprint to contain the new route.
        expected_role (str): Expected Role String. Either teacher or student.
        firebase_app (App): Firebase App Instance.
        user_model (Model): User Model Instance.

    Returns:
        function: Read Function for the Specific Model & Schema.
    """

    @blueprint.route("/triggered_events/<string:uuid>", methods=["GET"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def get_triggered_adaptative_events_by_topic_controller(
        uuid: str, current_user=None
    ):
        """Function to get all of the triggered adaptative events by the current user for a specific topic.

        Args:
            uuid (str): Unique ID for the Model Instance.

        Returns:
            dict: Response dictionary containing the Triggered Adaptative Events.
        """
        topic = models["Topic"].query.filter_by(id=uuid).first()
        if not topic:
            return {
                "message": "Topic not found",
                "data": {"error": "TOPIC_NOT_FOUND", "message": "Topic not found"},
                "success": False,
            }, 400

        # Use Utility Function to Construct a Bayesian Network for User Model.
        knowledge_bayesian_network = knowledge_bayesian_network_constructor(
            models, current_user
        )
        learning_styles_values = learning_style_bayesian_network_constructor(
            models, current_user
        )
        print("Knowledge Information =>", knowledge_bayesian_network.nodes)
        print("Learning Styles =>", learning_styles_values)

        # Get all of the adaptative events for the topic.
        adaptative_events = topic.adaptative_object.adaptative_events.order_by(
            "relative_position"
        ).all()

        # Filter out the adaptative events that are not triggered by the user.
        triggered_adaptative_events = []
        for adaptative_event in adaptative_events:
            condition_met_array = []
            for condition in adaptative_event.adaptation_conditions:
                if condition.variable_to_compare == "TOPIC_KNOWLEDGE":
                    variable_to_compare = knowledge_bayesian_network.nodes[topic.id][
                        "expected_knowledge"
                    ]
                elif condition.variable_to_compare == "LEARNING_STYLE_AURAL_AFFINITY":
                    variable_to_compare = learning_styles_values["AURAL"]
                elif condition.variable_to_compare == "LEARNING_STYLE_VISUAL_AFFINITY":
                    variable_to_compare = learning_styles_values["VISUAL"]
                elif condition.variable_to_compare == "LEARNING_STYLE_READING_AFFINITY":
                    variable_to_compare = learning_styles_values["READING"]
                elif (
                    condition.variable_to_compare
                    == "LEARNING_STYLE_KINESTHETIC_AFFINITY"
                ):
                    variable_to_compare = learning_styles_values["KINESTHETIC"]
                condition_met_array.append(
                    variable_to_compare <= condition.value_to_compare / 100
                    if condition.comparation_condition == "lte"
                    else variable_to_compare >= condition.value_to_compare / 100
                )

            if adaptative_event.condition_aggregator == "AND" and all(
                condition_met_array
            ):
                triggered_adaptative_events.append(adaptative_event)
            elif adaptative_event.condition_aggregator == "OR" and any(
                condition_met_array
            ):
                triggered_adaptative_events.append(adaptative_event)
        return {
            "success": True,
            "data": schemas["AdaptativeEvent_CompleteSchema"]().dump(
                obj=triggered_adaptative_events, many=True
            ),
            "message": "Adaptative Events for Topic Retrieved Successfully",
        }, 200

    return get_triggered_adaptative_events_by_topic_controller
