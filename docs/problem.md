# Research question and game model

## State and rules

Let `s₀` be the standard initial chess position. A state records piece placement, side to move, castling rights, and the en-passant option when available. A legal history starts at `s₀` and follows orthodox movement, capture, castling, en passant, and promotion rules. Checkmate, stalemate, and a *dead position* end the game. A position is dead only when checkmate is impossible for either side after **every** legal continuation, including cooperative continuations. An infinite game is a draw.

There is no resignation, agreed draw, clock, repetition draw, or 50/75-move draw in this model. In particular, a repeated state does not end play. Move counters and repetition history therefore are not components of a state. Returning to current FIDE draw rules is a separate project; results below do not transfer automatically.

`M(s)` records the counts of pawns, knights, bishops, rooks, and queens **separately for White and Black**. Both kings are always present and are implicit in a material label. We include terminal states when collecting materials.

## Value and optimal moves

`V(s) ∈ {W,D,L}` is the minimax outcome from White's perspective. Each player prefers a win to a draw to a loss. If one side can force mate, that side minimizes the guaranteed number of plies to mate, and the defender maximizes it without sacrificing a better WDL result. Write this distance as `d(s)` or DTM. At a decisive, nonterminal state, an optimal move `s→t` satisfies `V(t)=V(s)` and `d(t)=d(s)−1`. **All** moves satisfying the relevant criterion are retained, including all optimal replies by the defender.

In a drawn position we study two policies:

1. **D-WDL:** every move to another drawn state is optimal.
2. **D-DTD:** among moves to drawn states, both sides minimize the length of a *WDL-preserving* path to terminal stalemate or a dead position. This shortest path length is DTD. If no such finite path exists, DTD is infinity and all draw-preserving continuations within the infinite-distance region are allowed. A finite-distance optimal move lowers DTD by exactly one.

D-DTD is an explicit cooperative tie-breaker within the minimax draw class. It is not implied by DTM, and a cooperative path to a draw does not prove that either player can force a draw against arbitrary play. An optimal game is a legal play in which **each move** is optimal at its full current state; a final mate length alone does not certify this property.

## Reachability sets

For each possible initial result `v`, let:

- `H_v = {M(s) : s is historically reachable from s₀ and V(s)=v}`. The prefix used to reach `s` may contain suboptimal moves.
- `R_v = {M(s) : s occurs in at least one fully optimal game from s₀}`, conditional on `V(s₀)=v` and on the draw policy when `v=D`.

Terminal materials are included in both sets. Always `R_v ⊆ H_v`. The central question is whether `H_v \ R_v` is nonempty in each of four conditional cases: W, D-WDL, D-DTD, and L. The starting value `V(s₀)` is not assumed. The two draw policies have the same WDL classification and hence the same `H_D`, but `R_D-DTD ⊆ R_D-WDL`. A D-WDL exclusion therefore implies a D-DTD exclusion; the converse need not hold.

A candidate material needs separate evidence for (i) legal history, (ii) an outcome-compatible state, and (iii) exclusion from **all** optimal opening games. A local endgame witness supplies neither (i) nor (iii) by itself.

## Relationship to solving chess

A full classification of historically reachable states with WDL and DTM, plus their legal edges, suffices to compute every `H_v` and `R_v`; D-DTD additionally needs shortest paths in the drawn subgraph. Knowing only `V(s₀)` or `DTM(s₀)` does not identify all equally optimal continuations. No reduction from a material-reachability oracle back to the opening's WDL or DTM is established here, and no strict computational separation is claimed.

For fixed 8×8 chess, asymptotic complexity labels do not classify this one instance. Fraenkel and Lichtenstein prove EXPTIME-completeness for winning from **arbitrary positions** in a specified `n×n` generalized-chess family; they explicitly distinguish those positions from positions reachable from a natural opening. Brunner and coauthors prove PSPACE-completeness for generalized cooperative retrograde reachability and helpmate. Neither theorem directly settles the four material questions above. See [methods and sources](methods.md).
