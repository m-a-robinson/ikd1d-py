"""Canonical data layout shared by every loader and processing step.

Replaces the MATLAB globals TIMECOL/TORQUECOL/ANGLECOL/VELCOL.
"""

COLUMNS = ("time", "torque", "angle", "velocity")  # s, N·m, deg, deg/s
