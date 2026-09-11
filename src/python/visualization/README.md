# visualization (Phase 2, 4)

3D mesh rendering (pyvista recommended, plotly as an alternative — see
`docs/architecture.md`), scalar field coloring (pressure map, heat map),
wind direction vector, legend/colorbar.

Design this to take a mesh + any single per-face scalar array and color it —
one function, reused for both the pressure map and the heat map, rather than
writing two near-duplicate rendering functions.
