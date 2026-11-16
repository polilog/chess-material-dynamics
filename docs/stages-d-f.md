# Stages D–F — barrier, conditional conclusions, and use

**Status:** a proved transfer criterion and one chess-specific trajectory restriction, but no proof that `H_v \ R_v` is nonempty for the standard opening. The distinction matters: a sound certificate format is useful only after its hypotheses are discharged for a concrete target.

## Stage D: a first-entry barrier theorem

Let `T` be the full-state target consisting of positions with a chosen material `M`. For a full state `s`, let `ℓ(s,T)` be any proved lower bound on the number of **legal** plies needed to first reach `T` from `s`, with `∞` allowed. It may come from pawn moves, captures, piece placement, turn, or a more detailed invariant. It must count paths through the unrestricted legal graph; computing it in a graph that silently removes defensive moves would be unsound.

**Theorem (rank-budget first-entry barrier).** Fix a decisive case `v∈{W,L}`. Let `U` contain every full state that first enters a chosen material layer on any fully optimal game from `s₀` that later reaches `T`. Suppose every `s∈U` of value `v` has a certified DTM `d(s)` with `d(s)<ℓ(s,T)`. Then `M∉R_v`. If there is independently a legal history from `s₀` to a state of material `M` and value `v`, then `M∈H_v\R_v`.

**Proof.** Assume an optimal game reaches `T`. Its first entry `s` into the chosen layer is in `U`. Primary optimality preserves the initial decisive value `v`, so `V(s)=v`. Every following optimal ply decreases DTM by exactly one; the game terminates after exactly `d(s)` further plies. A path first reaching `T` requires at least `ℓ(s,T)>d(s)` legal plies, a contradiction. The independent historical witness gives the second assertion. ∎

This criterion does **not** require a value or DTM for `s₀`. It requires a sound cover of *all* relevant first-entry states and exact or safe upper bounds for their DTM. The cover can be made outcome-independent by including every historically reachable first entry; even all statically legal layer states give a sound but probably too large cover. A certificate can be checked by (i) a proof that the cover includes every possible first entry, (ii) local DTM bounds under the stated rules, and (iii) legal-path lower bounds. None of the three may be inferred from one engine line.

The same proof applies to D-DTD if every covered drawn entry has finite `DTD(s)<ℓ(s,T)`, since each optimal ply decreases finite DTD. It does not apply to D-WDL, which has no decreasing distance rank and may retain cycles. If a local certificate covers only one source material or one turn, it excludes only paths through that source, not the target globally.

### A chess instance with a certified local barrier

The [promotion-fork theorem](result.md) supplies an instance of this logic that is independent of the opening value and avoids a tablebase. At any drawn `KP–K` state immediately before legal promotion, bishop or knight promotion produces a terminal dead-position draw in one ply. Hence `DTD=1`. A proposed *nonterminal* `KQ–K` or `KR–K` position requires one promotion ply and at least one further ply to continue an optimal game, exceeding the one-ply terminal-draw budget. The resulting ordered-material prohibition is genuine for a fully optimal game from `s₀` conditional on `V(s₀)=D`, but it is **not** a prohibition of either heavy-piece material itself. A terminal stalemate after queen or rook promotion remains possible.

### Attempts at a target-wide certificate

- **Nine-queen W target.** The 79/80-ply historical lower bound is proved, but it is measured from `s₀`. No bound on `DTM(s₀)` below it is known here, and a historical outcome-compatible witness has not been reproduced. The rank-budget theorem cannot yet certify this target.
- **Loyd stalemate material in D-DTD.** Its 19-ply legal history proves `H_D`, but may pass through non-drawn states. It supplies neither a finite bound for `DTD(s₀)` nor a first-entry cover. The [abstract counterexample](stage-a-complexity.md#a-short-cooperative-draw-does-not-bound-dtd) proves this inference would be invalid in general.
- **Small-piece local pair barriers.** The [retained local theorems](model-and-theorems.md#3-general-material-barriers-from-exact-boundaries) supply local exclusions. The queen-only DTM barrier has now been [regenerated and transferred](result.md#transferred-queen-only-dtm-barrier) to the opening rule model, but no checked cover shows every fully optimal opening path to `KQ–K` crosses the four-queen source class. Material projection alone cannot supply that cover because consecutive projected edges can require incompatible middle positions.

These three failures have distinct causes: unknown opening rank, unproved WDL of a legal draw path, and missing compulsory entry. Adding more local positions does not resolve any of them without a structural lemma.

## Stage E: conclusions by initial outcome

| Conditional initial case | Established chess statement | Established compatible historical material | Global `H_v\R_v` conclusion |
| --- | --- | --- | --- |
| W with strict DTM | DTM falls by one on every optimal ply; the rank-budget barrier applies to any fully covered entry layer. The transferred `KQ^a–K → KQ–K` strict-DTM exclusion and `KP–KQ^a → KP–K` pawn-side-win WDL exclusion hold under their source hypotheses. | Two 31-piece White-mate materials are replayed from the opening, including one with all Black resources intact. | Unknown: no complete entry cover or target-wide rank certificate. |
| D-WDL | Every optimal move remains in the drawn WDL region; cycles and infinite optimal games are allowed. A [local concrete path](result.md#transferred-pawn-versus-queens-wdl-barrier) shows why a winning-side WDL barrier does not extend automatically to draws. | The 26-piece Loyd terminal stalemate material is replayed. | Unknown: the short legal game is not certified draw-preserving throughout. |
| D-DTD | Finite DTD falls by one; the `KP–K` promotion fork forbids a nonterminal heavy-piece continuation on any fully optimal game containing that segment. `R_D-DTD⊆R_D-WDL`. | The same 26-piece terminal stalemate material belongs to `H_D`. | Unknown: the trajectory restriction does not exclude a material globally. |
| L with strict DTM | The rank-budget barrier works with Black as winner. Both the queen-only and pawn-side-win exclusions transfer after color reflection **if** an optimal opening path actually reaches their Black-side source; color exchange does not create that prefix. | A 31-piece Black-mate material is replayed from the opening. | Unknown: no complete entry cover or target-wide rank certificate. |

The historical witnesses are checked by [the replay script](../scripts/verify_historical_witnesses.py). A terminal mate or stalemate proves the final WDL value in the chosen rules. The script does not classify intermediate positions or any optimal opening prefix.

## Stage F: what can be used now

The promotion-fork theorem can remove a *specific ordered segment* from a D-DTD optimal-path search. It cannot remove every `KQ–K` or `KR–K` state, because either might arise through another legal history or as a terminal draw. More generally, a strict DTM barrier can prune paths when proving **all strict DTM-optimal games**, but it does not automatically let a WDL solver ignore a defender move: a slower losing defense may still matter to the WDL proof. A WDL-pruning certificate needs a value-preserving simulation or a complete attractor argument of its own.

The abstract-game reduction in [Stage A](stage-a-complexity.md) is a formal warning about information loss; it is not a chess hardness theorem. The first-entry barrier is a general sufficient certificate, not a new game-theoretic classification. The promotion fork is a chess-specific conditional theorem already foreshadowed in the previous local release. No mathematical priority or global forbidden-material claim follows from the literature search. The most valuable next experiment is to choose a small historically verified target family and produce a **sound, finite first-entry cover** with local rank bounds. If that fails because the cover spans arbitrary opening play, the target or abstraction should be changed before computing larger endgame tables.
