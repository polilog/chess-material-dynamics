# Verified draw control: Loyd's 26-piece material

The [replayed game](stage-b-targets.md#verified-historical-and-outcome-compatible-controls) ends in stalemate after 19 plies. Its final material has all 16 White resources and ten Black resources: Black retains four pawns, one knight, one bishop, two rooks, a queen, and the king. This proves membership of that material in `H_D` under both draw tie-breakers. It does not prove an optimal path to it from a drawn opening.

## An exact resource frontier

**Lemma.** In every legal history from `s₀` to this material, Black makes no captures, White makes exactly six, and first entry into each total-piece layer from 31 down to 26 follows a White capture with Black to move.

**Proof.** White starts and ends with all 16 resources. A captured White resource cannot be restored, and all eight White pawns still appear as pawns, so Black cannot have captured any White piece. Black begins with 16 resources and ends with ten, and every loss is a White capture. Promotion preserves total-piece count. Hence the six piece-count decreases are White captures and leave Black to move. ∎

The final material can first appear later *within* the 26-piece layer if a Black pawn promotion changes its counts. Thus the turn statement applies to first **piece-count entry**, not automatically to first appearance of the precise material. In the specific Loyd game, the sixth White capture is `9.Qxc8`; Black then plays `9...Kg6`, and `10.Qe6` is stalemate at the same piece count.

## Why this is not yet a D-DTD exclusion

The 19-ply legal game is cooperative. The [small arena counterexample](stage-a-complexity.md#a-short-cooperative-draw-does-not-bound-dtd) proves that a short path from a drawn root to terminal draw need not stay inside the drawn WDL region. Neither the WDL values of all Loyd prefixes nor a separate D-preserving route from `s₀` have been certified. Therefore `DTD(s₀)≤19` cannot be inferred, even under `V(s₀)=D`. The current frontier is resource-exact but too broad strategically: all Black-to-move first entries with 26 pieces and full White material remain possible until a WDL/DTD invariant restricts them.

This candidate has the advantage of verified `H_D` and a fixed first-entry turn. Its missing lemma differs from the nine-queen pilots: the issue is a certified draw-preserving opening path or a WDL cut, rather than an absent historical target witness. It remains a separate D-DTD and D-WDL track; a DTD shortcut cannot be used for D-WDL.
