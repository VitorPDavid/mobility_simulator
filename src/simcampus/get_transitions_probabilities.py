from pathlib import PosixPath
import pickle
from simcampus.simulation_types import Place, Transitions


def get_transitions_probabilities(
    transitions_data_file_path: PosixPath,
    places: list[Place],
) -> dict[None | str, list[float]]:
    """
    Utilizando o caminho recebido como parametro para ler um arquivo contendo as informações de quantidade
    de pessoas que transicionaram de um local a outro.

    os dados devem estar no formato de um dicionario contendo uma chave "transitions" que tem como valor
    um dicionario que tem os identificadores de lugar como chaves e como valor outro dicionario contendo
    todos os demais lugares como chave e a quantidade total de pessoas que se moveram do primeiro local
    para o segundo local como valor.

    tendo os dados a função intera sobre a lista de lugares, places, e criar um dicionario que tem os identificadores
    de lugar como chaves e como valor outro dicionario contendo todos os demais lugares, other_place, como chave e a
    seguinte conta:
    transitions[place in places][other_place in places if other_place != place]
    /
    sum[transitions[place][i] for i in places] como valor.

    Args:
        transitions_data_file_path (PosixPath): caminho para o arquivo pickle contendo as informações de transitions
        places (list[Place]): uma lista contento os identificadores dos possives lugares

    Returns:
        dict[ None | str, list[float] ]:

        retorna um dicionario tendo as chaves igual ao identificadores dos lugares e os valores
        uma lista de proabilidade de troca para outro lugar
    """

    with open(transitions_data_file_path, "rb") as file:
        transitions: Transitions = (pickle.load(file))["transitions"]

    transition_probability: dict[None | str, list[float]] = {}

    for place in places:
        transition_probability[place] = []
        total = sum(transitions[place].values())

        transition_probability[place] = [
            (transitions[place][nextplace] / total) if place != nextplace else 0.0 for nextplace in places
        ]

    return transition_probability
