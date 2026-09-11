# Architecture Notes

## Why "just numpy" isn't the whole story, and what MATLAB's job should be

Python/numpy should carry roughly 90% of this project: geometry, the
vectorized Newtonian pressure/force calc, visualization, UI, orchestration.
That's also where most of the portfolio value (data manipulation + data
visualization + Python fluency) actually lives.

MATLAB's job should be small, clear, and *optional to run* — the Python app
should degrade gracefully (e.g. show a cached/precomputed result) if MATLAB
isn't installed on whoever's machine is looking at your portfolio. Pick **one**
of the following, don't spread MATLAB across many small things:

- **Option A — Structural sanity check.** Treat the top-N flagged weak points
  (Phase 5) as simple beam/plate elements and compute a rough stress
  concentration or natural-frequency estimate in MATLAB, feeding into the
  "why this is a weak point" explanation.
- **Option B — Parallel computing showcase.** Re-implement the Phase 3
  force/pressure sweep — run it across many wind speeds/angles at once — in
  MATLAB using `parfor`, and benchmark it against the numpy/numba version.
- **Option C — Curve fitting / statistics.** Fit Cd-vs-Reynolds-number or
  Cd-vs-angle-of-attack curves from a batch of simulation runs using MATLAB's
  Curve Fitting Toolbox, and compare against known textbook curves.

**Recommendation for a first pass: Option B.** It's the cleanest to scope, it
directly demonstrates the "optimized and parallel" goal from the project
brief, and it doesn't duplicate physics you're already writing in Python.

## Python ↔ MATLAB integration: two options

**Option 1 — `.mat` file exchange (recommended to start)**
Python writes inputs (mesh faces/normals/areas, wind conditions) to a `.mat`
file with `scipy.io.savemat`; a MATLAB script/function reads it, computes,
writes results to another `.mat` file; Python reads them back with
`scipy.io.loadmat`.
- Pros: no MATLAB Engine/licensing dependency for anyone trying to run your
  Python demo; trivial to debug (just inspect the `.mat` files); same
  behavior whether you trigger MATLAB by hand or automate it later.
- Cons: not "live"/interactive; small round-trip latency.

**Option 2 — MATLAB Engine API for Python**
Python calls `matlab.engine.start_matlab()` and calls MATLAB functions
directly, in-process.
- Pros: live/interactive, no intermediate files.
- Cons: requires a licensed MATLAB install wherever the app runs, *and* a
  Python version MATLAB's engine supports for your specific MATLAB release
  — check MathWorks' compatibility table for your release rather than
  trusting an old note, since this changes across MATLAB versions.

**Start with Option 1.** It keeps the project runnable by anyone — important
for a portfolio piece people will actually clone and try — and you can add
Option 2 later as a "bonus" mode to show you know the Engine API too.

## Visualization stack

- **pyvista** — recommended primary 3D renderer. Built for exactly this
  (mesh + scalar field coloring), gives you pressure/heat color maps on the
  mesh almost for free, and can embed in Streamlit via the `stpyvista`
  community package.
- **plotly** — good alternative for browser-native interactivity without
  pyvista's VTK dependency; a bit more manual for per-face mesh coloring.
- **matplotlib** (`mplot3d`) — fine for quick Phase 1–2 sanity checks, too
  slow/clunky for the final interactive UI on larger meshes.

## UI

**Streamlit** is the recommended choice: fastest path from "script that
works" to "shareable interactive demo," minimal boilerplate, plays well with
pyvista/plotly, and is a common, well-understood choice for a portfolio piece
someone else can actually run locally.

## Data flow (high level)

1. **Geometry module** produces a mesh (vertices, faces, per-face normals + areas)
2. **Simulation module** takes mesh + wind conditions → per-face Cp, pressure,
   temperature, per-face force
3. **Analysis module** takes per-face results → risk scores, weak-point list,
   suggestion text
4. *(Optional)* **MATLAB module** takes flagged weak points or a parameter
   sweep → its specific scoped result
5. **Visualization module** takes mesh + any per-face scalar field → colored
   3D render
6. **UI module** wires user inputs → steps 2–5 → rendered output

Keep these as separate modules passing plain data (numpy arrays, dicts)
between them — not classes reaching into each other's internals. This keeps
the project easy to unit test and easy to explain clearly in an interview.
