from typing import Collection, Iterable
from simcampus.contacts.contacts_types import Contact, ContactData
from simcampus.simulation_types import GroupIdentifier


def get_group_contacts_data(all_contacts: dict[int, list[Contact]]):
    contacts_data: list[ContactData] = []
    group_contacts: dict[int, Collection[Contact]] = {}

    for person, person_contacts in all_contacts.items():
        if len(person_contacts) > 0:
            group = int(person_contacts[0].get_person(person).group)
            group_contacts[group] = set([*group_contacts.get(group, set()), *person_contacts])

    groups_list = list(group_contacts.keys())
    groups_list.sort()

    contact_matrix: list[list[int]] = []
    unique_contacts_matrix: list[list[int]] = []
    frequency_matrix: list[list[float]] = []
    unique_contacts_frequency_matrix: list[list[float]] = []

    unique_contact_graph: dict[GroupIdentifier, dict[GroupIdentifier, int]] = {
        group: {group: 0 for inner_group in groups_list if inner_group != group} for group in groups_list
    }

    for index, group in enumerate(groups_list):
        contacts = group_contacts[group]

        unique_contacts_control: set[int] = set()
        unique_contacts: list[Contact] = []

        for contact in contacts:
            if contact.persons_hash() not in unique_contacts_control:
                unique_contacts.append(contact)
                unique_contacts_control.add(contact.persons_hash())

        contact_matrix.append(__create_matrix_row(index, groups_list, contacts))
        unique_contacts_matrix.append(__create_matrix_row(index, groups_list, unique_contacts))

        frequency_matrix.append(__create_frequence_row(contact_matrix[index], groups_list))
        unique_contacts_frequency_matrix.append(__create_frequence_row(unique_contacts_matrix[index], groups_list))

        contacts_data.append(ContactData(group, contacts, len(contacts), len(unique_contacts)))

    return (
        contacts_data,
        groups_list,
        contact_matrix,
        unique_contacts_matrix,
        frequency_matrix,
        unique_contacts_frequency_matrix,
        unique_contact_graph,
    )


def __create_matrix_row(row_index: int, groups_list: list[GroupIdentifier], contacts: Iterable[Contact]):
    row = [
        len(
            list(
                filter(
                    lambda contact: contact.contact_with_group(groups_list[row_index], column_group),
                    contacts,
                )
            )
        )
        for column_group in groups_list
    ]

    total = sum(row)
    row.append(total)
    row.append(total - row[row_index])

    return row


def __create_frequence_row(contact_row: list[int], groups_list: list[GroupIdentifier]):
    total = contact_row[-2]

    return [
        total / contact_row[column_index] if contact_row[column_index] > 0 else 0
        for column_index in range(len(groups_list))
    ]
