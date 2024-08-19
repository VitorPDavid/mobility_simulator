import os
from pathlib import PosixPath
import pickle

from simcampus.simulation_types import DistributionParameter, Place


def read_stay_data_from_files(inputdir: str | PosixPath) -> dict[Place, DistributionParameter]:
    stay_filepath = os.path.join(inputdir, "staydist")

    with open(stay_filepath, "rb") as file:
        stay_data = {
            stay_key: DistributionParameter(stay_values)
            for stay_key, stay_values in (pickle.load(file))["staydist"].items()
        }

    print(stay_data)

    return stay_data
