# Mathematical model and results

> **Scope:** This retained local endgame study uses locally legal positions, omits castling, and includes a fresh-third-repetition variant. Its transition barriers are valid under their stated local model. The [opening research model](problem.md) permits unlimited repetition and requires historical reachability from the standard start; transferring a local barrier requires matching rules and a proof that the relevant source is reached.

## 1. States and objectives

A state records placement, side to move and the relevant en-passant state used by the implementation. We study locally legal states (the previous mover is not left in check), not necessarily positions with a legal history from the opening. The ordinary chess move rules apply except castling, the 50/75-move rules and claims are omitted. Mate, stalemate and dead positions terminate. In the WDL model infinite play is a draw. No draw by agreement is allowed. The repetition convention uses exact placement, turn and the engine's en-passant encoding; DTD-3 is not a complete historical FIDE-state model.

Let `M(s)` be the color-sensitive material multiset and `n(s)` the number of men, including kings. `V(s)` is the minimax value from White's perspective: W = +1, D = 0, L = -1. A WDL-preserving edge `s -> t` requires legal play from a nonterminal state and `V(s)=V(t)`.

For decisive positions define DTM `d(s)` as the number of plies under minimax mate distance: 0 at checkmate, `1+min d(t)` on the winning side's turn (winning children only), `1+max d(t)` on the losing side's turn. All moves from the losing side preserve the result. Strict edges satisfy `d(t)=d(s)-1`.

For draws DTD-0 is the length of a shortest WDL-D path to stalemate or a dead position. Both players minimize; this is a secondary common preference, not a new zero-sum minimax game. DTD-0 is infinity when no such finite path exists; these states have no finite DTD-0 optimal continuation. DTD-3 additionally treats the third occurrence of the same position as automatic termination. DTD-3 here is measured from fresh history, not arbitrary prior repetitions. We do not identify a WDL draw with a terminal draw.

If `g(r)` is the shortest nonempty WDL-D cycle at an exact position r, then for fresh history

```
d3(s) = min(d0(s), min_r (dist_D(s,r) + 2*g(r))).
```

Every third-repetition path must reach some r and return to it twice, giving the lower bound. Conversely, a shortest path to r followed by two shortest cycles yields a draw by that length (possibly earlier at another repeated state), giving the upper bound. The shortest ordinary position cycle is at least four plies. Any capture or promotion reduces a monotone material parameter, so it must precede the first occurrence of the finally repeated position. For material paths, a fresh-distance gradient through the last material change is consequently necessary and sufficient for extension to a fresh shortest terminal draw: a shorter repetition in the prefix would contradict optimality, and a shorter fresh continuation would also contradict optimality. This does not assert that the fresh-distance gradient describes every history-dependent optimal quiet move after the last material change.

## 2. Material abstraction and complete finite checks

For a result v, an edge between material classes exists if at least one concrete strictly optimal move changes one class into the other. A material word is realizable only if one concrete position path realizes **all** its consecutive changes, allowing strictly optimal quiet moves between changes. Pair reachability asks whether any such word connects the two materials.

A plain material graph can overapproximate pair reachability: two edges may use incompatible middle positions. Exact composition is relational. Let `R(A,B)` be the concrete crossing relation, and `Q_B*` the closure of optimal moves staying inside B. Then the two-edge word A,B,C is realizable iff

```
R(B,C) ∘ Q_B* ∘ R(A,B) != empty.
```

A graph of concrete positions or exact strongly connected components preserves WDL reachability. Strict finite distance already makes the concrete graph acyclic. A useful conservative abstraction is `(material, WDL, side_to_move, distance)`; it still need not be exact. The implemented exact small-layer word algorithm propagates bitsets of feasible suffix words along actual legal moves in order of distance; no positive material path is inferred merely by concatenating abstract edges.

### Theorem A — First-capture boundary and global monotonicity

Let `R_N,v` be all targets reachable by a strict path from any locally legal N-man state of value v (fresh history in DTD-3). Every path to fewer than N men crosses the N -> N-1 capture boundary. If B is excluded from every possible first-entry state (or a sound upper approximation to their material/turn classes), B is excluded from the original layer. A capture resets the relevant repetition history for the smaller material because no previous state had that smaller number of men. It also fixes the receiving side to move: the side whose piece was captured.

If B of size at most N is impossible from **every** N-man state, then it is impossible from every larger layer. Conversely, a positive path from N to B proves all intermediate starting-size lower bounds by truncation at the first capture to the respective layer. An existence certificate for one material class cannot be concatenated with an unrelated certificate for that class.

### Theorem B — Distance budget

For a strict material edge e let E(e) be the set of feasible source distances. A word with consecutive material edges e1,...,ek requires distances d1>...>dk with di in E(ei). If no such choice exists, the word is impossible. This criterion uses strictly decreasing ply counts; intervening quiet moves can only consume additional budget. The more general bound `max_d(A) < minimum_plies(A,B)+min_d(B)` also proves impossibility for decisive material pairs, provided the extrema and side-to-move assumptions are valid. Four-man data contain 108 budget-obstructed words (104 formerly WDL-realizable). It is a necessary, not sufficient, condition for realizability.

