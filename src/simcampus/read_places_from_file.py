import os
from pathlib import PosixPath
import pickle

from simcampus.simulation_types import Place


def read_places_from_file(inputdir: str | PosixPath) -> list[Place]:
    places_filepath = os.path.join(inputdir, "places")

    with open(places_filepath, "rb") as file:
        places = pickle.load(file)

    return places
