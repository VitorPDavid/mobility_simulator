from pathlib import PosixPath
from typing import Union
import numpy as np
import simpy
from numpy.random import default_rng

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

    group_freq, group_param, transitions, stay_data = read_data_from_files(inputdir)

    # initialization
    env = simpy.Environment()
    places = [None, "adm", "inf", "mul", "bib", "pos"]
    focp = open("occupation", "w")
    occupation = {}
    tprob = {}

    # transitions
    for place in places:
        occupation[place] = 0
        # fout[place] = open(str(place), "w")
        tprob[place] = []
        total = sum(list(transitions[place].values()))
        for nextplace in places:
            if place != nextplace:
                tprob[place].append(transitions[place][nextplace] / total)
            else:
                tprob[place].append(0.0)
        print(tprob[place])
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
            person(env, rnd, i, occupation, places, groups, groupprob, aparam, dparam, stay_data, tprob, verbose)
        )

    env.process(trace(env, occupation, places, focp))

    env.run(until=days * 1440)
