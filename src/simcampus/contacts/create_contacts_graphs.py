from itertools import chain
from pathlib import PosixPath
import pickle

import matplotlib.pyplot as plt
import numpy as np

from simcampus.simulation_types import Place
from simcampus.contacts.contacts_types import Contact, ContactData, GroupContactsData
from simcampus.contacts.create_contact_heatmap import create_contact_heatmap
from simcampus.contacts.get_group_contacts_data import get_group_contacts_data


def create_contacts_graphs(
    output_path: PosixPath,
    all_contacts: dict[int, list[Contact]],
    places: list[Place],
    person_contacts_data: list[ContactData],
):
    # groups
    groups_contacts_data = get_group_contacts_data(all_contacts)
    __groups_contacts_heatmap(groups_contacts_data, output_path)

    __create_groups_contact_bar_graph(groups_contacts_data, output_path)
    __create_groups_unique_contact_bar_graph(groups_contacts_data, output_path)

    __create_groups_total_contacts_with_other_groups_bar_graph(groups_contacts_data, output_path)
    __create_groups_total_unique_contacts_with_other_groups_bar_graph(groups_contacts_data, output_path)

    # places
    __create_place_contacts_bar_graph(places, all_contacts, output_path)

    # general contatcs graphs
    __create_contacts_histogram(person_contacts_data, output_path)
    __create_unique_contacts_histogram(person_contacts_data, output_path)
    __create_total_time_histogram(all_contacts, output_path)


def __groups_contacts_heatmap(groups_contacts_data: GroupContactsData, output_path: PosixPath):
    create_contact_heatmap(
        groups_contacts_data.groups_list,
        groups_contacts_data.contact_matrix,
        "Contatos entre grupos",
        output_path / "groups_contacts_heatmap.png",
    )

    create_contact_heatmap(
        groups_contacts_data.groups_list,
        groups_contacts_data.unique_contacts_matrix,
        "Contatos Unicos entre grupos",
        output_path / "groups_unique_contacts_heatmap.png",
    )


def __create_groups_contact_bar_graph(groups_contacts_data: GroupContactsData, output_path: PosixPath):
    fig, ax = plt.subplots()

    ax.bar(
        groups_contacts_data.groups_list, groups_contacts_data.total_contacts, label=groups_contacts_data.groups_list
    )

    ax.set_ylabel("Total de encontros por Grupo")
    ax.set_xlabel("Grupos")

    fig.savefig(output_path / "groups_total_contacts.png", bbox_inches="tight")
    plt.close(fig)


def __create_groups_unique_contact_bar_graph(groups_contacts_data: GroupContactsData, output_path: PosixPath):
    fig, ax = plt.subplots()

    ax.bar(
        groups_contacts_data.groups_list,
        groups_contacts_data.total_unique_contacts,
        label=groups_contacts_data.groups_list,
    )

    ax.set_ylabel("Total de encontros Unicos por Grupo")
    ax.set_xlabel("Grupos")

    fig.savefig(output_path / "groups_total_unique_contacts.png", bbox_inches="tight")
    plt.close(fig)


def __create_groups_total_contacts_with_other_groups_bar_graph(
    groups_contacts_data: GroupContactsData, output_path: PosixPath
):
    fig, ax = plt.subplots()

    ax.bar(
        groups_contacts_data.groups_list,
        groups_contacts_data.total_contacts_with_other_groups,
        label=groups_contacts_data.groups_list,
    )

    ax.set_ylabel("Total de Encontros com Outros Grupos")
    ax.set_xlabel("Grupos")

    fig.savefig(output_path / "groups_total_contacts_with_other_groups.png", bbox_inches="tight")
    plt.close(fig)


def __create_groups_total_unique_contacts_with_other_groups_bar_graph(
    groups_contacts_data: GroupContactsData, output_path: PosixPath
):
    fig, ax = plt.subplots()

    ax.bar(
        groups_contacts_data.groups_list,
        groups_contacts_data.total_unique_contacts_with_other_groups,
        label=groups_contacts_data.groups_list,
    )

    ax.set_ylabel("Total de Encontros Unicos com Outros Grupos")
    ax.set_xlabel("Grupos")

    fig.savefig(output_path / "groups_total_unique_contacts_with_other_groups.png", bbox_inches="tight")
    plt.close(fig)


def __create_place_contacts_bar_graph(
    places: list[Place], all_contacts: dict[int, list[Contact]], output_path: PosixPath
):
    contacts_list = [
        contact
        for contact in {
            contact for contact in chain.from_iterable([contact_list for contact_list in all_contacts.values()])
        }
    ]

    places = [place for place in places if place is not None]

    counts: list[int] = []
    for place in places:
        counts.append(len([contact for contact in contacts_list if contact.place == place]))

    fig, ax = plt.subplots()

    ax.bar(places, counts, label=places)

    ax.set_ylabel("total de encontros")

    fig.savefig(output_path / "place_total_contacts_bars.png", bbox_inches="tight")
    plt.close(fig)


def __create_contacts_histogram(contacts_data: list[ContactData], output_path: PosixPath):
    contacts = np.array([data.total_contacts for data in contacts_data], dtype=np.int32)

    fig, ax = plt.subplots()
    ax.hist(contacts, bins=20)
    ax.plot(contacts, 0 * contacts, "d")
    ax.set_ylabel("total de pessoas com esses contatos")
    ax.set_xlabel("quantidade de contatos")

    fig.savefig(output_path / "contact_histogram.png", bbox_inches="tight")
    plt.close(fig)


def __create_unique_contacts_histogram(contacts_data: list[ContactData], output_path: PosixPath):
    unique_contacts = np.array([data.total_unique_contacts for data in contacts_data], dtype=np.int32)
    fig, ax = plt.subplots()

    ax.hist(unique_contacts, bins=20)
    ax.plot(unique_contacts, 0 * unique_contacts, "d")
    ax.set_ylabel("total de pessoas com esses encontros")
    ax.set_xlabel("quantidade de pessoas encontradas")

    fig.savefig(output_path / "unique_contact_histogram.png", bbox_inches="tight")
    plt.close(fig)


def __create_total_time_histogram(all_contacts: dict[int, list[Contact]], output_path: PosixPath):
    all_times = np.array(
        [
            contact.contact_duration
            for contact in {
                contact for contact in chain.from_iterable([contact_list for contact_list in all_contacts.values()])
            }
        ],
        dtype=np.float64,
    )

    with open(output_path / "all_times.pkl", "wb") as all_times_file:
        pickle.dump(all_times, all_times_file)

    fig, ax = plt.subplots()

    ax.hist(all_times, bins=25)
    ax.plot(all_times, 0 * all_times, "d")
    ax.set_xlabel("tempo de contato")
    ax.set_ylabel("total de contatos")

    fig.savefig(output_path / "total_time_histogram.png", bbox_inches="tight")
    plt.close(fig)
