# -*- coding: utf-8 -*-
"""Module containing the Helper Function to construct a Bayesian Network of User Model Learning Style.

Returns:
    function: Function for constructing the users Learning Style Bayesian Network.
"""

from typing import Dict

from flask_sqlalchemy.model import Model


def learning_style_bayesian_network_constructor(
    models: Dict[str, Model], current_user
) -> Dict[str, float]:
    """Function to construct a Bayesian Network Structure of Learning Styles.

    Args:
        models (Dict[str,Model]): Dictionary containing all models defined in the Database.
        current_user (): Instance of the Currently Authenticated User
    """
    LEARNING_STYLES = ["VISUAL", "AURAL", "KINESTHETIC", "TEXTUAL"]
    vark_learning_style_values = current_user.learning_style
    # Define the Learning Style Values as Default Values dependent on the VARK Cuestionnaire
    learning_style_values = {
        "VISUAL": vark_learning_style_values.visual,
        "AURAL": vark_learning_style_values.aural,
        "KINESTHETIC": vark_learning_style_values.kinesthetic,
        "TEXTUAL": vark_learning_style_values.textual,
    }
    # To make the Bayesian Network work, all Learning Styles must have interactions.
    learning_style_interactions_found = {
        "VISUAL": False,
        "AURAL": False,
        "KINESTHETIC": False,
        "TEXTUAL": False,
    }
    for learning_style in LEARNING_STYLES:
        # A New "Bayesian Network" simulation is created for each Learning Style
        found_interactions = (
            models["InteractionFired"]
            .query.filter_by(user_id=current_user.id)
            .join(models["MeasurableInteraction"])
            .filter_by(learning_style_attribute=learning_style)
        ).all()
        if found_interactions:
            # If the Learning Style has interactions, then we set the corresponding flag to True
            learning_style_interactions_found[learning_style] = True
            # And we proceed to calculate the expected value for the Learning Style affinity

            # To calculate such expected value we follow the Noisy-OR formula
            expected_affinity = 1
            expected_affinity_modifier = 1
            for interaction in found_interactions:
                expected_affinity_modifier *= (
                    1 - interaction.measurable_interaction.interaction_weight / 100
                )
            # NOTE: In this case the Leaky parameter is set to 0, so there is no
            # default affinity for the Learning Style
            expected_affinity -= expected_affinity_modifier
            # We then set the expected value for the Learning Style
            learning_style_values[learning_style] = expected_affinity

            # This simulates a Shallow Bayesian Network, where the Learning Style
            # is the root node, and the interactions are the leaf nodes.

    # We check if all Learning Styles have interactions found.
    # If not we reset the Learning Styles Values to their defaults
    if not all(learning_style_interactions_found.values()):
        learning_style_values = {
            "VISUAL": vark_learning_style_values.visual,
            "AURAL": vark_learning_style_values.aural,
            "KINESTHETIC": vark_learning_style_values.kinesthetic,
            "TEXTUAL": vark_learning_style_values.textual,
        }

    # We normalize the Learning Style Values
    # NOTE: This is done because a Learning Style Value represents the affinity
    # of the user to that Learning Style, the meaning of the value is important only relative to the others,
    # so the sum of all Learning Style Values must be 1.
    learning_style_values_sum = sum(learning_style_values.values())
    for learning_style in LEARNING_STYLES:
        learning_style_values[learning_style] /= learning_style_values_sum

    return learning_style_values
