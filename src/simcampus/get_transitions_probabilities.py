from simcampus.simulation_types import Place, Transitions


def get_transitions_probabilities(places: list[Place], transitions: Transitions) -> dict[None | str, list[float]]:
    transition_probability: dict[None | str, list[float]] = {}

    for place in places:
        # fout[place] = open(str(place), "w")
        transition_probability[place] = []
        total = sum(list(transitions[place].values()))
        for nextplace in places:
            if place != nextplace:
                transition_probability[place].append(transitions[place][nextplace] / total)
            else:
                transition_probability[place].append(0.0)
        print(transition_probability[place])

    return transition_probability
