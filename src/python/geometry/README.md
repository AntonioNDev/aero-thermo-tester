# geometry (Phase 1)

Mesh generation (primitives: box, sphere, cone) and mesh loading
(STL/OBJ, via `trimesh`) plus per-face normal/area computation.

Every object type — plane, block, ball, human, anything — should end up as
the *same* representation here: vertices + faces (+ cached per-face normals
and areas). Every later module (simulation, analysis, visualization) should
only ever need that representation, never object-type-specific logic.
