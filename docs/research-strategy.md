# Proof strategy from the opening

## Objective and current boundary

Prove `H_v \ R_v ≠ ∅` for at least one of W, D-WDL, D-DTD, or L in the [opening model](problem.md), or obtain a stronger chess-specific theorem about all optimal opening paths. A successful material prohibition needs two independent certificates: one legal history to an outcome-compatible state (`M∈H_v`), and one universal exclusion covering **every** fully optimal opening path (`M∉R_v`). A local source-to-target exclusion, a principal variation, and a game-theoretic recursion do not supply the second certificate.

The [retained endgame theorems](model-and-theorems.md) provide exact boundaries and concrete transition relations. The [local saturation data](results.md#five-man-layer-and-global-reachability) show that every admissible target through five pieces has a strict path from at least one six-piece local state. Thus a proof based only on a universal low-piece *material-origin* barrier is a poor primary bet. The missing information is an opening-specific restriction on **which full states, turns, ranks, and resource histories** can enter that layer optimally.

## Main proof architecture: backward resource slice plus a sound optimal cut

For a target material family `T`, first derive necessary facts about **every legal history ending in T**. Track original queens, each pawn resource and its promotion, the survival of original pieces, captures by color, bishop-square provenance when needed, total-piece layers, and turn at each irreversible event. This backward slice is a proof about the unrestricted legal game; it must not silently assume an optimal opening.

Next choose a first-entry frontier `F` that every such history crosses. A frontier is a set of **full-state predicates**, not just material labels. Its cover proof should use resource monotonicity and unavoidable events, so it can be checked without knowing `V(s₀)` or `DTM(s₀)`. Represent same-layer quiet moves and promotions explicitly; a capture-only material graph loses paths.

Finally exclude all optimal continuations through `F` by one of three mechanisms:

1. **Rank budget for W or L.** At each covered entry, certify an upper bound on its no-counter DTM and a strictly larger lower bound on legal plies to `T`. The [first-entry theorem](stages-d-f.md#stage-d-a-first-entry-barrier-theorem) then gives a global exclusion without an opening DTM value.
2. **Relational incompatibility.** Use the actual crossing relations and same-material closure, as in [Theorem A and the composition rule](model-and-theorems.md#2-material-abstraction-and-complete-finite-checks). Prove that all target-directed event orders have empty composition, even if every projected material edge exists separately. Preserve all equally optimal moves and defensive replies.
3. **Sound optimal-path abstraction.** Build an overapproximation containing every full-state optimal edge. A fixed point omitting `T` proves exclusion. Any pruned edge needs a certified WDL or DTM/DTD inequality; otherwise keep it. A reported abstract path is only a candidate counterexample until realized by compatible full states and an optimal prefix from `s₀`.

The cut is the hard new chess lemma. A cover of all *legal* target histories is sound but may be too broad; a cover of only one engine line is not sound. The aim is a compact intermediate cover based on irreversible resources, turn, and exact local bounds.

## First target sequence

| Role | Family | Why test it | Gate before using it in a theorem |
| --- | --- | --- | --- |
| Main W pilot | `KP–KQ⁹R²B²N²`, White win, reported in the original brief | All 16 Black resources survive, so White makes no captures before the target; all eight Black pawns must promote. This is a strong history invariant, and the brief reports a 19-to-18-piece local strict witness. | Recover and independently replay a full legal history, exact WDL/DTM certificate, and first-entry claim. The report in the brief is not yet a verified repository certificate. |
| Second W pilot | `KP–KQ⁹`, White win, reported in the brief | Nine queens force eight promotions and preservation of Black's original queen; an alleged 20-piece local witness and a 25-piece WDL-versus-DTM contrast can test the rank and event-order abstractions. | Same historical and value checks. The 79/80-ply lower bound alone cannot exclude an optimal path. |
| Calibration, not a global target | `KQ^a–K → KQ–K`, `a≥4`, and the 27 four-piece draw pair exclusions | Existing local data give exact negative examples and turn-sensitive boundaries. Queen-only decisive positions avoid castling, making this a cleaner model-transfer audit. | Recheck the selected exact boundary in the no-repetition opening rules. Never promote a source-to-target exclusion into a material-wide claim without a compulsory-source proof. |
| D-DTD pilot | A historically witnessed terminal-draw material with a mandatory promotion or last-capture pattern | The [promotion-fork theorem](result.md) and 27 local draw pair exclusions provide strict DTD obstructions. | Prove a D-preserving route or a finite DTD bound **inside** the draw region, then cover every last-entry alternative. The 19-ply Loyd game alone is only an `H_D` control. |
| D-WDL and L controls | Draw materials with WDL-only incoming barriers; color-reflected resource-rigid L families | D-WDL needs a value invariant because cycles destroy a distance budget. L must be analyzed from White-to-move `s₀`, not obtained by color reflection alone. | Produce historical outcome-compatible witnesses and a global cut for each case independently. |

The extreme W families are **pilots**, not assumed theorem targets. If their history or frontier gates fail, select a different target from the retained four-/five-piece negative matrices using few incoming event types, a short historical proof game, and a locally checkable value. The 31-piece mates and 26-piece stalemate already verified in [Stage B](stage-b-targets.md) serve as controls for `H_W`, `H_L`, and `H_D`, not as presumed forbidden materials.

## Ordered work and decision gates

1. **Model and evidence audit.** For each selected old theorem, record terminal rules, DTD-0 versus DTD-3, castling, en passant, side to move, and exact data rows. Re-run `scripts/reproduce.py structure`; reproduce only the critical exact boundary, not all large tables. **Pass:** a self-contained local statement in the opening model, or an explicit model-mismatch lemma.
2. **Historical witness recovery.** Locate or reconstruct the two extreme certificates reported in the brief. Check SAN/UCI from `s₀`, first entry into the stated piece layer, target material, all opponent alternatives in the local DTM proof, and the no-counter metric. **Pass:** machine-readable proof game plus independently checkable WDL/DTM certificate. **Fail:** keep the family as an unverified candidate, never use it as `H_W` evidence.
3. **Backward event lemma.** For one certified target, derive all mandatory promotion, capture, survival, and turn constraints. Enumerate *event types*, not board layouts. **Pass:** a finite cover of every legal first entry into a chosen layer. A single missed route invalidates the cover.
4. **Falsify the proposed cut.** Search the relaxed, resource-aware relation for a compatible chain into the target. Validate any found chain in full positions. If a legal or locally strict counterpath exists, refine the predicates or change target; never relabel `UNKNOWN` as `NO`.
5. **Prove the optimal cut.** Apply a verified rank inequality, an exact relational obstruction, or an inductive invariant on every covered entry and every equally optimal successor. Show the cut separates `s₀` from all target positions, not merely one FEN or one material word. **Pass:** a checkable `M∉R_v` proof that does not assume the opening value beyond the named conditional case.
6. **Assemble and verify.** Pair the exclusion with an independent `M∈H_v` certificate. State W, D-WDL, D-DTD, and L conclusions separately. Re-run minimal certificate checkers, compare the critical local values with an independent source where metrics match, and document what remains conditional.

After two substantive failed refinements of a target frontier, stop expanding tables for that target and switch family or abstraction. A failure is informative only if it identifies a real alternate event order, an unsound WDL/DTM pruning step, or a demonstrably intractable cover. A short legal stalemate path does not bound DTD without drawn intermediate states; a color reflection does not solve the Black-win opening case; and an optimal path from a local endgame state does not supply an optimal prefix from `s₀`.

## First concrete deliverable

Produce a **target dossier** for `KP–KQ⁹R²B²N²`: a verified historical game and local value certificate (if recoverable), a resource ledger proving that Black loses no original resource and White makes no capture before first target entry, a list of all possible last irreversible event types, and one proposed first-entry cut with a clearly stated cover proof or a concrete counterpath. In parallel, audit the queen-only `KQ^a–K → KQ–K` boundary under the opening rule model. This creates either the first usable global-proof frontier or a precise reason to move to the second W pilot.

## Execution checkpoint

| Gate | Observed result | Consequence |
| --- | --- | --- |
| Model transfer of a decisive local barrier | The [focused queen-only regeneration](../scripts/reproduce_queen_boundary.py) reproduced zero White-to-move strict paths from `KQQQ–K` to `KQ–K`, 8,611 Black-to-move paths, matching released statistics with zero Bellman errors. The [opening-model transfer](result.md#transferred-queen-only-dtm-barrier) is proved. | The turn-sensitive boundary is usable on an actual optimal opening path **if** its source occurs; it does not exclude the target material globally. |
| WDL boundary and draw-policy falsification | The [focused pawn/queen regeneration](../scripts/reproduce_pawn_queen_boundary.py) found zero queen-to-move WDL paths to `KP–K` for a pawn-side win, but one canonical drawn exception. The exception has a legal three-ply D-WDL path and a one-ply D-DTD stalemate shortcut. | A second W/L conditional trajectory theorem transfers; the corresponding D-WDL extension is false locally. |
| 18-piece White-win pilot | The [resource ledger](target-dossier-18.md) proves 14 Black captures, eight Black queen promotions, full Black survival, White-to-move first entries at layers 31 through 18, and three possible final-event types. | The claimed historical White-win and DTM-3 records remain unavailable. `H_W` is unverified for this material; the ledger supplies no optimal-prefix exclusion. |
| 12-piece White-win fallback | The [fallback ledger](target-dossier-12.md) proves the six White captures and 14 Black captures, but first-entry turn is not fixed. | Its claimed historical/DTM certificates are also unavailable, and its frontier is less constrained than the 18-piece pilot. |
| Verified draw target | The [Loyd material](target-dossier-draw.md) is in `H_D`; White makes all six captures and Black moves after each piece-count entry. | A D-preserving opening prefix or other WDL cut is still missing; the 19-ply game is not a DTD bound. |

The resource-only pilots have reached the plan's stopping gate: both nine-queen families lack checkable historical/value certificates, and the 12-piece family has a weaker cut. No larger table search is justified by these facts. The next decisive input is either a recovered extreme certificate **or** a new opening-prefix invariant for a target with already verified `H_v`. Until then, the proved deliverables are the two transferred trajectory restrictions, the resource ledgers, and the concrete D-WDL versus D-DTD counterexample; `H_v\R_v≠∅` remains unproved.
