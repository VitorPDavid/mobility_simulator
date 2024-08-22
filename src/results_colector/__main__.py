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
from .create_args_options import create_args_options


if __name__ == "__main__":
    parser = create_args_options()

    # Read args from command line
    (options, _) = parser.parse_args()

    with open(options.input_file, "r") as cases_file:
        for index, case in enumerate(cases_file.readlines()):
            command_string = case.strip()
            comand_name = f"execucao_{index}"

            os.makedirs(f"{options.output_dir}/{comand_name}", exist_ok=True)

            for case_redudance in range(options.repeat_count):
                file_name = f"{options.output_dir}/{comand_name}/repetition_{case_redudance}.txt"
                os.system(f"touch {file_name}")
                os.system(f"{command_string} > {file_name}")
