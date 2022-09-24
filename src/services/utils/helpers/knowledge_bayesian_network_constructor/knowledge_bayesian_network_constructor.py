# -*- coding: utf-8 -*-
"""Module containing the Helper Function to construct a Bayesian Network Structure of User Model Knowledge.

Returns:
    function: Function for constructing the users Knowledge Bayesian Network.
"""

from typing import Dict

from easygraph.classes.directed_graph import DiGraph
from flask_sqlalchemy.model import Model


def knowledge_bayesian_network_constructor(
    models: Dict[str, Model], current_user
) -> DiGraph:
    """Function to construct a Bayesian Network Structure of User Model Knowledge.

    Args:
        models (Dict[str,Model]): Dictionary containing all models defined in the Database.
        current_user (): Instance of the Currently Authenticated User
    """
    # Get all of the Domain Model Topics.
    domain_model_topics = models["Topic"].query.all()

    # Get all of the Topic Precedence Relations.
    topic_precedence_relations = models["TopicPrecedence"].query.all()

    # Construct a Directed Graph of the Topics.
    bayesian_network = DiGraph()

    # Create an Auxiliary Dictionary to store the Edges.
    edges = {}
    # Add all of the Topics as Nodes.
    for topic in domain_model_topics:
        bayesian_network.add_node(
            topic.id,
            **{
                "default_knowledge": topic.default_knowledge,
                "leak_parameter": topic.leak_parameter / 100,
                "entity_type": "topic",
            }
        )

    # Add all of the Topic Precedence Relations as Edges.
    # NOTE: We add the Edges in the Reverse Direction to the Graph.
    # Because in a Bayesian Network of Knowdlege, the Successor is the Cause and the
    # Predecessor is the logical Effect.
    for relation in topic_precedence_relations:
        bayesian_network.add_edge(
            relation.predecessor_id,
            relation.successor_id,
            **{
                "knowledge_weight": relation.knowledge_weight,
            }
        )
        edges[
            (relation.predecessor_id, relation.successor_id)
        ] = relation.knowledge_weight

    # Get all of the Templates.
    templates = models["Template"].query.all()

    # Add all of the Templates as Nodes and all Template -> Topic Relationships.
    for template in templates:
        bayesian_network.add_node(
            template.id,
            **{
                "default_knowledge": template.default_knowledge,
                "leak_parameter": template.leak_parameter / 100,
                "entity_type": "template",
            }
        )
        bayesian_network.add_edge(
            template.id,
            template.topic_id,
            **{
                "knowledge_weight": template.knowledge_weight,
            }
        )
        edges[(template.id, template.topic_id)] = template.knowledge_weight

    # Get all of the Pages.
    pages = models["Page"].query.all()

    # Add all of the Pages as Nodes and all Page -> Template Relationships.
    # NOTE: Pages must be differentiated between Practice Tests and Learning Content Interactions
    for page in pages:
        if page.practice_test:
            # We Check if the user has attempted the Practice Test
            test_attempt = page.practice_test.test_attempts.filter_by(
                user_id=current_user.id
            ).first()
            # We add the practice test. Setting the evidence_observed flag as True
            # only if the user passed the test.
            bayesian_network.add_node(
                page.id,
                **{
                    "evidence_observed": (
                        test_attempt.acquired_score >= page.practice_test.approval_score
                    )
                    if test_attempt
                    else False,
                    "entity_type": "practice_test",
                }
            )
            # We add the edge between the practice test and the template.
            bayesian_network.add_edge(
                page.id,
                page.template_id,
                **{
                    "knowledge_weight": page.practice_test.adaptation_weight,
                }
            )
            edges[(page.id, page.template_id)] = page.practice_test.adaptation_weight

        if page.learning_content:
            # We Check if the user has attempted any Learning Content Interaction
            # NOTE: We filter the Learning Content Interactions so that we only get
            # the ones that are not related to learning styles.
            interactions_fired = (
                page.learning_content.measurable_interactions.filter_by(
                    learning_style_attribute=None
                )
                .join(models["InteractionFired"], aliased=True)
                .filter_by(user_id=current_user.id)
            )
            interactions_not_fired = (
                page.learning_content.measurable_interactions.except_(
                    interactions_fired
                )
            )
            # We add the learning content. Setting the evidence_observed flag as True only
            # if the user triggered the interaction.
            for interaction in interactions_fired.all():
                bayesian_network.add_node(
                    interaction.id,
                    **{
                        "evidence_observed": True,
                        "entity_type": "interaction",
                    }
                )
                # We add the edge between the interaction and the template.
                bayesian_network.add_edge(
                    interaction.id,
                    page.template_id,
                    **{
                        "knowledge_weight": interaction.interaction_weight,
                    }
                )
                edges[
                    (interaction.id, page.template_id)
                ] = interaction.interaction_weight

            for interaction in interactions_not_fired.all():
                bayesian_network.add_node(
                    interaction.id,
                    **{
                        "evidence_observed": False,
                        "entity_type": "interaction",
                    }
                )
                # We add the edge between the interaction and the template.
                bayesian_network.add_edge(
                    interaction.id,
                    page.template_id,
                    **{
                        "knowledge_weight": interaction.interaction_weight,
                    }
                )
                edges[
                    (interaction.id, page.template_id)
                ] = interaction.interaction_weight

    # print("Edges", bayesian_network.edges)
    # print("Nodes", bayesian_network.nodes)
    # print("Auxiliary Edges", edges)
    # Now we Estimate the Expected Knowledge for each Template.

    # For estimation we use Leaky OR Model.

    # We iterate over all of the Templates.
    for template in templates:
        # For each template we get its predecessors.
        predecessors = bayesian_network.predecessors(template.id)
        # print("Reading Template", template.id)
        # We initialize the expected knowledge of the template.
        expected_knowledge = 1

        # We Initialize the Noisy OR expected_knowledge modifier
        expected_knowledge_modifier = 1

        # We iterate over all of the predecessors.
        for predecessor in predecessors:
            # print("Predecessor: ", bayesian_network.nodes[predecessor])
            # We take the node into account only if it's evidence_observed flag is True.
            if bayesian_network.nodes[predecessor]["evidence_observed"]:
                # We calculate the expected_knowledge_modifier.
                # print("Evidence Observed! => ", edges[(predecessor, template.id)])
                expected_knowledge_modifier *= 1 - (
                    edges[(predecessor, template.id)] / 100
                )
        expected_knowledge_modifier *= 1 - template.leak_parameter / 100
        expected_knowledge -= expected_knowledge_modifier

        # Now we set the node's expected_knowledge attribute.
        bayesian_network.nodes[template.id]["expected_knowledge"] = expected_knowledge

        # And we set the node's evidence_observed attribute.
        # NOTE: We set it to True only if the expected_knowledge is greater than the default_knowledge.
        bayesian_network.nodes[template.id]["evidence_observed"] = (
            bayesian_network.nodes[template.id]["expected_knowledge"]
            > bayesian_network.nodes[template.id]["default_knowledge"] / 100
        )

    # Now we Estimate the Expected Knowledge for each Topic.

    # For estimation we use Leaky OR Model.

    # We create a list of Topics to be updated.
    topics_to_update = []

    # We iterate over all of the Topics.
    for topic in domain_model_topics:
        # We add the topic to the list of topics to be updated
        # if the topic has no successors.
        if not topic.predecessors:
            topics_to_update.append(topic)
    # print("Initial Topic to Update", topics_to_update)
    # Now we iterate until we have no more topics to update.
    while topics_to_update:
        topic_to_update = topics_to_update.pop(0)
        print("Updating Topic", topic_to_update.id)
        # We get the topic's predecessors.
        predecessors = bayesian_network.predecessors(topic_to_update.id)

        # We initialize the expected knowledge of the topic.
        expected_knowledge = 1

        # We Initialize the Noisy OR expected_knowledge modifier
        expected_knowledge_modifier = 1

        # We iterate over all of the predecessors.
        for predecessor in predecessors:
            print("Working on Predecessor => ", predecessor)
            # We take the node into account only if it's evidence_observed flag is True.
            if bayesian_network.nodes[predecessor]["evidence_observed"]:
                # We calculate the expected_knowledge_modifier.
                expected_knowledge_modifier *= 1 - (
                    edges[(predecessor, topic_to_update.id)] / 100
                )
        expected_knowledge_modifier *= 1 - topic_to_update.leak_parameter / 100
        expected_knowledge -= expected_knowledge_modifier
        # Now we set the node's expected_knowledge attribute.
        bayesian_network.nodes[topic_to_update.id][
            "expected_knowledge"
        ] = expected_knowledge

        # And we set the node's evidence_observed attribute.
        # NOTE: We set it to True only if the expected_knowledge is greater than the default_knowledge.
        bayesian_network.nodes[topic_to_update.id]["evidence_observed"] = (
            bayesian_network.nodes[topic_to_update.id]["expected_knowledge"]
            > bayesian_network.nodes[topic_to_update.id]["default_knowledge"] / 100
        )

        # Now we add the topic's successors to the list of topics to be updated.
        # NOTE: We only add the successors if they have no predecessors that are not yet updated.
        for successor in bayesian_network.successors(topic_to_update.id):
            add_successor = True
            for predecessor in bayesian_network.predecessors(successor):
                if (
                    bayesian_network.nodes[predecessor].get("expected_knowledge")
                    is None
                ):
                    add_successor = False
                    break
            if add_successor:
                print("Appending:", models["Topic"].query.get(successor))
                topics_to_update.append(models["Topic"].query.get(successor))
    # print("Final Node List => ", bayesian_network.nodes)
    return bayesian_network
