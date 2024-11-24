"""
Comando para ajudar a executar varias possibilidades de determinado comando
salva os outputs em pastas separadas para cada linha de um arquivo de entrada e
executa cada linha X vezes de acordo com o parametro "repeat-count".

Parametros:
-o ou --output-dir, valor default "output"
-i ou --input-file, valor default "cases.txt"
-r ou --repeat-count, valor default 3
"""

import os
import re
from pathlib import PosixPath

from .create_args_options import create_args_options


if __name__ == "__main__":
    parser = create_args_options()

    # Read args from command line
    (options, _) = parser.parse_args()

    with open(options.input_file, "r") as cases_file:
        for index, case in enumerate(cases_file.readlines()):
            command_string = case.strip()

            population = re.search(r"-p (\d+)", command_string)[1]
            seed = re.search(r"-s (\d+)", command_string)[1]

            comand_name = f"population_{population}_seed_{seed}"

            output_path = PosixPath(options.output_dir)
            directory_path = output_path / comand_name / f"{options.repeat_count}"
            os.makedirs(directory_path, exist_ok=True)

            for case_redudance in range(options.repeat_count):
                os.system(f"{command_string} -o {directory_path}")
