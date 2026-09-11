# tests

Unit tests, built in Phase 9. Test the pure-math functions in
`src/python/simulation` and `src/python/analysis` against hand-calculated or
known textbook values — e.g.:

- A flat plate perpendicular to flow should land near Cd ~1.1-1.3
- A sphere should land much lower, roughly Cd ~0.4-0.5 in the relevant
  Reynolds number range

If your numbers are wildly off, the bug is almost always a sign error or a
face-normal-direction error, not the underlying physics — check that first.
