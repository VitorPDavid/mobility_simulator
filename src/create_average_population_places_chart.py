from itertools import chain
from pathlib import PosixPath
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import pickle
from scipy.stats import sem


def calculate_means_and_plot(data):
    for population, places_data in data.items():
        places = []
        means = []
        confidence_intervals = []
        for place, place_data in places_data.items():
            mean_time = np.mean(place_data)
            standard_error = sem(place_data)
            confidence_interval = 1.96 * standard_error

            places.append(place)
            means.append(mean_time)
            confidence_intervals.append(confidence_interval)

        fig = plt.figure(figsize=(10, 6))
        plt.bar(places, means, yerr=confidence_intervals, capsize=5, alpha=0.7, color="b")

        plt.xlabel("Locais")
        plt.ylabel("Media de Contatos do Local")

        plt.xticks(rotation=45)
        plt.tight_layout()

        fig.savefig(
            f"/home/vitorpdavid/codigos/mobility_simulator/place_contact_mean_with_{population}_persons",
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

        plt.xlabel("Locais")
        plt.ylabel("Media de Contatos Unicos do Local")

        plt.xticks(rotation=45)
        plt.tight_layout()

        fig.savefig(
            f"/home/vitorpdavid/codigos/mobility_simulator/place_unique_contact_mean_with_{population}_persons",
            bbox_inches="tight",
        )
        plt.close(fig)


def find_average_contacts_in_subfolders(population_to_collect: str, root_path, places):
    contacts_by_folder = {}
    unique_contacts_by_folder = {}

    folder_name_list = list(os.listdir(root_path))
    folder_name_list.sort()

    for folder_name in folder_name_list:
        file_path = os.path.join(root_path, folder_name, "1", "all_contacts.pkl")
        population_match = re.search(r"population_(\d+)", folder_name)
        if not population_match:
            continue
        folder_identifier = population_match.group(1)
        if folder_identifier != population_to_collect:
            continue

        if os.path.isfile(file_path):
            print(file_path)
            if folder_identifier not in contacts_by_folder:
                contacts_by_folder[folder_identifier] = {}
                unique_contacts_by_folder[folder_identifier] = {}

            with open(file_path, "rb") as file:
                all_contacts = pickle.load(file)

            contacts_list = [
                contact
                for contact in {
                    contact
                    for contact in chain.from_iterable([contact_list for contact_list in all_contacts.values()])
                }
            ]

            places = [place for place in places if place is not None]

            for place_key in places:
                if place_key not in contacts_by_folder[folder_identifier]:
                    contacts_by_folder[folder_identifier][place_key] = []
                    unique_contacts_by_folder[folder_identifier][place_key] = []

                unique_contacts_control: set[int] = set()
                unique_contacts = []

                for contact in contacts_list:
                    if contact.place != place_key:
                        continue
                    if contact.persons_hash() not in unique_contacts_control:
                        unique_contacts.append(contact)
                        unique_contacts_control.add(contact.persons_hash())

                contacts_by_folder[folder_identifier][place_key].append(
                    len([contact for contact in contacts_list if contact.place == place_key])
                )
                unique_contacts_by_folder[folder_identifier][place_key].append(len(unique_contacts))

    return contacts_by_folder, unique_contacts_by_folder


if __name__ == "__main__":
    path = PosixPath(os.path.abspath(__file__)).parent.parent
    with open(path / "data/places", "rb") as file:
        places = pickle.load(file)

    contacts_by_folder, unique_contacts_by_folder = find_average_contacts_in_subfolders("400", path / "output", places)

    calculate_means_and_plot(contacts_by_folder)
    calculate_unique_means_and_plot(unique_contacts_by_folder)
