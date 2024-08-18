from typing import TypeAlias, TypedDict


class SimulationArgs(TypedDict):
    inputdir: str
    days: int
    stay: float
    population: int
    seed: int
    verbose: bool


Transitions: TypeAlias = dict[str | None, dict[None | str, int]]

Stay: TypeAlias = dict[str | None, tuple[float, float]]

GroupFrequency: TypeAlias = dict[int, int]

GroupParameters: TypeAlias = dict[int, list[tuple[float, float]]]

Place: TypeAlias = str | None
