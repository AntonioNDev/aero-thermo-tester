# TODO — Build Roadmap

Work top to bottom. Each phase should end with something you can screenshot or
demo — that's what makes a portfolio project, not a pile of half-finished
features. Don't start a phase until the previous one has a working demo, even
a rough one.

## Phase 0 — Decisions & environment (before writing any code)
- [ ] Decide MATLAB's exact role now, in writing, in `docs/architecture.md`
      (a recommendation is already drafted there — confirm it or change it).
      Vague "Python + MATLAB" scope is the #1 way this kind of project stalls.
- [ ] Install Python 3.11 or 3.12. If you plan to use the MATLAB Engine API
      (Option 2 in `architecture.md`), check MathWorks' supported-Python-version
      table for *your* MATLAB release first — it changes between releases.
- [ ] Create a virtual environment, install `requirements.txt`
- [ ] If using the Engine API: confirm `matlab.engine` imports cleanly.
      If using the `.mat` file exchange instead, skip this — that's the point.
- [ ] `git init`, first commit = this scaffold

## Phase 1 — Geometry (the object in the "wind tunnel")
- [ ] Start with primitives only: box, sphere, cone — generate procedurally
      with numpy/trimesh, no external files needed yet
- [ ] Represent **every** object the same way internally: a triangular mesh
      (vertices + faces). This is the single most important design decision —
      once plane, ball, block, and human are all "just a mesh," every later
      phase (pressure calc, visualization, weak-point scoring) works identically
      on all of them
- [ ] Add mesh loading (STL/OBJ) so you can later drop in a plane or human
      model from a free source (NASA 3D Resources, Sketchfab, Thingiverse) —
      this is what makes "literally anything" true
- [ ] Compute and cache per-face normals and areas — needed in Phase 3
- [ ] **Demo:** load 2–3 shapes, print vertex/face counts, render one with
      matplotlib or pyvista

## Phase 2 — Basic 3D visualization
- [ ] Render the mesh in 3D with pyvista (recommended) or plotly
- [ ] Add a wind direction arrow/vector to the scene
- [ ] Add rotate/zoom camera controls (pyvista gives you this for free)
- [ ] **Demo:** object floating in a scene with a wind arrow, rotatable

## Phase 3 — Aerodynamic simulation (core physics)
Read `docs/formulas.md` sections 1–4 first.
- [ ] Compute dynamic pressure from user-chosen wind speed
- [ ] Compute pressure coefficient per face with Modified Newtonian theory —
      this is one vectorized numpy expression across all faces, no loops
- [ ] Convert to pressure per face → force per face → sum to total force
- [ ] Decompose total force into drag and lift, compute Cd and Cl
- [ ] Compute center of pressure
- [ ] **Demo:** pick a shape + wind speed, print Cd, Cl, drag force in Newtons

## Phase 4 — Pressure & heat visualization
Read `docs/formulas.md` section 6 first.
- [ ] Color each face by pressure coefficient (your first real "wow" screenshot)
- [ ] Add skin-friction drag (section 5) so total drag isn't pressure-only
- [ ] Add the thermal layer: stagnation/recovery temperature and convective
      heat flux per face, color-mapped the same way — this is what actually
      makes it a *thermodynamics* tester, not just an aero one
- [ ] Add a legend/colorbar and a small readout panel (Cd, Cl, max surface temp)
- [ ] **Demo:** side-by-side pressure map and heat map on the same object

## Phase 5 — Weak point detection & suggestions
Read `docs/formulas.md` section 7 first.
- [ ] Compute a per-face "risk score" from local pressure gradient + local
      curvature (angle between adjacent face normals)
- [ ] Flag the top N faces by risk score, highlight them on the mesh
- [ ] Write a small rule-based suggestion engine — a handful of if/else rules
      is fine and honest, don't oversell it as "AI": e.g. "sharp edge near
      [coords] → consider a fillet", "high frontal pressure zone → consider
      a sloped leading surface"
- [ ] **Demo:** object with 3–5 highlighted weak points and matching suggestions

## Phase 6 — Performance & parallel computing
- [ ] Confirm Phases 3–5 are fully vectorized (no `for face in mesh.faces`
      Python loops) — this alone removes most lag
- [ ] Profile with `cProfile`/`%timeit` *before* optimizing further — don't
      parallelize blind
- [ ] For any remaining hot loop, try `numba` (`@njit(parallel=True)` +
      `prange`) before reaching for multiprocessing — usually faster and
      simpler for numeric array loops
- [ ] Use `multiprocessing`/`joblib` only for genuinely independent,
      coarse-grained work — e.g. sweeping many wind speeds/angles or multiple
      objects at once — not per-face math numpy already vectorizes
- [ ] If MATLAB owns the heavy numeric piece, use its Parallel Computing
      Toolbox (`parfor`) there and benchmark it against the numpy/numba path —
      a "numpy vs numba vs MATLAB parfor" chart is genuinely good portfolio content
- [ ] **Demo:** a before/after timing chart for at least one optimization

## Phase 7 — MATLAB integration
- [ ] Implement the specific piece scoped in Phase 0
- [ ] Keep the interface narrow: one function in, one struct/array out
- [ ] Prefer the `.mat` file exchange (`scipy.io.savemat`/`loadmat`) unless
      you specifically want to demonstrate the live Engine API — the file
      exchange means anyone can run your Python demo without owning MATLAB,
      which matters for a portfolio piece people will actually try
- [ ] **Demo:** a result that only exists because MATLAB computed it, clearly
      labeled as such in the UI

## Phase 8 — UI
- [ ] Build a single-page Streamlit app: object picker (your primitives +
      "upload your own mesh"), wind speed slider, wind direction control, run button
- [ ] Wire it to Phases 3–5's outputs: 3D pressure/heat view, Cd/Cl/temp
      readout, weak-point list with suggestions
- [ ] Add a loading state — simulations shouldn't freeze the UI (this is also
      where Phase 6's optimization work pays off visibly)
- [ ] **Demo:** the whole pipeline, object → suggestions, driven from the UI

## Phase 9 — Tests & validation
- [ ] Unit tests for the pure-math functions (Cp formula, Reynolds number,
      force integration) — easy to test against hand-calculated values
- [ ] Sanity-check against known results: a flat plate perpendicular to flow
      should land near a textbook Cd (~1.1–1.3); a sphere should be much lower
      (~0.4–0.5 in the relevant Re range). If your numbers are wildly off, the
      bug is almost always a sign error or normal-direction error, not the physics
- [ ] Automate these sanity checks as real tests, not just one-off notebook checks

## Phase 10 — Portfolio polish
- [ ] Write a real top-level README with screenshots/GIF of the running app
- [ ] Record a 30–60s demo clip
- [ ] Add a "Limitations & assumptions" section (Newtonian theory isn't full
      CFD, no turbulence modeling, etc.) — being explicit about this reads as
      engineering maturity, not weakness
- [ ] Push to GitHub, tag a v1.0 release

## Common ways this stalls (and how to avoid them)
- **Trying to do full CFD (Navier–Stokes).** Don't. `formulas.md` gives you a
  fast, honest, vectorizable approximation on purpose. Full CFD is a PhD
  topic, not a portfolio weekend project.
- **Starting with the human/plane mesh instead of a cube/sphere.** Primitives
  let you validate the physics against known Cd values before geometry
  complexity enters the picture.
- **Building the UI before the math works.** You'll end up debugging physics
  through a slow UI layer. Prove Phase 3 in a plain script or notebook first.
- **Deciding MATLAB's role halfway through.** Pin it down in Phase 0 and don't
  revisit until Phase 7.
