# Proved trajectory restriction

## Promotion-fork theorem

**Theorem.** Assume `V(s₀)=D` and use D-DTD. In no fully optimal game from `s₀` can a position with material `KP–K` be followed by a **nonterminal** position with material `KQ–K` or `KR–K` for the same side. The assertion is symmetric under exchanging the colors. Consequently the material words `KP–K → KQ–K → K–K` and `KP–K → KR–K → K–K` are impossible on such a game.

**Proof.** Suppose one of the heavy-piece materials first appears after `KP–K`. With only one pawn and the two kings on the board, the new queen or rook can only be produced by promoting that pawn. Immediately before promotion the promoting side is not in check: the opposing side has only a king, and legal kings cannot attack one another. Promoting on the same square to a bishop or knight is therefore legal. The resulting `KB–K` or `KN–K` is dead: neither side can ever checkmate with that material. This move produces a terminal draw in one ply.

The position immediately before the contemplated heavy-piece promotion lies on a fully optimal drawn game, so its WDL is D. Since a legal draw-preserving move reaches a terminal draw in one ply, its DTD is exactly one. A D-DTD-optimal move must also reach a terminal draw in one ply. A queen or rook promotion leading to a *nonterminal* position cannot be optimal. If the heavy-piece promotion itself causes stalemate, it is terminal and is outside the theorem's claim. The two stated three-material words require a further move after the heavy-piece material and are therefore excluded. ∎

