"""Biodex System 3 text export loader.

Ports the radioBiodex branch of ``loadButton_Callback`` in the MATLAB app. Two layouts exist
and are told apart the way the MATLAB code does it: if line 4 of the file is blank it is the
older layout, otherwise it is the Biodex v5 layout.

* older: 6 header lines, then whitespace-separated ``TIME(ms) TORQUE POSITION POS(ANAT)
  VELOCITY``. Angle is taken from ``POS (ANAT)``; ``POSITION`` is discarded.
* v5: 3 header lines, comma decimal separators and ``-`` for blank cells. MATLAB drops the
  first two columns and the fifth, and rebuilds the time column from the first sample step.
  No v5 sample file is available yet, so this branch is untested against real data.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from ikd1d.schema import COLUMNS


def _read_lines(path: Path) -> list[str]:
    with open(path, encoding="utf-8", errors="replace", newline=None) as fh:
        return fh.read().splitlines()


def _frame(time_ms, torque, angle, velocity) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "time": np.asarray(time_ms, dtype=float) / 1000.0,
            "torque": torque,
            "angle": angle,
            "velocity": velocity,
        },
        columns=list(COLUMNS),
    )


def _load_legacy(lines: list[str]) -> pd.DataFrame:
    rows = [[float(x) for x in ln.split()] for ln in lines[6:] if ln.strip()]
    d = np.array(rows, dtype=float)
    # columns: time, torque, position, pos(anat), velocity -> use pos(anat)
    return _frame(d[:, 0], d[:, 1], d[:, 3], d[:, 4])


def _load_v5(lines: list[str]) -> pd.DataFrame:
    rows = []
    for ln in lines[3:]:
        if not ln.strip():
            continue
        tokens = [("0" if t == "-" else t.replace(",", ".")) for t in ln.split()]
        rows.append([float(t) for t in tokens])
    d = np.array(rows, dtype=float)
    # MATLAB: delete cols 1 and 2, then (new) col 3 -> original cols 3, 4, 6
    if d.shape[1] < 7:
        raise ValueError("Unexpected Biodex v5 layout: fewer than 7 columns")
    time_ms, torque, angle, velocity = d[:, 2], d[:, 3], d[:, 5], d[:, 6]
    # MATLAB rebuilds time as a uniform ramp from the first step
    step = time_ms[1] - time_ms[0]
    time_ms = time_ms[0] + step * np.arange(len(time_ms))
    return _frame(time_ms, torque, angle, velocity)


def load_biodex(path: str | Path) -> pd.DataFrame:
    """Load a Biodex export as a DataFrame with ``ikd1d.schema.COLUMNS`` (time in seconds)."""
    lines = _read_lines(Path(path))
    if len(lines) < 4:
        raise ValueError(f"{path}: too short to be a Biodex export")
    return _load_legacy(lines) if lines[3].strip() == "" else _load_v5(lines)
