from itertools import chain
from pathlib import PosixPath
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import pickle
from scipy.stats import sem


def calculate_means_and_plot(data):
    populations = []
    means = []
    confidence_intervals = []

    entries = list(data.items())
    entries.sort(key=lambda a: int(a[0]))

    for population, contacts in entries:
        mean_time = np.mean(contacts)
        standard_error = sem(contacts)
        confidence_interval = 1.96 * standard_error

        populations.append(population)
        means.append(mean_time)
        confidence_intervals.append(confidence_interval)

    fig = plt.figure(figsize=(10, 6))
    plt.bar(populations, means, yerr=confidence_intervals, capsize=5, alpha=0.7, color="b")

    plt.xlabel("População")
    plt.ylabel("Media de Contatos Por Lugar")

    plt.xticks(rotation=45)
    plt.tight_layout()

    fig.savefig("/home/vitorpdavid/codigos/mobility_simulator/places_contact_mean", bbox_inches="tight")
    plt.close(fig)


def find_average_contacts_in_subfolders(root_path, places):
    contacts_by_folder = {}

    for folder_name in os.listdir(root_path):
        file_path = os.path.join(root_path, folder_name, "1", "all_contacts.pkl")

        population_match = re.search(r"population_(\d+)", folder_name)
        if not population_match:
            continue
        folder_identifier = population_match.group(1)

        if os.path.isfile(file_path):
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

            counts: list[int] = [
                len([contact for contact in contacts_list if contact.place == place]) for place in places
            ]

            if folder_identifier not in contacts_by_folder:
                contacts_by_folder[folder_identifier] = []

            contacts_by_folder[folder_identifier].append(sem(counts))

    return contacts_by_folder


if __name__ == "__main__":
    path = PosixPath(os.path.abspath(__file__)).parent.parent
    with open(path / "data/places", "rb") as file:
        places = pickle.load(file)

    data = find_average_contacts_in_subfolders(path / "output", places)

    calculate_means_and_plot(data)