**Boundary of the result.** The theorem excludes an ordered segment of a game. It does not show that `KQ–K` or `KR–K` is absent from `R_D-DTD`: either material might arise along a different path or as a terminal stalemate. It does not apply to D-WDL, where a move preserving the draw need not minimize time to a terminal draw. The shorter three-material version appeared in the [previous local release](https://github.com/polilog/chess-material-dynamics/blob/457fc79d507ef5c3c78b5450f964f1df438976ca/docs/model-and-theorems.md); no priority claim is made here.

## Transferred queen-only DTM barrier

**Theorem (retained computed boundary in the opening rule model).** Conditional on `V(s₀)=W`, no fully DTM-optimal game from `s₀` can visit `KQ^a–K` with `a≥4` and later visit `KQ–K`. Conditional on `V(s₀)=L`, the color-reflected statement holds for `K–KQ^a` followed by `K–KQ`. This forbids an **ordered pair of materials**, not `KQ–K` or `K–KQ` as a material in all optimal games.

**Proof.** The [retained exact table](model-and-theorems.md#3-general-material-barriers-from-exact-boundaries) gives zero strict paths from a White-to-move, White-winning `KQQQ–K` position to `KQ–K`. We regenerated the relevant `K–K`, `KQ–K`, `KQQ–K`, and `KQQQ–K` tables with the source-derived [focused verifier](../scripts/reproduce_queen_boundary.py). Its Bellman audit reported zero errors over 320,474,646 legal moves; the regenerated statistics and distance histogram match the released files exactly. The table reports zero such paths when White moves and 8,611 when Black moves, so the incoming turn is essential.

Starting from `KQ^a–K` with `a≥4`, any play that later has just one White queen must first pass through `KQQQ–K`. There are no pawns to promote, and the bare Black king must capture the queen that reduces the count from four to three. It is therefore White's turn at the first three-queen entry. An optimal prefix preserves W and has a strict DTM-optimal suffix, contradicting the zero-path table. The queen-only states and all their descendants have no rooks or pawns, so castling and en passant are unavailable. Both the retained decisive endgame solver and the opening model treat infinite play as a draw and use no repetition or move-count termination for DTM. Their WDL/DTM game graphs on these states therefore coincide. Color reflection gives the L statement for a path that actually starts at the ordinary White-to-move opening. ∎

**Evidence limit.** The focused verifier reuses the released move generator and retrograde algorithm; it is a reproducible regeneration, not an independent solver. A separately replayed Black-to-move positive path in the retained [witness file](../results/five/exact/heavy_triples_witnesses.csv) confirms that dropping the turn condition would be false. The theorem still needs a new opening-specific cut before it can exclude `KQ–K` globally; a path from `s₀` could reach that material without ever visiting four queens.

## Transferred pawn-versus-queens WDL barrier

**Theorem (retained computed WDL boundary in the opening rule model).** Conditional on `V(s₀)=W`, no fully optimal game from `s₀` can visit White `KP–KQ^a` with `a≥2` and later visit `KP–K`. Conditional on `V(s₀)=L`, the color-reflected statement holds for Black's pawn side. The exclusion uses only WDL preservation, so it holds under either decisive tie-breaker. It is again an ordered-pair restriction, not a global prohibition of `KP–K`.

**Proof.** If the pawn side starts against at least two opposing queens and later faces a bare king, it must first pass from two queens to one. The pawn side captures the queen that makes this transition, so the remaining queen side moves next. The [focused WDL regeneration](../scripts/reproduce_pawn_queen_boundary.py) solves the necessary `KQ–KP` subsystem, including all possible pawn promotions, and propagates WDL-preserving predecessors of queen captures. For a **pawn-side win** it finds 361,708 canonical `KQ–KP` sources from which the queen can eventually be captured while preserving WDL, but zero with the queen side to move. A fully optimal game preserves its decisive WDL at every ply, so the required first one-queen entry cannot continue to `KP–K` while preserving the pawn-side win. There are no rooks and only one pawn in these states or descendants; castling and en passant cannot occur. The regenerated no-repetition WDL graph therefore matches the opening rule model. The argument is color symmetric at the local boundary and applies to an actual opening path only under its stated initial outcome. ∎

**Why the draw analogue fails under D-WDL.** The same regeneration finds one canonical queen-to-move **drawn** `KQ–KP` state with a WDL-preserving path to `KP–K`:

```text
k7/2p5/1Q1K4/8/8/8/8/8 w - - 0 1
1.Kc6 cxb6 2.Kxb6
```

White begins in check from the pawn on c7. White can play `Qxc7` or `Kxc7`, each immediately stalemating Black, so White can secure a draw. On any other legal White move, the queen remains on b6 and Black can play `cxb6`; after that White has a bare king and cannot force mate. The source is therefore D. The displayed line stays in D and ends with bare kings, so it is D-WDL optimal. It is **not** D-DTD optimal: `Qxc7` or `Kxc7` gives a terminal draw in one ply instead of three. The moves and terminal states are checked independently with `python-chess` by the focused verifier. This concrete exception explains why the WDL winning-side barrier cannot simply be copied to D-WDL and why the old DTD condition is substantive.

## Draw-policy inclusion

**Proposition.** `R_D-DTD ⊆ R_D-WDL`, while `H_D` is identical under the two draw policies.

**Proof.** Both policies use the same primary WDL evaluation. Every D-DTD-optimal move is drawn-state preserving, hence is D-WDL optimal. The WDL value of every historically reachable state is independent of the secondary draw policy, so its contribution to `H_D` is unchanged. ∎

## Historical promotion bound

**Proposition.** If one side has nine queens in a historically reachable position, it has retained its original queen and promoted all eight original pawns. That side has made at least 40 pawn moves. The first such position cannot occur before ply 79 for White or ply 80 for Black.

**Proof.** Each pawn can produce at most one queen; eight pawns plus the original queen are the only nine possible resources. A pawn needs to advance six ranks to promote. Its initial double step can cover two ranks, while every other move, including a capture, advances at most one. Thus each pawn needs at least five moves, and eight pawns need at least 40 moves by that side. White's 40th move is ply 79; Black's is ply 80. ∎

This is a lower bound on **historical elapsed play**, not on DTM or DTD, and it does not establish the WDL of any nine-queen position. The extreme local witnesses described in the research brief were not present in the inspected previous release and are not treated as verified certificates here.

## Status of the central conjecture

| Initial outcome and policy | Proved from `s₀` | Is `H_v \ R_v ≠ ∅` proved? |
| --- | --- | --- |
| White win, DTM | DTM decreases by one on every optimal ply; local barriers transfer only after their source is reached. | No |
| Draw, D-WDL | Draw-preserving optimal paths can be infinite. | No |
| Draw, D-DTD | Promotion-fork theorem; finite DTD decreases by one on every optimal ply. | No |
| Black win, DTM | Color-reflected local statements require an actual optimal opening prefix; color exchange does not preserve White's first move. | No |

`UNKNOWN` means no proof has been established; it is not a negative finding. An endgame restriction can be lifted to a game from `s₀` only when the game is known to enter the relevant source class, with matching rules and turn information. It cannot by itself exclude the destination material from every optimal opening game.
