from pathlib import PosixPath
import pickle

from simcampus.simulation_types import Place


def read_places_from_file(places_file_path: PosixPath) -> list[Place]:
    """
    utilizando o caminho passado retornar uma lista com os indentificadores de lugares

    Args:
        places_file_path (PosixPath): caminho para o arquivo pickle contendo os identificadores de lugares

    Returns:
        list[Place]: lista com todos os possiveis locais
    """

    with open(places_file_path, "rb") as file:
        places = pickle.load(file)

    return places
