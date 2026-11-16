# Stage A — logical dependence and complexity

**Status:** completed for explicit finite game graphs; the corresponding separation question for standard 8×8 chess remains open. This stage is about what can and cannot follow from general game theory before choosing a chess material target.

## Five different tasks

The following questions have different inputs and outputs, even though all refer to the same opening state in the chess application.

| Task | Information requested |
| --- | --- |
| Weak solution | The single value `V(s₀) ∈ {W,D,L}`. |
| Opening DTM and optimal play | If decisive, the exact minimax mate distance and **all** value-and-distance-preserving opening continuations. |
| Strong state classification | WDL and, where decisive, DTM for every historically reachable full state, with legal successor information. |
| One material target | Whether a specified outcome-compatible material lies in `R_v` or `H_v \ R_v`. |
| Existence of a prohibition | Whether `H_v \ R_v` is nonempty, without naming the material. |

Strong classification plus the legal graph is sufficient for all five tasks. Weak solution, even augmented by `DTM(s₀)`, is insufficient to reconstruct all optimal material paths: two finite arenas can have the same root value and root DTM while a second winning branch is tied in one arena and one ply slower in the other. Put a unique material label on that branch; the root's WDL and DTM agree, but `R_W` differs.

There is also a simple reverse implication that depends on **what the oracle returns**. Suppose an oracle reports the three actual, outcome-indexed optimal-reachability sets, with the two sets for outcomes that are not the actual value of `s₀` empty. The initial material `M(s₀)` belongs to exactly the set indexed by `V(s₀)`, because every optimal game contains `s₀`. Three membership queries therefore recover the opening WDL. An oracle that answers only a *conditional* question of the form “assuming `V(s₀)=v`, could `M` occur?” does not have this implication: the query already assumes the unknown outcome. Nor does the three-query observation recover opening DTM: two forced-chain games of lengths one and two can assign every state the same material label, giving identical material-reachability answers but different root DTM. This distinction prevents an accidental claim of independence based solely on conditional casework.

For an **explicit** finite graph with `n` states and `m` edges, the WDL regions are found by two reachability-attractor computations. In a decisive region, the winner's minimax DTM is finite and at most `n`: an attractor-rank strategy reaches mate within at most `n` transitions. Exact DTM and all optimal edges can be computed in polynomial time; ordinary graph reachability then produces `R_v`, while unrestricted reachability followed by WDL classification produces `H_v`. D-DTD uses shortest paths inside the drawn-state subgraph to terminal draws, with infinity on states having no such path. Thus material reachability is polynomial in the size of an **already explicit** complete game graph. This does not imply a feasible algorithm for chess, whose graph is not supplied explicitly.

## A reduction showing why a material question can encode WDL

**Theorem (abstract game family, not a chess reduction).** Consider finite two-player reachability games given by an explicit graph. White wins by reaching a designated terminal target; otherwise infinite play is a draw. Add a material label consisting of a single resource that can disappear but never return. Even when the new initial state is guaranteed to be a White win and there are only two material labels, deciding whether `H_W \ R_W` is nonempty is at least as hard, under a logspace reduction, as deciding whether White can force the target from an arbitrary state of the original reachability game. The same construction reduces that WDL question to membership of the resource-absent label in `R_W`.

**Construction and proof.** Let the original game be `G`, with `n` states and designated state `x`. Add a new White-owned root `p` with three choices:

1. Enter `x`, removing the resource on that first edge.
2. Enter a forced chain ending in a White-win terminal in exactly `n+2` plies from `p`, keeping the resource throughout.
3. Enter another forced chain ending in a White-win terminal in exactly `n+3` plies from `p`, removing the resource on its first edge.

All states of the original `G` branch and the third chain carry the resource-absent label `M`; `p` and the second chain carry the resource-present label. Forced-chain vertices may alternate owners, each with one successor. The new root is a White win regardless of the value of `x`. The resource-absent label belongs to `H_W` in every instance, because the third chain is a legal, historically reachable winning continuation, although it may be suboptimal.

If `x` is White-winning, its DTM is at most `n`; entering it gives a win in at most `n+1` plies from `p`. That is faster than either forced chain, so every optimal first move enters the `M`-labelled branch and `M∈R_W`. If `x` is not White-winning, entering it is WDL-suboptimal. Of the two guaranteed wins, the `n+2`-ply resource-present chain is strictly faster, so it is the only optimal first choice and `M∉R_W`. The initial resource-present label always lies in `R_W`. Consequently

`H_W \ R_W ≠ ∅` **if and only if** White cannot force the original target from `x`.

The gadget has `O(n)` new vertices and only one monotone material bit. It is computable in logarithmic workspace: copy the input edges and emit the two chains with an `O(log n)` counter. This proves a relative reduction for explicit graph games; it does **not** implement the gadget with legal chess positions, promotion, or the standard chess opening. The [reachability-games survey, §3.1.1](https://drops.dagstuhl.de/storage/00lipics/lipics-vol284-fsttcs2023/LIPIcs.FSTTCS.2023.1/LIPIcs.FSTTCS.2023.1.pdf) records that ordinary two-player zero-sum reachability games on explicit graphs are P-complete. Combined with the polynomial upper bound above and closure of P-completeness under complement, the constructed abstract resource-labelled decision problem is P-complete for that input family. The conclusion for chess is narrower: the smaller answer format and monotonicity of material **alone** do not establish an easier problem. Chess-specific geometry or an opening-specific invariant would be needed.

## A short cooperative draw does not bound DTD

Consider a turn-based arena with a Black-owned drawn vertex `b` and White-owned drawn vertex `w` forming a forced two-vertex cycle (`b→w→b`). Black may also move from `b` to a White-winning vertex `z`. At `z`, White can choose an immediate White-win terminal or a terminal draw. Then `b` is a minimax draw: Black can remain in the drawn cycle forever and prefers that to White's win. A legal cooperative path `b→z→draw` reaches a terminal draw in two plies, but it passes through a White-win state; the D-subgraph has **no** terminal draw path from `b`, so `DTD(b)=∞`.

This is why a short legal stalemate construction from the chess opening cannot by itself bound `DTD(s₀)` when `V(s₀)=D`. Its intermediate states would first need proved WDL D. It is also why D-DTD is a cooperative secondary criterion **inside** the primary draw class, not a replacement for minimax WDL.

## What remains unresolved for chess

Fraenkel–Lichtenstein's [EXPTIME-completeness result](https://kubokovac.eu/zlozitost/mat/chessExptime.pdf) uses arbitrary positions in a specified `n×n` chess family and explicitly does not establish their reachability from a natural start. Brunner et al. prove [PSPACE-completeness of generalized retrograde reachability and helpmate](https://arxiv.org/abs/2010.09271). Neither result transfers the gadget above to orthodox 8×8 chess or establishes a complexity class for its single fixed starting position. No reverse reduction from the proposed chess material oracle to `V(s₀)` or `DTM(s₀)` is known here. Strict computational separation from weakly solving the opening is an open question.
