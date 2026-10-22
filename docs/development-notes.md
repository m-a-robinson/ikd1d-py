# Development notes

Running record of points to remember, by phase. Add to it as work proceeds.

## Process
- Original repo `m-a-robinson/ikd1d` is never modified. All work is in `ikd1d-py`.
- One branch per phase, merged to `main` by pull request (Phase 0 = PR #1).
- Legacy MATLAB lives untouched in `legacy/matlab/` and is the reference implementation.

## Phase 0 – skeleton
- Package layout `src/ikd1d`, hatchling build, ruff + pytest, CI on Python 3.10 and 3.12.
- **Licence unresolved:** `LICENSE` is GPLv3, MATLAB headers say BSD-2-Clause (© 2020 LJMU).
  `pyproject.toml` currently says BSD-2-Clause with a TODO. Decide and add a top-level LICENSE.

## Phase 1 – loaders
- Canonical schema: `time` (s), `torque` (N·m), `angle` (deg), `velocity` (deg/s). MATLAB used ms.
- Biodex angle is `POS (ANAT)`; `POSITION` is discarded (as MATLAB).
- Cybex torque sign is restored from angle direction (flip where `angle[i] < angle[i+1]`).
- **Biodex v5 layout is untested on real data** (ported from MATLAB; no sample). Need a real file.
- MATLAB turned every `-` into `0` (corrupting negatives); Python only replaces a standalone `-`. Confirm.
- Cybex sample ends with a junk row (status 0000, angle 0). Kept for parity; trim in `segment`.
- MATLAB "Other" import format not ported (unclear spec).
- Locale: MATLAB had Belgian-locale workarounds for `xlsread`; Python parses with explicit rules.

## Phase 2 – golden regression
- `tools/octave/golden_load.m` copies the MATLAB loader statements and writes `tests/golden/*.csv`
  (ms units). Octave 8 on Ubuntu: `apt-get install octave`.
- Deviation from pure MATLAB: `xlsread` (needs Octave `io` package) is replaced by `dlmread` on the
  CSV with quotes stripped. Everything after that is verbatim.
- **Limit:** the MATLAB processing functions read parameters from GUI handles and mutate globals, so
  they cannot be called headless. Golden output for gravity correction, segmentation, auto-select
  and fits needs small MATLAB/Octave wrapper scripts that set the globals and call the
  `polyCurveFitting`/`autoSelect*` bodies, or a real MATLAB session to export intermediate results.
  Prefer capturing outputs from MATLAB itself for those stages if available.
- Tolerance: loader outputs compared to 1e-9 (identical parsing); expect looser tolerances for fits.

## Backlog / future
- Phase 1 remaining: `correction`, `segment` (incl. auto-select), `fit` (poly + moving average),
  `resample`.
- Phase 3: CLI, notebooks, optional GUI. Phase 4: 1D stats (`spm1d`), more manufacturers, PyPI.
