import os
from pathlib import PosixPath
import pickle
from simcampus.simulation_types import (
    DistributionParameter,
    GroupArrivelAndDerpartureParameters,
    GroupFrequency,
    GroupParameters,
)


def get_groups_probabilities(inputdir: str | PosixPath):
    wh_filepath = os.path.join(inputdir, "workhours")

    with open(wh_filepath, "rb") as file:
        data = pickle.load(file)
        groups_frequency: GroupFrequency = data["group_freq"]
        groups_parameters: GroupParameters = {
            group_key: GroupArrivelAndDerpartureParameters(group_values)
            for group_key, group_values in data["group_param"].items()
        }

    groups_ids: list[int] = []
    groups_probability: list[float] = []
    arrival_parameters: dict[int, DistributionParameter] = {}
    departure_parameters: dict[int, DistributionParameter] = {}

    total_group_values = sum(groups_frequency.values())
    for group_key, group_value in groups_frequency.items():
        groups_ids.append(group_key)
        groups_probability.append(group_value / total_group_values)
        arrival_parameters[group_key] = groups_parameters[group_key].arrivel
        departure_parameters[group_key] = groups_parameters[group_key].derparture

    return groups_ids, groups_probability, arrival_parameters, departure_parameters
