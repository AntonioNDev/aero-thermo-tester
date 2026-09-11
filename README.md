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

## Start here
1. Read `docs/formulas.md` — every equation you'll need, explained in plain English.
2. Read `docs/architecture.md` — how Python and MATLAB should talk to each other, and why.
3. Follow `TODO.md` top to bottom. It's ordered so each phase is small, testable,
   and demoable on its own — you should be able to screenshot progress after every phase.

## Folder map

```
aero-thermo-tester/
├── README.md              this file
├── TODO.md                step-by-step build plan
├── LICENSE                MIT
├── requirements.txt       pip dependencies
├── environment.yml        conda alternative
├── .gitignore
├── config/
│   └── settings.yaml      default physical constants & sim defaults
├── docs/
│   ├── formulas.md        every formula you need, explained
│   ├── architecture.md    Python/MATLAB integration design + rationale
│   └── resources.md       further reading
├── data/
│   ├── models/            drop .stl/.obj files here (Phase 1)
│   └── outputs/           generated results, figures, benchmark CSVs
├── notebooks/             scratch space for prototyping formulas
├── tests/                 unit tests (Phase 9)
└── src/
    ├── python/
    │   ├── geometry/      mesh generation + loading (Phase 1)
    │   ├── simulation/    aero + thermal physics (Phase 3, 4)
    │   ├── analysis/      weak-point scoring + suggestions (Phase 5)
    │   ├── visualization/ 3D rendering (Phase 2, 4)
    │   ├── ui/             Streamlit app (Phase 8)
    │   └── utils/         shared helpers, config loading, .mat I/O
    └── matlab/            the one scoped MATLAB piece (Phase 7)
```

## Why this is a good portfolio piece
- **Data manipulation:** mesh math, vectorized numpy force/pressure calculations
- **Data visualization:** interactive 3D pressure and heat maps, drag/lift charts
- **Python breadth:** numpy, parallel computing (numba/multiprocessing), a real UI
- **Domain depth:** you'll be able to explain the actual physics, not just "I called a library"

Keep this README's folder map accurate as you build — an out-of-date README is
one of the first things that makes a portfolio repo look unfinished.
