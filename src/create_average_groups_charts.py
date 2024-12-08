from pathlib import PosixPath
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import pickle
from scipy.stats import sem

from simcampus.contacts.get_group_contacts_data import get_group_contacts_data


def calculate_means_and_plot(data):
    for population, groups_data in data.items():
        groups = []
        means = []
        confidence_intervals = []
        for group, group_data in groups_data.items():
            mean_time = np.mean(group_data)
            standard_error = sem(group_data)
            confidence_interval = 1.96 * standard_error

            groups.append(group)
            means.append(mean_time)
            confidence_intervals.append(confidence_interval)

        fig = plt.figure(figsize=(10, 6))
        plt.bar(groups, means, yerr=confidence_intervals, capsize=5, alpha=0.7, color="b")

        plt.xlabel("Grupos")
        plt.ylabel("Media de Contatos do Grupo")

        plt.xticks(rotation=45)
        plt.tight_layout()

        fig.savefig(
            f"/home/vitorpdavid/codigos/mobility_simulator/group_contact_mean_with_{population}_persons",
            bbox_inches="tight",
        )
        plt.close(fig)


def calculate_unique_means_and_plot(data):
    for population, groups_data in data.items():
        groups = []
        means = []
        confidence_intervals = []
        for group, group_data in groups_data.items():
            mean_time = np.mean(group_data)
            standard_error = sem(group_data)
            confidence_interval = 1.96 * standard_error

            groups.append(group)
            means.append(mean_time)
            confidence_intervals.append(confidence_interval)

        fig = plt.figure(figsize=(10, 6))
        plt.bar(groups, means, yerr=confidence_intervals, capsize=5, alpha=0.7, color="b")

        plt.xlabel("Grupos")
        plt.ylabel("Media de Contatos Unicos do Grupo")

        plt.xticks(rotation=45)
        plt.tight_layout()

        fig.savefig(
            f"/home/vitorpdavid/codigos/mobility_simulator/group_unique_contact_mean_with_{population}_persons",
            bbox_inches="tight",
        )
        plt.close(fig)


def find_average_contacts_in_subfolders(population_to_collect: str, groups_data: list[int], root_path: PosixPath):
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
            if folder_identifier not in contacts_by_folder:
                contacts_by_folder[folder_identifier] = {}
                unique_contacts_by_folder[folder_identifier] = {}

            with open(file_path, "rb") as file:
                all_contacts = pickle.load(file)

            groups_contacts_data = get_group_contacts_data(groups_data, all_contacts)

            for index, group_key in enumerate(groups_contacts_data.groups_list):
                if group_key not in contacts_by_folder[folder_identifier]:
                    contacts_by_folder[folder_identifier][group_key] = []
                    unique_contacts_by_folder[folder_identifier][group_key] = []

                contacts_by_folder[folder_identifier][group_key].append(groups_contacts_data.total_contacts[index])
                unique_contacts_by_folder[folder_identifier][group_key].append(
                    groups_contacts_data.total_unique_contacts[index]
                )

    return contacts_by_folder, unique_contacts_by_folder


if __name__ == "__main__":
    path = PosixPath(os.path.abspath(__file__)).parent.parent

    with open(path / "data/workhours", "rb") as file:
        data = pickle.load(file)
        groups_data = [int(key) for key in data["group_freq"].keys()]

    contacts_by_folder, unique_contacts_by_folder = find_average_contacts_in_subfolders(
        "1000", groups_data, path / "output"
    )

    calculate_means_and_plot(contacts_by_folder)
    calculate_unique_means_and_plot(unique_contacts_by_folder)
