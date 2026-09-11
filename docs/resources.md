# Learning Resources

The formulas and reasoning in `formulas.md` come from general aerodynamics
and heat-transfer knowledge, not a transcription of one specific source.
Cross-check anything you rely on for correctness against a primary reference
before treating it as authoritative, especially exact coefficient values
(`Cp_max`, skin-friction correlations) if you need precision rather than a
qualitative, portfolio-level result. I don't have web access from here, so
treat the titles below as starting points to search for, not guaranteed
current links.

**Aerodynamics fundamentals**
- John D. Anderson Jr., *Fundamentals of Aerodynamics* — the standard
  textbook; the Newtonian theory and skin-friction material in
  `formulas.md` is the kind of content covered in its early chapters.
- NASA Glenn Research Center's "Beginner's Guide to Aerodynamics" (public
  NASA educational site) — much lighter weight, good for building intuition
  before the textbook.

**Aerothermodynamics / heat transfer**
- Frank Incropera et al., *Fundamentals of Heat and Mass Transfer* —
  standard reference for the convection formulas in `formulas.md` §6.

**Python performance**
- numpy vectorization guides (avoid Python-level loops over mesh faces)
- Numba documentation — specifically `@njit(parallel=True)` and `prange`
- `joblib.Parallel` for coarse-grained parallel batch runs (e.g. sweeping
  many wind speeds at once)

**MATLAB ↔ Python**
- MathWorks' official docs for the MATLAB Engine API for Python (check the
  Python-version compatibility table for your specific MATLAB release)
- `scipy.io.savemat` / `loadmat` docs for the file-exchange approach

**Visualization / UI**
- PyVista documentation (mesh scalar coloring, camera, plotting)
- Streamlit documentation
- `stpyvista` (community package for embedding PyVista in Streamlit), if
  you go that route
