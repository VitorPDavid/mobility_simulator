from typing import Collection, Iterable
from simcampus.contacts.contacts_types import Contact, ContactData, GroupContactsData
from simcampus.simulation_types import GroupIdentifier


def get_group_contacts_data(
    groups: list[GroupIdentifier], all_contacts: dict[int, list[Contact]]
) -> GroupContactsData:
    contacts_data: list[ContactData] = []
    group_contacts: dict[int, Collection[Contact]] = {}

    for person, person_contacts in all_contacts.items():
        if len(person_contacts) > 0:
            group = int(person_contacts[0].get_person(person).group)
            group_contacts[group] = set([*group_contacts.get(group, set()), *person_contacts])

    groups_list: list[int] = [*groups]
    groups_list.sort()

    contact_matrix: list[list[int]] = []
    unique_contacts_matrix: list[list[int]] = []

    total_contacts: list[int] = []
    total_contacts_with_other_groups: list[int] = []
    total_unique_contacts: list[int] = []
    total_unique_contacts_with_other_groups: list[int] = []

    for index, group in enumerate(groups_list):
        contacts = group_contacts.get(group, [])

        unique_contacts_control: set[int] = set()
        unique_contacts: list[Contact] = []

        for contact in contacts:
            if contact.persons_hash() not in unique_contacts_control:
                unique_contacts.append(contact)
                unique_contacts_control.add(contact.persons_hash())

        row = __create_matrix_row(index, groups_list, contacts)
        contact_matrix.append(row)

        total_contacts.append(sum(row))
        total_contacts_with_other_groups.append(sum(row) - row[index])

        row = __create_matrix_row(index, groups_list, unique_contacts)
        unique_contacts_matrix.append(row)

        total_unique_contacts.append(sum(row))
        total_unique_contacts_with_other_groups.append(sum(row) - row[index])

        contacts_data.append(ContactData(group, contacts, len(contacts), len(unique_contacts)))

    return GroupContactsData(
        contacts_data,
        [str(group) for group in groups_list],
        contact_matrix,
        unique_contacts_matrix,
        total_contacts,
        total_contacts_with_other_groups,
        total_unique_contacts,
        total_unique_contacts_with_other_groups,
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

    return row
