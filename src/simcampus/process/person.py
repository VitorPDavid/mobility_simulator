from scipy.stats import norm, expon  # type: ignore

from simpy import Environment

from simcampus.simulation_types import DistributionParameter, Place

from numpy.random import Generator

MAX_MINUTES_IN_DAY = 1440.0


def change_occupation(occupation: dict[Place, int], old_place: Place, new_place: Place):
    occupation[old_place] -= 1
    occupation[new_place] += 1


def change_place(
    *_,
    rnd: Generator,
    actual_place: Place,
    places: list[Place],
    occupation: dict[Place, int],
    transition_probability: list[float],
    stay_data: dict[Place, DistributionParameter],
) -> tuple[Place, float]:
    """TODO: place of arrival needs to be obtained from data... using tprob from None is wrong"""
    new_place: Place = rnd.choice(places, size=1, p=transition_probability)[0]
    stay: float = expon.rvs(size=1, loc=stay_data[new_place].loc, scale=stay_data[new_place].scale)[0]

    change_occupation(occupation, actual_place, new_place)

    return new_place, stay


def get_arrival(arrival_parameter: DistributionParameter) -> float:
    # User arrival
    arrival: float = norm.rvs(size=1, loc=arrival_parameter.loc, scale=arrival_parameter.scale)[0]

    while arrival > 1440:
        arrival: float = norm.rvs(size=1, loc=arrival_parameter.loc, scale=arrival_parameter.scale)[0]

    return arrival


def get_departure(
    departure_parameter: DistributionParameter,
    arrival: float,
) -> float:
    departure: float = norm.rvs(size=1, loc=departure_parameter.loc, scale=departure_parameter.scale)[0]

    while departure < arrival:
        departure = norm.rvs(size=1, loc=departure_parameter.loc, scale=departure_parameter.scale)[0]

    if departure > MAX_MINUTES_IN_DAY:
        departure = MAX_MINUTES_IN_DAY

    return departure


def person(
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
):
    day = 1

    # Day loop
    while True:
        place: Place = None
        arrival = get_arrival(arrival_parameter)
        departure = get_departure(departure_parameter, arrival) + env.now

        yield env.timeout(arrival)

        place, stay = change_place(
            rnd=rnd,
            places=places,
            actual_place=place,
            stay_data=stay_data,
            occupation=occupation,
            transition_probability=transition_probability[place],
        )

        if verbose:
            print("[{:10.5f}]\tUser {:02d} arrived at {}".format(env.now, i, place))

        # Dinamica de jornada de trabalho
        while env.now + stay < departure:
            yield env.timeout(stay)

            place, stay = change_place(
                rnd=rnd,
                places=places,
                actual_place=place,
                stay_data=stay_data,
                occupation=occupation,
                transition_probability=transition_probability[place],
            )

            if verbose:
                print("[{:10.5f}]\tUser {:02d} switched to {}".format(env.now, i, place))

        # esperando momento de saida
        yield env.timeout(departure - env.now)

        change_occupation(occupation, place, None)
        if verbose:
            print("[{:10.5f}]\tUser {:02d} leaved".format(env.now, i))

        # esperando para o proximo dia
        yield env.timeout(day * 1440 - env.now)

        if verbose:
            print("[{:10.5f}]\tUser {:02d} day {} endded".format(env.now, i, day))

        day += 1
