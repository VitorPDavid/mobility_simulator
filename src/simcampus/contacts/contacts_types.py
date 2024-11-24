from dataclasses import dataclass, field
from typing import Any, Collection
from simcampus.simulation_types import GroupIdentifier, PersonIdentifier, Place


@dataclass
class ContactPerson:
    identifier: PersonIdentifier
    group: GroupIdentifier

    def __hash__(self) -> int:
        return hash(f"{self.identifier}")

    def __eq__(self, value: object) -> bool:
        if isinstance(value, int):
            return self.identifier == value

        return self.identifier == getattr(value, "identifier", None)


@dataclass
class Contact:
    place: Place
    start_time: float
    firts_person: ContactPerson
    second_person: ContactPerson
    end_time: float | None = None
    contact_duration: float = 0

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "end_time" and value is not None:
            self.contact_duration = value - self.start_time

        super().__setattr__(name, value)

    def __hash__(self) -> int:
        persons = [self.firts_person.identifier, self.second_person.identifier]
        persons.sort()

        return hash(f"{self.start_time}{self.end_time}{persons}")

    def __getitem__(self, name: object):
        if not isinstance(name, int):
            raise TypeError(f"Pessoa so pode ter o identificador do tipo inteiro, {name} não é inteiro")

        if name == self.firts_person:
            return self.firts_person

        if name == self.second_person:
            return self.second_person

        raise KeyError(f"Pessoa {name} não existe no contato")

    def persons_hash(self):
        persons = [self.firts_person.identifier, self.second_person.identifier]
        persons.sort()

        return hash(f"{persons}")

    def has_person(self, identifier: int):
        if identifier == self.second_person or identifier == self.firts_person:
            return True

        return False

    def get_person(self, identifier: int):
        if identifier == self.firts_person:
            return self.firts_person

        if identifier == self.second_person:
            return self.second_person

        raise KeyError(f"Pessoa {identifier} não existe no contato")

    def get_other_person_in_contact(self, identifier: int):
        if identifier == self.firts_person:
            return self.second_person.identifier

        if identifier == self.second_person:
            return self.firts_person.identifier

        raise KeyError(f"Pessoa {identifier} não existe no contato")

    def contact_with_group(self, base_group: int, other_group: int):
        return (self.firts_person.group == base_group and self.second_person.group == other_group) or (
            self.firts_person.group == other_group and self.second_person.group == base_group
        )


@dataclass
class ContactData:
    identifier: GroupIdentifier | PersonIdentifier | Place
    contacts: Collection[Contact]
    total_contacts: int
    total_unique_contacts: int
    total_contacts_matrix: list[list[int]] = field(default_factory=list)
    total_unique_contacts_matrix: list[list[int]] = field(default_factory=list)

    def __str__(self, verbose: bool = True) -> str:
        contacts_str = ""
        if verbose:
            contacts_str = self.get_contacts_str()

        return (
            f"Contatos de {self.identifier}\n"
            f"{contacts_str}"
            f"Contatos Totais: {self.total_contacts}\n"
            f"Contatos Unicos: {self.total_unique_contacts}\n\n"
        )

    def get_contacts_str(self):
        contacts_str = ""
        for contact in self.contacts:
            contacts_str += f"{contact}\n"

        return f"Lista de Contatos:\n{contacts_str}"


@dataclass
class GroupContactsData:
    contacts_data: list[ContactData]
    groups_list: list[str]
    contact_matrix: list[list[int]]
    unique_contacts_matrix: list[list[int]]

    total_contacts: list[int]
    total_contacts_with_other_groups: list[int]

    total_unique_contacts: list[int]
    total_unique_contacts_with_other_groups: list[int]
