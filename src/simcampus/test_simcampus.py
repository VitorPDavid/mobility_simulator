from pathlib import Path
import pytest

from simcampus.simulation_types import SimulationArgs

from .simulation import run_simulation

DATA_PATH = Path(__file__).parent.parent.parent / "data"


def test_case0(capsys):
    rep1 = Path(__file__).parent.parent.parent / "output/execucao_0/repetition_0.txt"

    run_simulation(
        **SimulationArgs(
            {
                "days": 10,
                "seed": 1,
                "stay": 10.0,
                "verbose": False,
                "population": 10,
                "inputdir": DATA_PATH.absolute(),
            }
        )
    )

    captured = capsys.readouterr()

    with open(rep1, "r") as file:
        assert file.read() == captured.out


def test_case1(capsys):
    rep1 = Path(__file__).parent.parent.parent / "output/execucao_1/repetition_0.txt"

    run_simulation(
        **SimulationArgs(
            {
                "days": 100,
                "seed": 1,
                "stay": 10.0,
                "verbose": False,
                "population": 10,
                "inputdir": DATA_PATH.absolute(),
            }
        )
    )

    captured = capsys.readouterr()

    with open(rep1, "r") as file:
        assert file.read() == captured.out


@pytest.mark.skip(reason="muito lento")
def test_case2(capsys):
    rep1 = Path(__file__).parent.parent.parent / "output/execucao_2/repetition_0.txt"

    run_simulation(
        **SimulationArgs(
            {
                "days": 1000,
                "seed": 1,
                "stay": 10.0,
                "verbose": False,
                "population": 10,
                "inputdir": DATA_PATH.absolute(),
            }
        )
    )

    captured = capsys.readouterr()

    with open(rep1, "r") as file:
        assert file.read() == captured.out


def test_case3(capsys):
    rep1 = Path(__file__).parent.parent.parent / "output/execucao_3/repetition_0.txt"

    run_simulation(
        **SimulationArgs(
            {
                "days": 10,
                "seed": 1,
                "stay": 10.0,
                "verbose": False,
                "population": 100,
                "inputdir": DATA_PATH.absolute(),
            }
        )
    )

    captured = capsys.readouterr()

    with open(rep1, "r") as file:
        assert file.read() == captured.out


def test_case4(capsys):
    rep1 = Path(__file__).parent.parent.parent / "output/execucao_4/repetition_0.txt"

    run_simulation(
        **SimulationArgs(
            {
                "days": 100,
                "seed": 1,
                "stay": 10.0,
                "verbose": False,
                "population": 100,
                "inputdir": DATA_PATH.absolute(),
            }
        )
    )

    captured = capsys.readouterr()

    with open(rep1, "r") as file:
        assert file.read() == captured.out


@pytest.mark.skip(reason="muito lento")
def test_case5(capsys):
    rep1 = Path(__file__).parent.parent.parent / "output/execucao_5/repetition_0.txt"

    run_simulation(
        **SimulationArgs(
            {
                "days": 1000,
                "seed": 1,
                "stay": 10.0,
                "verbose": False,
                "population": 100,
                "inputdir": DATA_PATH.absolute(),
            }
        )
    )

    captured = capsys.readouterr()

    with open(rep1, "r") as file:
        assert file.read() == captured.out


def test_case6(capsys):
    rep1 = Path(__file__).parent.parent.parent / "output/execucao_6/repetition_0.txt"

    run_simulation(
        **SimulationArgs(
            {
                "days": 10,
                "seed": 1,
                "stay": 10.0,
                "verbose": False,
                "population": 1000,
                "inputdir": DATA_PATH.absolute(),
            }
        )
    )

    captured = capsys.readouterr()

    with open(rep1, "r") as file:
        assert file.read() == captured.out


@pytest.mark.skip(reason="muito lento")
def test_case7(capsys):
    rep1 = Path(__file__).parent.parent.parent / "output/execucao_7/repetition_0.txt"

    run_simulation(
        **SimulationArgs(
            {
                "days": 100,
                "seed": 1,
                "stay": 10.0,
                "verbose": False,
                "population": 1000,
                "inputdir": DATA_PATH.absolute(),
            }
        )
    )

    captured = capsys.readouterr()

    with open(rep1, "r") as file:
        assert file.read() == captured.out


@pytest.mark.skip(reason="muito lento")
def test_case8(capsys):
    rep1 = Path(__file__).parent.parent.parent / "output/execucao_8/repetition_0.txt"

    run_simulation(
        **SimulationArgs(
            {
                "days": 1000,
                "seed": 1,
                "stay": 10.0,
                "verbose": False,
                "population": 1000,
                "inputdir": DATA_PATH.absolute(),
            }
        )
    )

    captured = capsys.readouterr()

    with open(rep1, "r") as file:
        assert file.read() == captured.out
