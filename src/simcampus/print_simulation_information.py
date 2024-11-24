from io import TextIOWrapper
from .simulation_types import DistributionParameter, Place


def print_simulation_information(
    foutput: TextIOWrapper,
    seed: int | str,
    stay_data: dict[Place, DistributionParameter],
    transition_probability: dict[None | str, list[float]],
):
    for _, place_transitions in transition_probability.items():
        foutput.write(f"{place_transitions}\n")

    foutput.write(f"{stay_data}\n")

    foutput.write(f"{seed}\n")
