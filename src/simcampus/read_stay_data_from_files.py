from pathlib import PosixPath
import pickle

from simcampus.simulation_types import DistributionParameter, Place


def read_stay_data_from_files(stay_data_file_path: PosixPath) -> dict[Place, DistributionParameter]:
    """
    Utilizando o caminho recebido como parametro para ler um arquivo contendo um conjunto
    de media e desvio padrão por lugar

    os dados devem estar no formato de um dicionario contendo que tem as chave como o identificador do lugar e
    os valores sendo um confunjo de informações para identificar uma função normal.

    tendo os dados a função intera sobre os possiveis lugares para formatar os dados da distribuição normal em
    uma forma melhor de ser utilizada no resto da simulação

    Args:
        stay_data_file_path (PosixPath): caminho para o arquivo pickle contendo as informações
        de tempo de permanencia por lugar

    Returns:
        dict[Place, DistributionParameter]: dicionario contendo os parametros da distribuição
        normal do tempo de estagia por lugar
    """

    with open(stay_data_file_path, "rb") as file:
        stay_data = {
            place: DistributionParameter(stay_values) for place, stay_values in (pickle.load(file))["staydist"].items()
        }

    return stay_data
