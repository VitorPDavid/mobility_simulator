from dataclasses import dataclass, astuple
from typing import Sequence, TypeAlias, TypedDict


class SimulationArgs(TypedDict):
    inputdir: str
    days: int
    stay: float
    population: int
    seed: int
    verbose: bool


Place: TypeAlias = str | None

Transitions: TypeAlias = dict[Place, dict[None | str, int]]

GroupFrequency: TypeAlias = dict[int, int]


@dataclass
class DistributionParameter:
    loc: float
    scale: float

    def __init__(self, params: tuple[float, float]):
        self.loc = params[0]
        self.scale = params[1]

    def __iter__(self):
        return iter(astuple(self))

    def __repr__(self) -> str:
        return f"({self.loc}, {self.scale})"


@dataclass
class GroupArrivelAndDerpartureParameters:
    arrivel: DistributionParameter
    derparture: DistributionParameter

    def __init__(self, params: Sequence[tuple[float, float]]):
        self.arrivel = DistributionParameter(params[0])
        self.derparture = DistributionParameter(params[1])

    def __iter__(self):
        return iter(astuple(self))

    def __repr__(self) -> str:
        return f"{self.arrivel}{self.derparture}"


GroupParameters: TypeAlias = dict[int, GroupArrivelAndDerpartureParameters]
