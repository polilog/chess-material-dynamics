# Stage C — first nonconstructive-existence attempts

**Status:** no proof of `H_v \ R_v ≠ ∅` in any case. The attempts below isolate exact missing hypotheses and prevent a local observation from being reported as a global theorem.

## Attempt 1: count materials on one optimal game

In a decisive case, every fully optimal game has the same DTM length, so any *one* such game visits at most `DTM(s₀)+1` states. This does not bound `R_v`, which is the union over **all** equally optimal games. Even a finite graph with one binary choice at each of `k` levels can have exponentially many optimal paths and visit many distinct material labels. The [Stage A reduction](stage-a-complexity.md) gives a stronger warning: a monotone resource can be present on every optimal path in one instance and absent from all of them in another, depending on an embedded WDL question. Counting a principal variation gives no nonconstructive existence proof.

## Attempt 2: force a target beyond the DTM horizon

Let `τ(M)` be a proved lower bound on the earliest legal ply at which material `M` can occur from `s₀`. If `V(s₀)` is decisive and a separate proof gives `DTM(s₀)<τ(M)`, then `M∉R_v`, because each strict optimal ply reduces DTM by one and the game ends by ply `DTM(s₀)`. With a historical state of material `M` and value `v`, this would prove `M∈H_v\R_v`.

For a side to have nine queens, the proved lower bound is 79 plies if White has them and 80 if Black has them. The research brief reports extreme outcome-compatible local positions, but their historical and WDL/DTM certificates were not found in the inspected release. More importantly, **no** bound below 79/80 on the appropriate `DTM(s₀)` has been proved. This route currently requires an opening result of exactly the kind it was meant to avoid. Increasing the promotion count cannot exceed eight pawn promotions and does not remove that dependency.

## Attempt 3: use an early cooperative stalemate in D-DTD

The verified 26-piece Loyd stalemate occurs after 19 legal plies; a separate all-piece stalemate construction occurs after 24 plies. Neither bounds `DTD(s₀)` conditional on a drawn opening. DTD is computed inside the WDL-D subgraph, and no WDL proof was found for every intermediate state of either construction. The [small arena counterexample](stage-a-complexity.md#a-short-cooperative-draw-does-not-bound-dtd) shows this inference fails in general: a short legal route to a terminal draw may pass through a winning state even when the start is drawn. Thus no D-DTD material has been excluded from `R_D-DTD` by these constructions.

## Attempt 4: lift a local endgame barrier without a compulsory entry

The [previous release](prior-work.md) reports source-specific exclusions, for example `KQ^a–K → KQ–K` under strict DTM for `a≥4` in its local model. If a fully optimal opening game reaches the source material with matching value and rules, that **particular** continuation to the destination is excluded. The destination may still be reached through another material history. A global material prohibition requires proof that *every* optimal path from `s₀` to the target crosses a forbidden boundary. No such opening-to-boundary lemma has been established.

## Decision after these attempts

The best next target is not yet a named exotic material. It is a **frontier lemma**: find a material family with a verified member of `H_v`, then prove that every optimal first entry into a selected lower piece-count layer lies in a compact set of full-state predicates (turn, WDL, rank bound, and irreversible provenance) from which the target is impossible. The proof must retain all equally optimal moves and all opponent responses. An abstract graph containing all legal moves is sound but likely too coarse; one containing only a chosen engine line is unsound. This is the concrete chess-specific condition the literature transfer audit leaves open.
