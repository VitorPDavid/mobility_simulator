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
    plt.ylabel("Media de Contatos Por Pessoa")
    plt.title("Contatos por População com Intervalo de Confiança")

    plt.xticks(rotation=45)
    plt.tight_layout()

    fig.savefig("/home/vitorpdavid/codigos/mobility_simulator/contact_mean", bbox_inches="tight")
    plt.close(fig)


def calculate_unique_contacts_means_and_plot(data):
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
    plt.ylabel("Media de Contatos Unicos Por Pessoa")
    plt.title("Contatos Unicos por População com Intervalo de Confiança")

    plt.xticks(rotation=45)
    plt.tight_layout()

    fig.savefig("/home/vitorpdavid/codigos/mobility_simulator/unique_contact_mean", bbox_inches="tight")
    plt.close(fig)


def find_average_contacts_in_subfolders(root_path):
    contacts_by_folder = {}
    unique_contacts_by_folder = {}

    for folder_name in os.listdir(root_path):
        file_path = os.path.join(root_path, folder_name, "1", "all_contacts.pkl")

        population_match = re.search(r"population_(\d+)", folder_name)
        if not population_match:
            continue
        folder_identifier = population_match.group(1)

        if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                all_contacts = pickle.load(file)

            person_total_contacts = []
            person_total_unique_contacts = []
            for person, person_contacts in all_contacts.items():
                person_unique_contacts: set[int] = set(
                    map(lambda contact: contact.get_other_person_in_contact(person), person_contacts)
                )
                person_total_contacts.append(len(person_contacts))
                person_total_unique_contacts.append(len(person_unique_contacts))

            average_contact = np.mean(person_total_contacts)
            average_uniquecontact = np.mean(person_total_unique_contacts)

            population_match = re.search(r"population_(\d+)", folder_name)
            if population_match:
                folder_identifier = population_match.group(1)

                if folder_identifier not in contacts_by_folder:
                    contacts_by_folder[folder_identifier] = []
                    unique_contacts_by_folder[folder_identifier] = []

                contacts_by_folder[folder_identifier].append(average_contact)
                unique_contacts_by_folder[folder_identifier].append(average_uniquecontact)

    return contacts_by_folder, unique_contacts_by_folder


if __name__ == "__main__":
    path = PosixPath(os.path.abspath(__file__)).parent.parent
    with open(path / "data/places", "rb") as file:
        places = pickle.load(file)

    data, data2 = find_average_contacts_in_subfolders(path / "output")

    calculate_means_and_plot(data)
    calculate_unique_contacts_means_and_plot(data2)
