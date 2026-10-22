from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from ikd1d.io import load_biodex, load_cybex
from ikd1d.schema import COLUMNS

DATA = Path(__file__).parent / "data"


@pytest.fixture(scope="module")
def biodex_con():
    return load_biodex(DATA / "Biodex_system3_Qcon120-Hcon120.txt")


@pytest.fixture(scope="module")
def cybex():
    return load_cybex(DATA / "Cybex_Qcon60-Hcon60.CSV")


def test_biodex_schema_and_length(biodex_con):
    assert tuple(biodex_con.columns) == COLUMNS
    assert len(biodex_con) == 923  # 929 lines minus 6 header lines
    assert not biodex_con.isna().any().any()


def test_biodex_first_rows_use_anatomical_angle(biodex_con):
    first = biodex_con.iloc[0]
    assert first.to_dict() == pytest.approx(
        {"time": 0.0, "torque": 0.0, "angle": 105.0, "velocity": -1.8}
    )
    second = biodex_con.iloc[1]
    assert second["time"] == pytest.approx(0.010)
    assert second["torque"] == pytest.approx(74.9)
    assert second["angle"] == pytest.approx(105.0)


def test_biodex_time_is_seconds_and_monotonic(biodex_con):
    assert biodex_con["time"].iloc[-1] == pytest.approx(9.22)
    assert (np.diff(biodex_con["time"]) > 0).all()


def test_biodex_eccentric_file_loads():
    df = load_biodex(DATA / "Biodex_system3_QNaN-Hecc120.txt")
    assert tuple(df.columns) == COLUMNS
    assert df["torque"].iloc[1] == pytest.approx(-59.4)
    assert df["time"].iloc[-1] == pytest.approx(9.52)


def test_biodex_rejects_non_biodex(tmp_path):
    f = tmp_path / "x.txt"
    f.write_text("a\nb\n")
    with pytest.raises(ValueError):
        load_biodex(f)


def test_biodex_v5_layout(tmp_path):
    # 3 header lines, then comma decimals and "-" blanks; cols: 2 dropped, time, torque, x, ang, vel
    f = tmp_path / "v5.txt"
    f.write_text(
        "h1\nh2\nh3\n"
        "1 1 0 5,5 9 100,5 -1,5\n"
        "1 1 10 6,5 9 101,5 -\n"
        "1 1 99 7,5 9 102,5 3\n"
    )
    df = load_biodex(f)
    assert tuple(df.columns) == COLUMNS
    # time rebuilt as a uniform ramp, converted to seconds
    assert df["time"].tolist() == pytest.approx([0.0, 0.010, 0.020])
    assert df["torque"].tolist() == pytest.approx([5.5, 6.5, 7.5])
    assert df["angle"].tolist() == pytest.approx([100.5, 101.5, 102.5])
    assert df["velocity"].tolist() == pytest.approx([-1.5, 0.0, 3.0])


def test_cybex_schema_and_length(cybex):
    assert tuple(cybex.columns) == COLUMNS
    assert len(cybex) == 1518  # 1519 lines minus the header
    assert cybex["time"].iloc[1] == pytest.approx(0.010)


def test_cybex_torque_sign_follows_angle_direction(cybex):
    raw = pd.read_csv(DATA / "Cybex_Qcon60-Hcon60.CSV")
    angle, tq = raw["Position(Degrees)"].to_numpy(), raw["Torque(Newton-Meters)"].to_numpy()
    expected = tq.copy()
    expected[:-1][angle[:-1] < angle[1:]] *= -1
    np.testing.assert_allclose(cybex["torque"], expected)
    assert (cybex["torque"] < 0).any() and (cybex["torque"] > 0).any()


def test_cybex_missing_columns(tmp_path):
    f = tmp_path / "bad.csv"
    f.write_text("a,b\n1,2\n")
    with pytest.raises(ValueError):
        load_cybex(f)
