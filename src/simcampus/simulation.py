from pathlib import PosixPath
from typing import Union
import numpy as np
import simpy
from numpy.random import default_rng

from .get_groups_probabilities import get_groups_probabilities
from .get_transitions_probabilities import get_transitions_probabilities
from .process import person, trace
from .read_stay_data_from_files import read_stay_data_from_files
from .read_places_from_file import read_places_from_file


def run_simulation(
    *_: None,
    inputdir: Union[str, PosixPath] = "data",
    days: int = 7,
    stay: float = 10.0,
    population: int = 10,
    seed: int = 1,
    verbose: bool = False,
):
    rnd = default_rng(seed)
    np.random.seed(seed=seed)  # configura seed para as funções de norm e expo

    env = simpy.Environment()

    input_path = PosixPath(inputdir)

    (
        groups_ids,
        groups_probability,
        arrival_parameters,
        departure_parameters,
    ) = get_groups_probabilities(input_path / "workhours")
    places = read_places_from_file(inputdir)
    occupation = {place: 0 for place in places}
    transition_probability = get_transitions_probabilities(inputdir, places)
    stay_data = read_stay_data_from_files(inputdir)

    for i in range(population):
        group: int = rnd.choice(groups_ids, p=groups_probability, size=1)[0]
        arrival_parameter = arrival_parameters[group]
        departure_parameter = departure_parameters[group]

        env.process(
            person(
                env,
                rnd,
                i,
                occupation,
                places,
                arrival_parameter,
                departure_parameter,
                stay_data,
                transition_probability,
                verbose,
            )
        )

    env.process(trace(env, occupation, places))

    env.run(until=days * 1440)
