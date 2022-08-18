# -*- coding: utf-8 -*-
from typing import Dict
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
        # Validate that Relationship Does not yet Exist
        if successor.id in [
            relationship.successor_id for relationship in predecessor.successors
        ]:
            return {
                "success": False,
                "data": {
                    "error": "ALREADY_EXISTS",
                    "message": "Relationship Already Exists",
                },
                "message": "Relationship Already Exists",
            }, 400

        # Validate that No Circular Precedence Exists and that No Path Between the Two Topics Exists
        # Construct a Graph of the Precedence Relationships

        graph = DiGraph()
        # Add Nodes to Graph
        graph.add_nodes([topic.id for topic in models["Topic"].query.all()])
        graph.add_node(predecessor.id)
        graph.add_node(successor.id)

        # Add Edges to Graph
        graph.add_edges(
            [
                (relationship.predecessor_id, relationship.successor_id)
                for relationship in models["TopicPrecedence"].query.all()
            ]
        )

        # Check that No Path exists between the Two Topics

        def dfs_pathfinder(start_node, objective_node):
            if start_node == objective_node:
                return True
            for successor in graph.successors(start_node):
                if dfs_pathfinder(successor, objective_node):
                    return True
            return False

        if dfs_pathfinder(predecessor.id, successor.id):
            return {
                "success": False,
                "data": {
                    "error": "PATH_EXISTS",
                    "message": "Path Between Nodes Already Exists",
                },
                "message": "Path Between Nodes Already Exists",
            }, 400

        # Check if the Graph has a Directed Cycle using DFS from the Predecessor Node
        graph.add_edge(predecessor.id, successor.id)

        visited = set()
        finished = set()

        def dfs_validate_circular(node):
            if node in finished:
                return
            if node in visited:
                raise CircularException("Circular Precedence Found")
            visited.add(node)
            for successor in graph.successors(node):
                dfs_validate_circular(successor)
            finished.add(node)

        try:
            dfs_validate_circular(predecessor.id)
        except CircularException:
            return {
                "success": False,
                "data": {
                    "error": "CIRCULAR_PRECEDENCE",
                    "message": "Circular Precedence Found",
                },
                "message": "Circular Precedence Found",
            }, 400

        # Create the Precedence Relationship
        precedence = models["TopicPrecedence"](
            knowledge_weight=req_data.get("knowledge_weight"),
            predecessor_id=predecessor.id,
            successor_id=successor.id,
        )

        predecessor.successors.append(precedence)
        successor.predecessors.append(precedence)
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
                "predecessor": schemas["Topic_DefaultSchema"]().dump(
                    obj=predecessor, many=False
                ),
                "successor": schemas["Topic_DefaultSchema"]().dump(
                    obj=successor, many=False
                ),
                "precedences": schemas["TopicPrecedence_DefaultSchema"]().dump(
                    obj=precedence, many=False
                ),
            },
        }, 200
