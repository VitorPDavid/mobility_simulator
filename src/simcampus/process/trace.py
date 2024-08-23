from simpy import Environment

from simcampus.simulation_types import Place


class Trace:
    def __init__(
        self,
        env: Environment,
        occupation: dict[Place, int],
        places: list[Place],
    ) -> None:
        self.env = env
        self.occupation = occupation
        self.places = places

        self.action = env.process(self.run())

    def run(self):
        step = 5.0

        with open("occupation", "w") as focp:
            while True:
                yield self.env.timeout(step)
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
