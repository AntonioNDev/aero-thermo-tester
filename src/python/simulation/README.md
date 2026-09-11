# simulation (Phase 3-4)

Dynamic pressure, per-face Cp (Modified Newtonian theory, see
`docs/formulas.md` §2), force integration, Cd/Cl (§3-4), skin friction (§5),
and the thermal layer (§6).

Keep this pure-numpy and fully vectorized — no Python `for face in faces`
loops, and no MATLAB calls made directly from here. If MATLAB is involved
(Phase 7), that belongs in a thin integration layer in `utils/`, not mixed
into the physics code.
