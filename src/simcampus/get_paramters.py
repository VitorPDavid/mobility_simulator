from optparse import Values

from simcampus.simulation_types import SimulationArgs


def get_paramters(options: Values) -> SimulationArgs:
    return {
        "inputdir": options.inputdir,
        "outputdir": options.outputdir,
        "days": options.days,
        "stay": options.stay,
        "population": options.population,
        "seed": options.seed,
        "verbose": options.verbose,
    }
