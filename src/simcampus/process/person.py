from typing import Any

from scipy.stats import norm, expon  # type: ignore

from simpy import Environment

from simcampus.simulation_types import DistributionParameter, Place
from simcampus.contacts.contacts_types import Contact, ContactPerson

from numpy.random import Generator

MAX_MINUTES_IN_DAY = 1440.0


class Person:
    def __init__(
        self,
        env: Environment,
        random_generator: Generator,
        identifier: int,
        occupation: dict[Place, int],
        places: list[Place],
        arrival_parameter: DistributionParameter,
        departure_parameter: DistributionParameter,
        stay_data: dict[Place, DistributionParameter],
        transition_probability: dict[Place, list[float]],
        persons_per_place: dict[Place, set[ContactPerson]],
        all_contacts: dict[int, list[Contact]],
        contact_information: dict[int, ContactPerson],
        verbose: bool,
    ) -> None:
        """
        Recebe as variaveis necessarias para executar o comportamento de uma pessoa e adiciona essa pessoa
        a simulação

        Args:
            env (Environment): variavel de ambiente do simpy que mantem a simulação
            random_generator (Generator): gerador de numeros aleatorios configurado com a seed da simulação
            identifier (int): identificador de pessoa
            occupation (dict[Place, int]): variavel para manter de forma global o total de pessoas em cada lugar
            places (list[Place]): lista com identificadores dos lugares
            arrival_parameter (DistributionParameter): parametros da distribuição normal do tempo de chegada do grupo
            departure_parameter (DistributionParameter): parametros da distribuição normal do tempo de partida do grupo
            stay_data (dict[Place, DistributionParameter]):
                parametros da distribuição normal do tempo de permanencia nos lugares
            transition_probability (dict[Place, list[float]]):
                dicionario de probabilidade de mudança para os demais locais por local
            verbose (bool): se a simulação deve ser
        """
        self.env = env
        self.places = places
        self.stay_data = stay_data
        self.identifier = identifier
        self.occupation = occupation
        self.random_generator = random_generator
        self.arrival_parameter = arrival_parameter
        self.departure_parameter = departure_parameter
        self.transition_probability = transition_probability
        self.persons_per_place = persons_per_place
        self.all_contacts = all_contacts
        self.contact_information = contact_information
        self.verbose = verbose

        self.action = env.process(self.run())

    def run(self):
        """
        comportamento da pessoa durante a simulação
        primeiro configura os valores iniciais da pessoa de acordo com as distribuições normais recebidas

        depois espera o momento de chega, altera o local e altera as variaveis de acompanhamento da simulação

        então enquanto o tempo da saida não tiver sido alcançado (linha 21 da função) fica esperando o tempo
        de permanencia no local atual para trocar para outro local dentro

        quando o tempo de saida é alcançado ajusta as variaveis de aocmpanhamento da simulação e espera o proximo dia
        """
        day = 1

        # Day loop
        while True:
            place: Place = None
            self.set_arrival()
            self.set_departure()

            yield self.env.timeout(self.arrival)

            place, stay = self.change_to_random_place(
                actual_place=place,
                transition_probability=self.transition_probability[place],
            )

            if self.verbose:
                print("[{:10.5f}]\tUser {:02d} arrived at {}".format(self.env.now, self.identifier, place))

            # Dinamica de jornada de trabalho
            while self.env.now + stay < self.departure:
                yield self.env.timeout(stay)

                place, stay = self.change_to_random_place(
                    actual_place=place,
                    transition_probability=self.transition_probability[place],
                )

                if self.verbose:
                    print("[{:10.5f}]\tUser {:02d} switched to {}".format(self.env.now, self.identifier, place))

            # esperando momento de saida
            yield self.env.timeout(self.departure - self.env.now)

            self.change_place(place, None)
            if self.verbose:
                print("[{:10.5f}]\tUser {:02d} leaved".format(self.env.now, self.identifier))

            # esperando para o proximo dia
            yield self.env.timeout(day * 1440 - self.env.now)

            if self.verbose:
                print("[{:10.5f}]\tUser {:02d} day {} endded".format(self.env.now, self.identifier, day))

            day += 1

    def change_to_random_place(
        self,
        *_: Any,
        actual_place: Place,
        transition_probability: list[float],
    ) -> tuple[Place, float]:
        """
        recebe um local e a lista de probabilidade de transição para outro local e retonar o proximo local
        de acordo com esse local.

        Args:
            actual_place (Place): identificador do local atual
            transition_probability (list[float]): lista de probilidade do proximo local

        Returns:
            tuple[Place, float]: retorna uma tupla com o novo local e o tempo de permanencia nesse local
        """

        new_place: Place = self.random_generator.choice(self.places, size=1, p=transition_probability)[0]
        stay: float = expon.rvs(
            size=1,
            loc=self.stay_data[new_place].loc,
            scale=self.stay_data[new_place].scale,
            random_state=self.random_generator,
        )[0]

        self.change_place(actual_place, new_place)

        return new_place, stay

    def change_place(self, old_place: Place, new_place: Place):
        self.occupation[old_place] -= 1
        self.occupation[new_place] += 1

        contact_info = self.contact_information[self.identifier]

        self.persons_per_place[old_place].discard(contact_info)
        self.persons_per_place[new_place].add(contact_info)

        self.handle_contact(new_place)
        self.handle_contact_end(old_place)

    def handle_contact(self, new_place: Place):
        if new_place is None:
            return

        contact_idetifiers = self.persons_per_place[new_place]

        for contact_person in contact_idetifiers:
            if contact_person.identifier != self.identifier:
                contact = Contact(
                    new_place,
                    self.env.now,
                    self.contact_information[self.identifier],
                    self.contact_information[contact_person.identifier],
                )

                self.all_contacts[self.identifier].append(contact)
                self.all_contacts[contact_person.identifier].append(contact)

    def handle_contact_end(self, old_place: Place):
        if old_place is None:
            return

        for contact in self.all_contacts[self.identifier]:
            if contact.place == old_place and contact.end_time is None:
                contact.end_time = self.env.now

        contact_idetifiers = self.persons_per_place[old_place]
        for contact_person in contact_idetifiers:
            if contact_person.identifier == self.identifier:
                continue

            for contact in self.all_contacts[contact_person.identifier]:
                if contact.end_time is None and contact.has_person(self.identifier):
                    contact.end_time = self.env.now

    def set_arrival(
        self,
    ):
        """
        seta um horario de chegada valido de acordo com a distribuição normal cadastrada no objeto.
        """

        arrival: float = norm.rvs(
            size=1,
            loc=self.arrival_parameter.loc,
            scale=self.arrival_parameter.scale,
            random_state=self.random_generator,
        )[0]

        while arrival > 1440:
            arrival = norm.rvs(
                size=1,
                loc=self.arrival_parameter.loc,
                scale=self.arrival_parameter.scale,
                random_state=self.random_generator,
            )[0]

        self.arrival: float = arrival

    def set_departure(
        self,
    ):
        """
        seta um horario de saida valido de acordo com o horario de chegada a distribuição normal cadastrados no objeto.
        """

        departure: float = norm.rvs(
            size=1,
            loc=self.departure_parameter.loc,
            scale=self.departure_parameter.scale,
            random_state=self.random_generator,
        )[0]

        while departure < self.arrival:
            departure = norm.rvs(
                size=1,
                loc=self.departure_parameter.loc,
                scale=self.departure_parameter.scale,
                random_state=self.random_generator,
            )[0]

        if departure > MAX_MINUTES_IN_DAY:
            departure = MAX_MINUTES_IN_DAY

        self.departure: float = departure + self.env.now
