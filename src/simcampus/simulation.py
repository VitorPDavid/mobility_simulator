import os
from pathlib import PosixPath
from typing import Union
import numpy as np
import simpy
from numpy.random import default_rng


from .get_groups_probabilities import get_groups_probabilities
from .get_transitions_probabilities import get_transitions_probabilities
from .process import Trace, Person
from .read_stay_data_from_files import read_stay_data_from_files
from .read_places_from_file import read_places_from_file
from .print_simulation_information import print_simulation_information
from .contacts.contacts_types import Contact, ContactPerson
from .simulation_types import Place


def run_simulation(
    *_: None,
    inputdir: Union[str, PosixPath] = "data",
    outputdir: Union[str, PosixPath] = "output",
    days: int = 7,
    stay: float = 10.0,
    population: int = 10,
    seed: int = 1,
    verbose: bool = False,
):
    rnd = default_rng(seed)

    input_path = PosixPath(inputdir)
    (
        groups_ids,
        groups_probability,
        arrival_parameters,
        departure_parameters,
    ) = get_groups_probabilities(input_path / "workhours")
    places = read_places_from_file(input_path / "places")
    transition_probability = get_transitions_probabilities(input_path / "transitions", places)
    stay_data = read_stay_data_from_files(input_path / "staydist")

    output_path = PosixPath(outputdir)
    os.makedirs(output_path, exist_ok=True)
    print_simulation_information(output_path, seed, stay_data, transition_probability)

    env = simpy.Environment()
    occupation = {place: 0 for place in places}
    contact_information: dict[int, ContactPerson] = {}
    all_contacts: dict[int, list[Contact]] = {}
    persons_per_place: dict[Place, set[ContactPerson]] = {place: set() for place in places}

    for i in range(population):
        group: int = rnd.choice(groups_ids, p=groups_probability, size=1)[0]
        arrival_parameter = arrival_parameters[group]
        departure_parameter = departure_parameters[group]

        contact_information[i] = ContactPerson(i, group)
        all_contacts[i] = []

        Person(
            env,
            rnd,
            i,
            occupation,
            places,
            arrival_parameter,
            departure_parameter,
            stay_data,
            transition_probability,
            persons_per_place,
            all_contacts,
            contact_information,
            verbose,
        )

    Trace(output_path, env, occupation, all_contacts, places, verbose)

    env.run(until=days * 1440)
