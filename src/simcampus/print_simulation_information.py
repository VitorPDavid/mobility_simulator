from pathlib import PosixPath
from .simulation_types import DistributionParameter, Place


def print_simulation_information(
    output_path: PosixPath,
    seed: int | str,
    stay_data: dict[Place, DistributionParameter],
    transition_probability: dict[None | str, list[float]],
):
    with open(output_path / "output.txt", "w") as foutput:
        for _, place_transitions in transition_probability.items():
            foutput.write(f"{place_transitions}\n")

        foutput.write(f"{stay_data}\n")

        foutput.write(f"{seed}\n")
