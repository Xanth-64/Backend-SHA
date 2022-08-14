# -*- coding: utf-8 -*-
from easygraph.classes.directed_graph import DiGraph
from firebase_admin import App
from flask import Blueprint, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy.exc import IntegrityError
from src.services.utils.middleware.auth_middleware import auth_middleware
from src.lib.exceptions.circular_exception import CircularException


def create_topic_prelations_controller_factory(
    db: SQLAlchemy,
    models: dict,
    topic_schema: Schema,
    blueprint: Blueprint,
    expected_role: str = None,
    firebase_app: App = None,
    user_model: Model = None,
):
    @blueprint.route("/prelations", methods=["POST"])
    @auth_middleware(
        expected_role=expected_role, firebase_app=firebase_app, user_model=user_model
    )
    def create_topic_prelations(current_user=None):
        """Controller function to Create a Prelation to Given Model.

        Returns:
            dict: Dictionary Containing the Model Instance with Its Prelation.
        """
        req_data = request.get_json()
        predecessor = models["Topic"].query.get(req_data.get("predecessor"))
        successor = models["Topic"].query.get(req_data.get("successor"))

        if predecessor is None:
            return {
                "success": False,
                "data": {
                    "error": "NOT_FOUND",
                    "message": "Predecessor Not Found",
                },
                "message": "Predecessor Not Found",
            }, 400
        if successor is None:
            return {
                "success": False,
                "data": {
                    "error": "NOT_FOUND",
                    "message": "Successor Not Found",
                },
                "message": "Successor Not Found",
            }, 400
        # Validate that No Circular Precedence Exists
        # Construct a Graph of the Precedence Relationships

        graph = DiGraph()
        # Add Nodes to Graph
        graph.add_nodes([topic.id for topic in models["Topic"].query.all()])
        graph.add_node(predecessor.id)
        graph.add_node(successor.id)

        # Add Edges to Graph
        graph.add_edges(
            [
                (relationship.predecessor, relationship.successor)
                for relationship in db.engine.execute(
                    models["TopicPrecedence"].select()
                ).all()
            ]
        )
        graph.add_edge(predecessor.id, successor.id)

        # Check if the Graph has a Directed Cycle using DFS from the Predecessor Node

        visited = set()
        finished = set()

        def dfs(node):
            print("Visiting Node", node)
            if node in finished:
                return
            if node in visited:
                raise CircularException("Circular Precedence Found")
            visited.add(node)
            for successor in graph.successors(node):
                dfs(successor)
            finished.add(node)

        try:
            dfs(predecessor.id)
        except CircularException:
            return {
                "success": False,
                "data": {
                    "error": "CIRCULAR_PRECEDENCE",
                    "message": "Circular Precedence Found",
                },
                "message": "Circular Precedence Found",
            }, 400

        predecessor.successors.append(successor)
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
            "message": "Model Data Created Successfully",
            "data": {
                "predecessor": topic_schema().dump(obj=predecessor, many=False),
                "successor": topic_schema().dump(obj=successor, many=False),
            },
        }, 200
