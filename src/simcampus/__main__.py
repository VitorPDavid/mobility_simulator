from .create_args_options import create_args_options
from .simulation import run_simulation
from .get_paramters import get_paramters


parser = create_args_options()
# Read args from command line
(options, _) = parser.parse_args()
print(options)
run_simulation(**get_paramters(options))
