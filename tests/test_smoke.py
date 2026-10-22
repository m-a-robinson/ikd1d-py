from pathlib import Path

import pytest

import ikd1d
from ikd1d.cli import main

DATA = Path(__file__).parent / "data"


def test_schema():
    assert ikd1d.COLUMNS == ("time", "torque", "angle", "velocity")


def test_cli_runs():
    assert main([]) == 0


@pytest.mark.parametrize("name", [
    "Biodex_system3_Qcon120-Hcon120.txt",
    "Biodex_system3_QNaN-Hecc120.txt",
    "Cybex_Qcon60-Hcon60.CSV",
])
def test_sample_data_present(name):
    assert (DATA / name).stat().st_size > 0

