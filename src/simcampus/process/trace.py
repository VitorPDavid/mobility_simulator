from simpy import Environment

from simcampus.simulation_types import Place


def trace(env: Environment, occupation: dict[Place, int], places: list[Place]):
    step = 5.0

    with open("occupation", "w") as focp:
        while True:
            yield env.timeout(step)
            total = 0
            focp.write("{} ".format(env.now))
            print("{} ".format(env.now), end="")
            for place in places:
                if place is None:
                    continue
                focp.write("{} ".format(occupation[place]))
                print("{} ".format(occupation[place]), end="")
                total += occupation[place]
            focp.write("{}\n".format(total))
            print("{}".format(total))
