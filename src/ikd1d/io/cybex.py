"""Cybex/HUMAC CSV export loader.

Ports the radioCybex branch of ``loadButton_Callback`` in the MATLAB app. Columns in the file
are ``Status, Time(Seconds), Position(Degrees), Torque(Newton-Meters), Speed(deg/sec)``.

Cybex reports torque as a magnitude, so as in MATLAB the sign is flipped on every sample where
the angle is about to increase (``angle[i] < angle[i+1]``). The final sample is left unchanged.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from ikd1d.schema import COLUMNS


def load_cybex(path: str | Path) -> pd.DataFrame:
    """Load a Cybex CSV export as a DataFrame with ``ikd1d.schema.COLUMNS`` (time in seconds)."""
    raw = pd.read_csv(path, dtype=str)
    needed = {"Time(Seconds)", "Position(Degrees)", "Torque(Newton-Meters)", "Speed(deg/sec)"}
    missing = needed - set(raw.columns)
    if missing:
        raise ValueError(f"{path}: missing Cybex columns {sorted(missing)}")
    num = raw[sorted(needed)].apply(pd.to_numeric, errors="coerce")
    df = pd.DataFrame(
        {
            "time": num["Time(Seconds)"],
            "torque": num["Torque(Newton-Meters)"],
            "angle": num["Position(Degrees)"],
            "velocity": num["Speed(deg/sec)"],
        },
        columns=list(COLUMNS),
    ).reset_index(drop=True)
    rising = df["angle"].to_numpy()[:-1] < df["angle"].to_numpy()[1:]
    sign = np.ones(len(df))
    sign[:-1][rising] = -1.0
    df["torque"] = df["torque"] * sign
    return df
