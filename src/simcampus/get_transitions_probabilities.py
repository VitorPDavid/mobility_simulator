import os
from pathlib import PosixPath
import pickle
from simcampus.simulation_types import Place, Transitions


def get_transitions_probabilities(inputdir: str | PosixPath, places: list[Place]) -> dict[None | str, list[float]]:
    transitions_filepath = os.path.join(inputdir, "transitions")
    with open(transitions_filepath, "rb") as file:
        transitions: Transitions = (pickle.load(file))["transitions"]

    transition_probability: dict[None | str, list[float]] = {}

    for place in places:
        transition_probability[place] = []
        total = sum(transitions[place].values())

        transition_probability[place] = [
            (transitions[place][nextplace] / total) if place != nextplace else 0.0 for nextplace in places
        ]

        print(transition_probability[place])

    return transition_probability
