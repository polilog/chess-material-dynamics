# Retained local endgame research and its transfer limits

The original endgame study from commit [`457fc79d507e`](https://github.com/polilog/chess-material-dynamics/tree/457fc79d507ef5c3c78b5450f964f1df438976ca) is restored in the current working tree. Its [mathematical model and proofs](model-and-theorems.md), [consolidated tables](results.md), [reproduction guide](reproduction.md), `results/`, `proofs/`, `src/`, and verification scripts are part of this project. They should be cited directly rather than treated as unavailable historical artifacts.

## Results retained

- The local study reports complete WDL, DTM, and shortest-draw classifications through four pieces, plus eight exact five-piece materials. It distinguishes individual material edges, material words, and endpoint pairs; projected edges can fail to compose into a concrete optimal path.
- Its [general barrier table](model-and-theorems.md#3-general-material-barriers-from-exact-boundaries) includes `KQ^a–K → KQ–K` for `a≥4` under winning-side DTM, `KQ^aR–K → KR–K` for `a≥3`, and `KP–KQ^a → KP–K` for `a≥2` under the stated outcome and metric conditions. These are genuine source-to-target restrictions in the local model, not claims that the destination material is absent from all optimal opening games.
- Its first-capture and turn-sensitive boundary arguments propagate exact small-layer exclusions to larger formal material families. The source class, side to move, WDL value, and draw metric are part of each hypothesis.
- Its positive certificates reach every admissible target through five pieces from at least one six-piece local state. This local saturation coexists with strong pairwise barriers; it does not establish a path from the standard opening.

## Verification performed in this session

`python3 scripts/reproduce.py structure` passed after restoration. It checked all five-piece candidate keys, 134,918 negative pair rows, 1,002 propagated exclusions, and legal replay of the released strict positive FEN/UCI paths. This is a structural and witness-replay check. The large binary endgame tables were not regenerated, and every numerical classification has not been independently compared with an external tablebase. See the [original verification record](reproduction.md#release-verification) for the release's own checks.

## Transfer to the opening problem

The old states are locally legal, not necessarily historically reachable from `s₀`. The old solver omits castling, and one shortest-draw variant ends on a fresh third occurrence; the current opening problem permits unlimited repetition and has no move-count draw. DTD-0 is the relevant local draw metric, but a transfer still needs matching full states and legal options. A local exclusion constrains an optimal opening game **if that game enters the specified source class under matching rules**. To exclude a destination material from every optimal opening game, one must additionally prove that all such games enter a covered source class, or supply another global barrier. The retained data are valuable components of that proof, not a completed opening theorem.
