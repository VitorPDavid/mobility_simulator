from io import TextIOWrapper
from itertools import chain
from pathlib import PosixPath
import pickle

import numpy as np
from simpy import Environment

from simcampus.contacts.create_contacts_graphs import create_contacts_graphs
from simcampus.contacts.contacts_types import Contact
from simcampus.contacts.get_person_contacts_data import get_person_contacts_data
from simcampus.simulation_types import Place, GroupIdentifier


class Trace:
    def __init__(
        self,
        output_path: PosixPath,
        env: Environment,
        occupation: dict[Place, int],
        all_contacts: dict[int, list[Contact]],
        places: list[Place],
        groups: list[GroupIdentifier],
        verbose: bool = False,
    ) -> None:
        """
        Recebe as variaveis necessarias para gerar as informações globais de pessoas e adiciona esse
        observador a simulação
        """

        self.env = env
        self.output_path = output_path
        self.occupation = occupation
        self.places = places
        self.groups = groups
        self.all_contacts = all_contacts
        self.verbose = verbose

        self.action = env.process(self.run())

    def run(self):
        """
        Enquanto a simulação estiver ocorrendo salva em uma arquivo e envia par aa saida padrão
        quantas pessoas estão ocupando cada local e o total de pessoas em todos os lugares a
        cada cinco minutos simulados
        """
        step = 5.0

        with open(self.output_path / "occupation.txt", "w") as focp:
            with open(self.output_path / "contacts.txt", "w") as fcontacts:
                while True:
                    yield self.env.timeout(step)

                    self.occupation_trace(focp)

                    if self.day_end():
                        self.contacts_trace(fcontacts)

                        for key in self.all_contacts:
                            self.all_contacts[key] = []

    def occupation_trace(self, focp: TextIOWrapper):
        total = 0
        focp.write("{} ".format(self.env.now))
        for place in self.places:
            if place is None:
                continue
            focp.write("{} ".format(self.occupation[place]))
            total += self.occupation[place]
        focp.write("{}\n".format(total))

    def day_end(self):
        return int(self.env.now) % 1435 == 0

    def contacts_trace(self, fcontacts: TextIOWrapper):
        with open(self.output_path / "all_contacts.pkl", "wb") as all_contacts_file:
            pickle.dump(self.all_contacts, all_contacts_file)

        person_contacts_data = get_person_contacts_data(self.all_contacts)
        for contact_data in person_contacts_data:
            fcontacts.write(contact_data.__str__(self.verbose))

        all_times = np.array(
            [
                contact.contact_duration
                for contact in {
                    contact
                    for contact in chain.from_iterable([contact_list for contact_list in self.all_contacts.values()])
                }
            ],
            dtype=np.float64,
        )

        fcontacts.write(f"tempo medio: {np.mean(all_times)}\n")

        create_contacts_graphs(self.output_path, self.all_contacts, self.places, self.groups, person_contacts_data)