### Theorem C — No incoming optimum

For a concrete n-man target s, every immediate predecessor has n or n+1 men. If no game-legal predecessor of the same WDL exists, no nonempty WDL-preserving path can end at s from any size. The exact <=4 predecessor audit establishes 2,268 such genuine WDL barriers among <=3 physical states, including 20 live pawn draws. This is a position-level theorem, not a material-level one.

## 3. General material barriers from exact boundaries

All claims below are about preserving the stated outcome; they do not exclude a material from all chess games. Reflections exchange colors and reverse decisive WDL.

| Source family | Target | Model / condition | Exact boundary |
| --- | --- | --- | --- |
| `KQ^a v K`, a >= 4 | `KQvK` | DTM, queen-side win | `KQQQvK`, winner to move: zero paths |
| `KQ^a R v K`, a >= 3 | `KRvK` | DTM, stronger-side win | `KQQRvK`, winner to move: zero paths |
| `KB^a NN v K`, a >= 1 | `KNNvK` | DTM, stronger-side win | `KBNNvK`, either turn: zero paths |
| `KB^a v K`, a >= 3 | `KBvK` | DTD, draw | `KBBBvK`, either turn: zero paths |
| `KB^a v K`, a >= 4 | `KBBvK` | DTD, draw | `KBBBvK`, stronger side to move: zero paths |
| `KPvKQ^a`, a >= 2 | `KPvK` | Pawn-side W under WDL, or D under DTD | `KPvKQ`, queen side to move: zero paths in respective model |
| `KX1...Xk v K`, k >= 3, Xi in Q,R,B,N,P | `KQvK` or `KRvK` | DTD-0 and fresh DTD-3, draw | All 15 four-man one-sided materials, stronger side to move: zero paths |

**Proof scheme.** The desired material is reached by removing pieces one at a time, and by preserving every piece type that must remain (in the pawnless families no new pieces of other types can arise). The smaller stated boundary is compulsory. The lone king captures the winning side's surplus pieces, fixing the stronger side to move upon entry. In the pawn-versus-queens family White must remove a queen, fixing Black to move at the one-queen boundary. In the general shortest-draw theorem the first entry into the four-man layer is after a lone-king capture, hence stronger side to move; the full table of 15 materials and both targets is exhausted. The relevant zero counts are in `results/five/exact/turn_pairs.csv` or `results/four/turn_pairs.csv` (a missing pair outside the WDL-reachable candidate set is already excluded by WDL). The DTD-0 four-man boundary is independently computed by `src/five/dtd0_boundary.cpp`. The WDL part of the pawn/queen theorem is verified by `src/five/wdl_turn.cpp`. The smaller layer's no-path result and Theorem A yield the exclusions above. No high-layer tablebase is required.

For the bishop-only family, the `KBBBvK` strong-turn DTD is at most 1, and no material-changing continuation can be played by the stronger side against a lone king. Exact counts show no KB target from either turn. The result applies to formal local compositions; the availability of many promoted pieces in an actual opening history is a separate question.

### An elementary shortest-draw obstruction

`KPvK -> KQvK -> KvK` and `KPvK -> KRvK -> KvK` cannot occur in a shortest draw. If promotion to Q or R is legal in a drawn KPvK state, promotion on the same square to B or N is legal and immediately produces a dead draw. Therefore the source DTD is 1; a heavy-piece promotion requiring a further capture cannot be a shortest draw. Color reflection gives two more exclusions.

### Five-man WDL nonexistence

A bare king cannot mate. A lone bishop cannot mate a king whose only additional pieces are queens/rooks: in the two orthogonal directions from the checked king toward the bishop's checking diagonal, the bishop attacks neither adjacent square and the mating king cannot cover both. An uncovered adjacent square is either an escape or occupied by a heavy piece which can block the diagonal at its first square or take the bishop. Thus the purported mate is not mate. With a lone knight vs queens only, two orthogonal escape squares toward the knight cannot both be controlled by the mating king; a queen occupying the uncovered one can take the knight (or another queen obstructing the line can). No pawn exists to create a new type; captures preserve these exclusions. Applied to the five-man universe this gives 70 bare-king and 8 nontrivial impossible outcomes. The 582 remaining classes have constructive strict certificates.

## 4. Saturation versus barriers

Define `h_v(M)` as the greatest initial material size admitting a strict path to some state of material M, capped by the chosen universe. The positive certificate tables prove `h_v(M)>=6` for **every** admissible target through five men. This excludes finite global barriers at or below that bound; no global material-origin NO has yet been proved for an admissible target. It does not contradict the source-specific exclusions above. An important future refinement is a live-target height, where the target must be nonterminal. This remains a research direction, not a completed classification.

The original opening position has a fixed geometry, fixed material and a specific history. A local exclusion can constrain a real strictly optimal path only when that path must enter the relevant state class under the same rules. Positive local certificates do not prove reachability from the opening. Neither DTM nor DTD tie-breaking alone solves WDL in an unknown position or justifies dropping arbitrary opponent moves from a minimax proof.
