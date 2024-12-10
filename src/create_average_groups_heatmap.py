from pathlib import PosixPath
from typing import Collection
import numpy as np
import os
import re
import pickle

from simcampus.contacts.create_contact_heatmap import create_contact_heatmap
from simcampus.contacts.contacts_types import Contact
from simcampus.contacts.get_group_contacts_data import __create_matrix_row


def find_average_contacts_in_subfolders(population_to_collect: str, groups: list[int], root_path: PosixPath):
    contacts_by_folder: dict[str, dict[str, list[int]]] = {}
    unique_contacts_by_folder: dict[str, dict[str, list[int]]] = {}

    folder_name_list = list(os.listdir(root_path))
    folder_name_list.sort()

    for folder_name in folder_name_list:
        file_path = os.path.join(root_path, folder_name, "1", "all_contacts.pkl")
        population_match = re.search(r"population_(\d+)", folder_name)
        if not population_match:
            continue
        folder_identifier = str(population_match.group(1))
        if folder_identifier != population_to_collect:
            continue

        if os.path.isfile(file_path):
            print(file_path)

            with open(file_path, "rb") as file:
                all_contacts = pickle.load(file)

            group_contacts: dict[int, Collection[Contact]] = {}
            for person, person_contacts in all_contacts.items():
                if len(person_contacts) > 0:
                    group = int(person_contacts[0].get_person(person).group)
                    group_contacts[group] = set([*group_contacts.get(group, set()), *person_contacts])

            groups_list: list[int] = [*groups]
            groups_list.sort()

            shape = (len(groups), len(groups))
            contact_matrix = np.zeros(shape)
            unique_contacts_matrix = np.zeros(shape)

            for index, group in enumerate(groups_list):
                contacts = group_contacts.get(group, [])

                unique_contacts_control: set[int] = set()
                unique_contacts: list[Contact] = []

                for contact in contacts:
                    if contact.persons_hash() not in unique_contacts_control:
                        unique_contacts.append(contact)
                        unique_contacts_control.add(contact.persons_hash())

                row = __create_matrix_row(index, groups_list, contacts)
                contact_matrix[index] = row

                row = __create_matrix_row(index, groups_list, unique_contacts)
                unique_contacts_matrix[index] = row

            if folder_identifier not in contacts_by_folder:
                contacts_by_folder[folder_identifier] = contact_matrix
                unique_contacts_by_folder[folder_identifier] = unique_contacts_matrix
            else:
                contacts_by_folder[folder_identifier] = contacts_by_folder[folder_identifier] + contact_matrix

                unique_contacts_by_folder[folder_identifier] = (
                    unique_contacts_by_folder[folder_identifier] + unique_contacts_matrix
                )

    contacts_by_folder = {key: value / 20 for key, value in contacts_by_folder.items()}
    unique_contacts_by_folder = {key: value / 20 for key, value in unique_contacts_by_folder.items()}

    return contacts_by_folder, unique_contacts_by_folder


if __name__ == "__main__":
    path = PosixPath(os.path.abspath(__file__)).parent.parent

    with open(path / "data/workhours", "rb") as file:
        data = pickle.load(file)
        groups_data = [int(key) for key in data["group_freq"].keys()]
        groups_data.sort()

    population = "400"

    contacts_by_folder, unique_contacts_by_folder = find_average_contacts_in_subfolders(
        population, groups_data, path / "output"
    )

    create_contact_heatmap(
        groups_data,
        contacts_by_folder[population],
        f"Mapa de Calor de Contatos Entre Grupos \n para o tamanho de população de {population}",
        path / f"groups_contacts_heatmap_with_{population}",
        dtype=np.float64,
    )
    create_contact_heatmap(
        groups_data,
        unique_contacts_by_folder[population],
        f"Mapa de Calor de Contatos Unicos Entre Grupos \n para o tamanho de população de {population}",
        path / f"groups_unique_contacts_heatmap_with_{population}",
        dtype=np.float64,
    )
