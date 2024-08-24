from .simulation_types import DistributionParameter, Place


def print_simulation_information(
    stay_data: dict[Place, DistributionParameter],
    transition_probability: dict[None | str, list[float]],
):
    for _, place_transitions in transition_probability.items():
        print(place_transitions)

    print(stay_data)
