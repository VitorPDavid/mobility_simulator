from pathlib import PosixPath
import numpy as np
import matplotlib.pyplot as plt
import os
import re

from scipy.stats import sem


def calculate_means_and_plot(data):
    populations = []
    means = []
    confidence_intervals = []

    entries = list(data.items())
    entries.sort(key=lambda a: int(a[0]))

    for population, times in entries:
        mean_time = np.mean(times)
        standard_error = sem(times)
        confidence_interval = 1.96 * standard_error

        populations.append(population)
        means.append(mean_time)
        confidence_intervals.append(confidence_interval)

    fig = plt.figure(figsize=(10, 6))
    plt.bar(populations, means, yerr=confidence_intervals, capsize=5, alpha=0.7, color="b")

    plt.xlabel("População")
    plt.ylabel("Tempo Medio de Contato")
    plt.title("Tempo Medio de Contato por População com Intervalo de Confiança de 95%")

    plt.xticks(rotation=45)
    plt.tight_layout()

    fig.savefig("/home/vitorpdavid/codigos/mobility_simulator/mean.png", bbox_inches="tight")
    plt.close(fig)


def find_average_times_in_subfolders(root_path):
    times_by_folder = {}

    for folder_name in os.listdir(root_path):
        folder_path = os.path.join(root_path, folder_name)

        if os.path.isdir(folder_path):
            file_path = os.path.join(folder_path, "contacts.txt")
            if not os.path.isfile(file_path):
                file_path = os.path.join(folder_path, "1", "contacts.txt")

            if file_path:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()

                    match = re.search(r"tempo medio: (\d+(\.\d+)?)", content)
                    if match:
                        average_time = float(match.group(1))

                        population_match = re.search(r"population_(\d+)", folder_name)
                        if population_match:
                            folder_identifier = population_match.group(1)

                            if folder_identifier not in times_by_folder:
                                times_by_folder[folder_identifier] = []

                            times_by_folder[folder_identifier].append(average_time)

    return times_by_folder


if __name__ == "__main__":
    data = find_average_times_in_subfolders(PosixPath(os.path.abspath(__file__)).parent.parent / "output")

    calculate_means_and_plot(data)
