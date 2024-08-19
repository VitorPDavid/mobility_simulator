from scipy.stats import norm, expon  # type: ignore

from simpy import Environment

from simcampus.simulation_types import DistributionParameter, Place

from numpy.random import Generator


# individual behavior
def person(
    env: Environment,
    rnd: Generator,
    i: int,
    occupation: dict[Place, int],
    places: list[Place],
    groups_ids: list[int],
    groups_probability: list[float],
    arrival_parameters: dict[int, DistributionParameter],
    departure_parameters: dict[int, DistributionParameter],
    stay_data: dict[Place, DistributionParameter],
    transition_probability: dict[Place, list[float]],
    verbose: bool,
):
    grp: int = rnd.choice(groups_ids, p=groups_probability, size=1)[0]  # choose a group
    place: Place = None
    occupation[place] += 1
    day = 1

    arrival_parameter = arrival_parameters[grp]
    departure_parameter = departure_parameters[grp]

    # Day loop
    while True:
        # User arrival
        arrival: float = norm.rvs(size=1, loc=arrival_parameter.loc, scale=arrival_parameter.scale)[0]
        departure: float = norm.rvs(size=1, loc=departure_parameter.loc, scale=departure_parameter.scale)[0]

        while departure < arrival:
            departure = norm.rvs(
                size=1,
                loc=departure_parameter.loc,
                scale=departure_parameter.scale,
            )[0]

        if departure > 1440:
            departure = 1440.0

        departure += env.now

        yield env.timeout(arrival)
        occupation[place] -= 1

        # TODO: place of arrival needs to be obtained from data... using tprob from None is wrong
        place = rnd.choice(places, p=transition_probability[place], size=1)[0]

        stay = expon.rvs(size=1, loc=stay_data[place].loc, scale=stay_data[place].scale)[0]

        occupation[place] += 1
        if verbose:
            print("[{:10.5f}]\tUser {:02d} arrived at {}".format(env.now, i, place))

        # Dinamica de jornada de trabalho
        while env.now + stay < departure:
            yield env.timeout(stay)
            occupation[place] -= 1
            place = rnd.choice(places, size=1, p=transition_probability[place])[0]
            occupation[place] += 1
            if verbose:
                print("[{:10.5f}]\tUser {:02d} switched to {}".format(env.now, i, place))

            stay = expon.rvs(size=1, loc=stay_data[place].loc, scale=stay_data[place].scale)[0]

        yield env.timeout(departure - env.now)

        occupation[place] -= 1
        place = None
        occupation[place] += 1

        if verbose:
            print("[{:10.5f}]\tUser {:02d} leaved".format(env.now, i))

        yield env.timeout(day * 1440 - env.now)

        if verbose:
            print("[{:10.5f}]\tUser {:02d} day {} endded".format(env.now, i, day))

        day += 1
