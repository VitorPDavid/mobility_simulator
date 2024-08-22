import os
from pathlib import PosixPath
import pickle
from simcampus.simulation_types import (
    DistributionParameter,
    GroupArrivelAndDerpartureParameters,
    GroupFrequency,
    GroupParameters,
)


def get_groups_probabilities(cluster_data_file_path: PosixPath) -> tuple[
    list[int],
    list[float],
    dict[int, DistributionParameter],
    dict[int, DistributionParameter],
]:
    """
    Utilizando o caminho recebido como parametro para ler um arquivo contendo:
     - quantidade total de participantes por grupo
     - dois conjuntos de media e desvio padrão por grupo

    os dados devem estar no formato de um dicionario contendo:
        - "group_freq" contendo um dicionario que tem as chaves como o identificador do grupo e tendo
        como valores a quantidade total de participantes do grupo
        - "group_param" contendo um dicionario que tem as chave como o identificador do grupo e
        os valores sendo uma lista contendo dois confunjos de informação para identificar uma função normal.
        O primeiro item da lista é uma tupla contendo a media e o desvio padrão que define a função normal das
        amostra do horario de chegada do pertecente ao grupo. A segunda contem as mesma informações de media e
        desvio padrão porem para as amostra do horario de saida da pessoa pertecente aquele grupo.

    tendo os dados a função intera sobre a lista de frequencia dos grupos para gerar uma lista com os identificadores,
    uma lista de probabilidade seguingo a conta: frequencia do grupo / (somatorio das frequencias), um dicionario com
    os parametros da curva normal de horario de chegada por grupo e um dicionario com os parametro da curva normal de
    horario de saida por grupo.

    Args:
        cluster_data_file_path (PosixPath): caminho para o arquivo picle contendo as informações de clusterização

    Returns:
        tuple[ list[int], list[float], dict[int, DistributionParameter], dict[int, DistributionParameter] ]:

        uma trupla contendo as seguintes variaves em cada index:
         0 lista contendo os identificadores dos grupos
         1 lista contendo as probabilidades de uma pessoa pertencer a cada grupo
         2 dicionario contendo os parametros da distribuição normal do horario de chegada de acordo com o grupos
         3 dicionario contendo os parametros da distribuição normal do horario de partida de acordo com o grupos
    """

    wh_filepath = os.path.join(cluster_data_file_path)

    with open(wh_filepath, "rb") as file:
        data = pickle.load(file)
        groups_frequency: GroupFrequency = data["group_freq"]
        groups_parameters: GroupParameters = {
            group_key: GroupArrivelAndDerpartureParameters(group_values)
            for group_key, group_values in data["group_param"].items()
        }

    groups_ids: list[int] = []
    groups_probability: list[float] = []
    arrival_parameters: dict[int, DistributionParameter] = {}
    departure_parameters: dict[int, DistributionParameter] = {}

    total_group_values = sum(groups_frequency.values())
    for group_key, group_value in groups_frequency.items():
        groups_ids.append(group_key)
        groups_probability.append(group_value / total_group_values)
        arrival_parameters[group_key] = groups_parameters[group_key].arrivel
        departure_parameters[group_key] = groups_parameters[group_key].derparture

    return groups_ids, groups_probability, arrival_parameters, departure_parameters
