# analysis (Phase 5)

Per-face risk scoring (pressure gradient + local curvature, see
`docs/formulas.md` §7), weak-point flagging (top-N by risk score), and the
rule-based suggestion text generator.

Keep the "suggestion engine" honest about what it is: a handful of if/else
rules driven by geometry and physics signals, not a learned model. That's a
perfectly good, explainable portfolio feature — don't oversell it.
