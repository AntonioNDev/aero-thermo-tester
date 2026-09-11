# Formulas Reference

Everything here is standard aerodynamics/heat-transfer material, written out
from general engineering knowledge rather than transcribed from one specific
source. If you need precise, citable numbers (not just qualitative/portfolio
results), cross-check exact coefficients against a primary reference — see
`resources.md`.

All formulas use SI units: meters (m), kilograms (kg), seconds (s), Kelvin (K),
Pascals (Pa), Newtons (N).

**Why Newtonian theory instead of "real" CFD?** Solving the Navier–Stokes
equations properly (real CFD) is a PhD-level topic and massive overkill here.
This document instead gives you a fast, fully vectorizable (numpy-friendly)
*approximation* that works on any triangular mesh — any object at all — at
the cost of accuracy. That trade-off is exactly right for a portfolio project:
be upfront about it in your README (see TODO Phase 10).

---

## 1. Fundamental quantities

| Quantity | Symbol | Typical value (sea level, 15°C) |
|---|---|---|
| Air density | ρ | 1.225 kg/m³ |
| Dynamic viscosity | μ | 1.81×10⁻⁵ Pa·s |
| Speed of sound | a | ~340.3 m/s |
| Specific heat ratio | γ | 1.4 |
| Prandtl number | Pr | ~0.71 |
| Thermal conductivity of air | k | ~0.026 W/(m·K) |

**Dynamic pressure:**
```
q = 0.5 * ρ * V²
```
`V` = freestream wind speed (m/s). This is the "how hard is the wind pushing"
term that every force calc below is built from.

**Reynolds number** (laminar vs. turbulent flow regime):
```
Re = ρ * V * L / μ
```
`L` = a characteristic length of the object (e.g. length along the flow direction).

**Mach number** (compressibility — matters more at high speed, e.g. a "plane" object):
```
M = V / a
```

---

## 2. Pressure over the surface — Modified Newtonian Impact Theory

This is the core of the whole simulation: a way to estimate pressure at
*every point on an arbitrary 3D mesh* using only geometry, no flow solver.

For each mesh face with outward unit normal **n̂**, and flow direction unit
vector **d̂** (the direction the wind is blowing):

```
windward face if:  n̂ · d̂ < 0   (face is angled into the oncoming flow)

Cp = Cp_max * (n̂ · d̂)²         for windward faces
Cp = 0                          for leeward/shadowed faces (n̂ · d̂ ≥ 0)
```

`Cp_max ≈ 2.0` is the classical Newtonian limit — use this as your starting
default (it's in `config/settings.yaml`). "Modified" Newtonian theory refines
`Cp_max` using normal-shock relations for more accuracy at true hypersonic
speeds; the classical value is a reasonable, defensible approximation for a
general-purpose tool like this one.

Convert to actual pressure:
```
P = P_infinity + Cp * q
```

**Honest limitation to note in your README:** Newtonian theory is strictly a
hypersonic approximation. Used here across all speeds, it's a fast qualitative
estimator — good for comparing shapes and finding relative weak points, not
for wind-tunnel-grade absolute numbers. This is exactly the kind of caveat
that makes a portfolio project read as mature engineering rather than
overclaiming.

---

## 3. Force integration

For each face `i` with area `A_i`, normal `n̂_i`, pressure `P_i`:
```
F_i = -P_i * A_i * n̂_i        (pressure pushes inward on the surface)
F_total = Σ F_i                (sum over all faces)
```

Decompose into drag (along flow) and lift (perpendicular, e.g. vertical):
```
D = F_total · d̂
L = F_total · ĥ                (ĥ = vertical/lift-direction unit vector)
```

Coefficients (need a reference area `A_ref`, see below):
```
Cd = D / (q * A_ref)
Cl = L / (q * A_ref)
```

**Reference/frontal area `A_ref`:** project the mesh onto a plane
perpendicular to `d̂` and compute the projected area. For convex shapes, a
quick approximation is `Σ A_i * max(0, -(n̂_i · d̂))` over windward faces; for
concave shapes (e.g. a human figure with arms and legs) this can double-count
overlapping projections — a proper 2D convex-hull-of-projected-vertices
approach is more correct if you need accuracy there.

---

## 4. Center of pressure

```
CoP = Σ(P_i * A_i * position_i) / Σ(P_i * A_i)
```
Useful for stability analysis and for weighting weak points — a large force
acting far from the center of mass produces more torque/stress than the same
force acting near it.

---

## 5. Skin friction (viscous) drag

Newtonian theory (section 2) gives you *pressure* (form) drag only. Add a
flat-plate skin-friction term for total drag:

```
Laminar:    Cf = 1.328 / sqrt(Re_L)
Turbulent:  Cf = 0.074 / Re_L^0.2          (valid roughly Re < 1e7)
            Cf = 0.455 / (log10(Re_L))^2.58  (higher Re)

Skin friction drag = Cf * q * A_wetted
Total drag = pressure drag + skin friction drag
```
`A_wetted` = total surface area of the mesh exposed to flow (sum of face areas).

---

## 6. Aerothermodynamics — heating from the airflow

This is what ties the project's name ("thermodynamics tester") to the physics:
air compresses and rubs against the surface, which heats it. This is real
engineering (relevant to aircraft leading edges, reentry vehicles) and gives
you a second, genuinely different scalar field to visualize alongside pressure.

**Stagnation temperature** (temperature where flow speed goes to zero, e.g.
the very front of the object):
```
T0 = T_infinity * (1 + (γ-1)/2 * M²)
```

**Recovery temperature** (more realistic value for the actual surface,
accounting for the boundary layer not being a perfect stagnation point):
```
Tr = T_infinity * (1 + r * (γ-1)/2 * M²)
r ≈ sqrt(Pr)     for laminar flow
r ≈ Pr^(1/3)     for turbulent flow
```

**Convective heat transfer coefficient** (flat-plate correlations — a
reasonable per-face approximation):
```
Laminar:    Nu = 0.664 * Re^0.5 * Pr^(1/3)
Turbulent:  Nu = 0.037 * Re^0.8 * Pr^(1/3)

h = Nu * k / L
```

**Heat flux into the surface** (Newton's law of cooling/heating):
```
q_conv = h * (Tr - Tw)
```
`Tw` = current wall/surface temperature (you can start with a fixed assumed
value, e.g. 288 K, and later let it evolve over time if you want a dynamic
simulation).

Color-mapping `q_conv` (or `Tr`) per face gives you a heat map exactly
parallel to the pressure map in section 2 — same mesh, same visualization
code, different scalar field.

---

## 7. Weak-point / structural proxy heuristics

Full structural FEA is out of scope, so use cheap geometric proxies instead —
this is standard engineering intuition, not a formula from a textbook:

- **Pressure gradient:** a big pressure *difference* between adjacent faces
  suggests a stress concentration.
- **Local curvature:** the angle between adjacent face normals approximates
  curvature. Small radius / sharp edges have both higher curvature *and*
  higher real-world stress concentration factors (a real, well-established
  structural fact — sharp fillets concentrate stress) *and* higher Cp spikes
  in Newtonian theory — so these two signals genuinely reinforce each other.

**Composite risk score per face** (starting point — tune the weights):
```
risk_i = w_p * normalize(pressure_gradient_i) + w_c * normalize(curvature_i)
```
Default weights are in `config/settings.yaml` (0.6 pressure, 0.4 curvature).

Rank faces by `risk_i`, take the top N, and drive your rule-based suggestion
text from there (e.g. high curvature + high pressure → "sharp edge in a
high-pressure zone — consider a fillet/rounding here").
