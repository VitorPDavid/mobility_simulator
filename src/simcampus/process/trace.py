from io import TextIOWrapper
from simpy import Environment
import pandas as pd

from simcampus.contacts.get_group_contacts_data import get_group_contacts_data
from simcampus.contacts.get_person_contacts_data import get_person_contacts_data
from simcampus.simulation_types import Place
from simcampus.contacts.contacts_types import Contact


class Trace:
    def __init__(
        self,
        env: Environment,
        occupation: dict[Place, int],
        all_contacts: dict[int, list[Contact]],
        places: list[Place],
        verbose: bool = False,
    ) -> None:
        """
        Recebe as variaveis necessarias para gerar as informações globais de pessoas e adiciona esse
        observador a simulação
        """

        self.env = env
        self.occupation = occupation
        self.places = places
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

        with open("occupation", "w") as focp:
            with open("contacts.txt", "w") as fcontacts:
                while True:
                    yield self.env.timeout(step)

                    self.occupation_trace(focp)

                    if self.day_end():
                        self.contacts_trace(fcontacts)

    def occupation_trace(self, focp: TextIOWrapper):
        total = 0
        focp.write("{} ".format(self.env.now))
        print("{} ".format(self.env.now), end="")
        for place in self.places:
            if place is None:
                continue
            focp.write("{} ".format(self.occupation[place]))
            print("{} ".format(self.occupation[place]), end="")
            total += self.occupation[place]
        focp.write("{}\n".format(total))
        print("{}".format(total))

    def day_end(self):
        return int(self.env.now) % 1435 == 0

    def contacts_trace(self, fcontacts: TextIOWrapper):
        person_contacts_data = get_person_contacts_data(self.all_contacts)
        for contact_data in person_contacts_data:
            fcontacts.write(contact_data.__str__(self.verbose))

        self.groups_contacts_trace(fcontacts)

        for key in self.all_contacts:
            self.all_contacts[key] = []

    def groups_contacts_trace(self, fcontacts: TextIOWrapper):
        if self.verbose:
            fcontacts.write("\n\ngrupos:\n")

        (
            contacts_data, groups_list,
            contact_matrix, unique_contacts_matrix,
            frequency_matrix, unique_contacts_frequency_matrix,
            unique_contact_graph
        ) = get_group_contacts_data(self.all_contacts)

        for contact_data in contacts_data:
            fcontacts.write(contact_data.__str__(self.verbose))

        fcontacts.write("Matriz de Contatos Totais dos Grupos:\n")
        df = pd.DataFrame(
            contact_matrix, index=groups_list,
            columns=groups_list + ["total", "total com outros grupos"]
        )
        fcontacts.write(f"{df.to_string(index=True)}\n")

        fcontacts.write("\nMatriz de Contatos Unicos dos Grupos:\n")
        df = pd.DataFrame(
            unique_contacts_matrix, index=groups_list,
            columns=groups_list + ["total", "total com outros grupos"]
        )
        fcontacts.write(f"{df.to_string(index=True)}\n")

        fcontacts.write("\nMatriz de Frequencia de Contatos dos Grupos:\n")
        df = pd.DataFrame(frequency_matrix, index=groups_list, columns=groups_list)
        fcontacts.write(f"{df.to_string(index=True, float_format="%.3f")}\n")

        fcontacts.write("\nMatriz de Frequencia de Contatos Unicos dos Grupos:\n")
        df = pd.DataFrame(unique_contacts_frequency_matrix, index=groups_list, columns=groups_list)
        fcontacts.write(f"{df.to_string(index=True, float_format="%.3f")}\n")

        fcontacts.write(f"{unique_contact_graph}")

        fcontacts.write("\n\n\n")
