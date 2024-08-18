import os
from pathlib import PosixPath
import pickle
from typing import Union

from simcampus.simulation_types import GroupFrequency, GroupParameters, Stay, Transitions, Place


def read_data_from_files(
    inputdir: Union[str, PosixPath]
) -> tuple[GroupFrequency, GroupParameters, Transitions, Stay, list[Place]]:
    """read input data from files"""
    wh_filepath = os.path.join(inputdir, "workhours")
    transitions_filepath = os.path.join(inputdir, "transitions")
    stay_filepath = os.path.join(inputdir, "staydist")
    places_filepath = os.path.join(inputdir, "places")

    with open(wh_filepath, "rb") as file:
        data = pickle.load(file)
        group_freq = data["group_freq"]
        group_param = data["group_param"]

    with open(transitions_filepath, "rb") as file:
        transitions = (pickle.load(file))["transitions"]

    with open(stay_filepath, "rb") as file:
        stay_param = (pickle.load(file))["staydist"]

    with open(places_filepath, "rb") as file:
        places = pickle.load(file)

    return group_freq, group_param, transitions, stay_param, places
