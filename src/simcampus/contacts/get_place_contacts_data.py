from simcampus.contacts.contacts_types import Place, Contact, ContactData


def get_place_contacts_data(all_contacts: dict[int, list[Contact]]):
    contacts_data: list[ContactData] = []
    place_contacts: dict[Place, list[Contact]] = {}

    for _, person_contacts in all_contacts.items():
        for contact in person_contacts:
            if contact.place in place_contacts:
                place_contacts[contact.place].append(contact)
            else:
                place_contacts[contact.place] = []

    for place in place_contacts.keys():
        contacts = place_contacts[place]

        unique_contacts_control: set[int] = set()
        unique_contacts: list[Contact] = []

        for contact in contacts:
            if contact.persons_hash() not in unique_contacts_control:
                unique_contacts.append(contact)
                unique_contacts_control.add(contact.persons_hash())

        contacts_data.append(ContactData(place, contacts, len(contacts), len(unique_contacts)))

    return contacts_data
