from create_args_options import create_args_options
from simcampus import run_simulation

if __name__ == "__main__":
    parser = create_args_options()

    # Read args from command line
    (options, _) = parser.parse_args()

    run_simulation(options)
