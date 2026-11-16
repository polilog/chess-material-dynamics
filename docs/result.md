# Proved trajectory restriction

## Promotion-fork theorem

**Theorem.** Assume `V(s₀)=D` and use D-DTD. In no fully optimal game from `s₀` can a position with material `KP–K` be followed by a **nonterminal** position with material `KQ–K` or `KR–K` for the same side. The assertion is symmetric under exchanging the colors. Consequently the material words `KP–K → KQ–K → K–K` and `KP–K → KR–K → K–K` are impossible on such a game.

**Proof.** Suppose one of the heavy-piece materials first appears after `KP–K`. With only one pawn and the two kings on the board, the new queen or rook can only be produced by promoting that pawn. Immediately before promotion the promoting side is not in check: the opposing side has only a king, and legal kings cannot attack one another. Promoting on the same square to a bishop or knight is therefore legal. The resulting `KB–K` or `KN–K` is dead: neither side can ever checkmate with that material. This move produces a terminal draw in one ply.

The position immediately before the contemplated heavy-piece promotion lies on a fully optimal drawn game, so its WDL is D. Since a legal draw-preserving move reaches a terminal draw in one ply, its DTD is exactly one. A D-DTD-optimal move must also reach a terminal draw in one ply. A queen or rook promotion leading to a *nonterminal* position cannot be optimal. If the heavy-piece promotion itself causes stalemate, it is terminal and is outside the theorem's claim. The two stated three-material words require a further move after the heavy-piece material and are therefore excluded. ∎

**Boundary of the result.** The theorem excludes an ordered segment of a game. It does not show that `KQ–K` or `KR–K` is absent from `R_D-DTD`: either material might arise along a different path or as a terminal stalemate. It does not apply to D-WDL, where a move preserving the draw need not minimize time to a terminal draw. The shorter three-material version appeared in the [previous local release](https://github.com/polilog/chess-material-dynamics/blob/457fc79d507ef5c3c78b5450f964f1df438976ca/docs/model-and-theorems.md); no priority claim is made here.

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
