from typing import Any
from scipy.stats import norm, expon  # type: ignore

from simpy import Environment

from simcampus.simulation_types import DistributionParameter, Place

from numpy.random import Generator

MAX_MINUTES_IN_DAY = 1440.0


class Person:
    def __init__(
        self,
        env: Environment,
        rnd: Generator,
        i: int,
        occupation: dict[Place, int],
        places: list[Place],
        arrival_parameter: DistributionParameter,
        departure_parameter: DistributionParameter,
        stay_data: dict[Place, DistributionParameter],
        transition_probability: dict[Place, list[float]],
        verbose: bool,
    ) -> None:
        self.env = env
        self.rnd = rnd
        self.i = i
        self.occupation = occupation
        self.places = places
        self.arrival_parameter = arrival_parameter
        self.departure_parameter = departure_parameter
        self.stay_data = stay_data
        self.transition_probability = transition_probability
        self.verbose = verbose

        self.action = env.process(self.run())

    def run(self):
        day = 1

        # Day loop
        while True:
            place: Place = None
            arrival = self.get_arrival()
            departure = self.get_departure(arrival) + self.env.now

            yield self.env.timeout(arrival)

            place, stay = self.change_place(
                actual_place=place,
                transition_probability=self.transition_probability[place],
            )

            if self.verbose:
                print("[{:10.5f}]\tUser {:02d} arrived at {}".format(self.env.now, self.i, place))

            # Dinamica de jornada de trabalho
            while self.env.now + stay < departure:
                yield self.env.timeout(stay)

                place, stay = self.change_place(
                    actual_place=place,
                    transition_probability=self.transition_probability[place],
                )

                if self.verbose:
                    print("[{:10.5f}]\tUser {:02d} switched to {}".format(self.env.now, self.i, place))

            # esperando momento de saida
            yield self.env.timeout(departure - self.env.now)

            self.change_occupation(place, None)
            if self.verbose:
                print("[{:10.5f}]\tUser {:02d} leaved".format(self.env.now, self.i))

            # esperando para o proximo dia
            yield self.env.timeout(day * 1440 - self.env.now)

            if self.verbose:
                print("[{:10.5f}]\tUser {:02d} day {} endded".format(self.env.now, self.i, day))

            day += 1

    def change_occupation(self, old_place: Place, new_place: Place):
        self.occupation[old_place] -= 1
        self.occupation[new_place] += 1

    def change_place(
        self,
        *_: Any,
        actual_place: Place,
        transition_probability: list[float],
    ) -> tuple[Place, float]:
        """TODO: place of arrival needs to be obtained from data... using tprob from None is wrong"""
        new_place: Place = self.rnd.choice(self.places, size=1, p=transition_probability)[0]
        stay: float = expon.rvs(size=1, loc=self.stay_data[new_place].loc, scale=self.stay_data[new_place].scale)[0]

        self.change_occupation(actual_place, new_place)

        return new_place, stay

    def get_arrival(
        self,
    ) -> float:
        # User arrival
        arrival: float = norm.rvs(size=1, loc=self.arrival_parameter.loc, scale=self.arrival_parameter.scale)[0]

        while arrival > 1440:
            arrival: float = norm.rvs(size=1, loc=self.arrival_parameter.loc, scale=self.arrival_parameter.scale)[0]

        return arrival

    def get_departure(
        self,
        arrival: float,
    ) -> float:
        departure: float = norm.rvs(size=1, loc=self.departure_parameter.loc, scale=self.departure_parameter.scale)[0]

        while departure < arrival:
            departure = norm.rvs(size=1, loc=self.departure_parameter.loc, scale=self.departure_parameter.scale)[0]

        if departure > MAX_MINUTES_IN_DAY:
            departure = MAX_MINUTES_IN_DAY

        return departure
