# Aerodynamics & Thermodynamics Tester

Portfolio project: put a 3D object — a plane, a block, a ball, a human, literally
anything — into a virtual wind tunnel, run a simplified aerodynamic + thermal
simulation, visualize pressure/heat/drag on the object, flag likely weak points,
and get shape-improvement suggestions.

**Stack:** Python (numpy, scipy, pyvista/plotly, streamlit) does orchestration,
geometry, physics, and visualization. MATLAB owns one clearly-scoped numerical
piece — see `docs/architecture.md` for exactly what and why.

This repo is intentionally **just scaffolding**: folders, docs, formulas, and a
step-by-step plan. No app logic is written yet — that's for you to build, using
this as a map so you don't get stuck or lost in scope.
