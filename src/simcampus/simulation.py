from pathlib import PosixPath
from typing import Union
import numpy as np
import simpy
from numpy.random import default_rng

from .get_transitions_probabilities import get_transitions_probabilities
from .process import person, trace
from .read_data_from_files import read_data_from_files


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
    # isso é necessario ?
    np.random.seed(seed=seed)

    group_freq, group_param, transitions, stay_data, places = read_data_from_files(inputdir)

    # initialization
    env = simpy.Environment()
    focp = open("occupation", "w")

    occupation = {place: 0 for place in places}
    transition_probability = get_transitions_probabilities(places, transitions)

    print(stay_data)

    # groups
    groups = []
    groupprob = []
    aparam = {}
    dparam = {}
    for grp in group_freq:
        groups.append(grp)
        groupprob.append(group_freq[grp] / sum(list(group_freq.values())))  # amount in grp/total
        aparam[grp] = group_param[grp][0]
        dparam[grp] = group_param[grp][1]

    for i in range(population):
        env.process(
            person(
                env,
                rnd,
                i,
                occupation,
                places,
                groups,
                groupprob,
                aparam,
                dparam,
                stay_data,
                transition_probability,
                verbose,
            )
        )

    env.process(trace(env, occupation, places, focp))

    env.run(until=days * 1440)
