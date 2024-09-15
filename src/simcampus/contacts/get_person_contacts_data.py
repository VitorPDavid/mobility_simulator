from simcampus.contacts.contacts_types import Contact, ContactData


def get_person_contacts_data(
    all_contacts: dict[int, list[Contact]],
):
    contacts_data: list[ContactData] = []
    for person, person_contacts in all_contacts.items():
        person_unique_contacts: set[int] = set(
            map(lambda contact: contact.get_other_person_in_contact(person), person_contacts)
        )

        contacts_data.append(ContactData(person, person_contacts, len(person_contacts), len(person_unique_contacts)))

    return contacts_data
