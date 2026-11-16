# Fallback target dossier: `KP–KQ⁹`

**Target:** White has king and one pawn; Black has king and nine queens, for 12 pieces. The original brief reports a historically reachable White-winning state, a local strict continuation from a first 20-piece entry, and a separate 25-piece WDL-versus-DTM contrast. The corresponding full move histories, FENs, and exact value certificates were not found in the accessible repository or local files. Thus the target's membership in `H_W` is not currently certified here.

## Exact history constraints

**Lemma.** Every legal history from the standard start to `KP–KQ⁹` has all of the following properties:

1. Black's original queen and all eight Black pawn resources survive; every Black pawn promotes to a queen. No Black queen or pawn is ever captured.
2. White captures exactly the six original Black rooks, bishops, and knights, and no other Black piece. Black captures exactly 14 White resources. The one surviving White pawn is original; any other White pawn may have promoted before Black captured its resource.
3. Exactly 20 captures occur in total, because promotions do not change the piece count. At least 40 Black pawn moves and 80 elapsed plies precede the target.

**Proof.** Nine queens require the original Black queen plus all eight pawns, each promoted to a queen. No pawn remains available to replace an original rook, bishop, or knight, and the target has none, so all six of those original pieces were captured by White. White starts with 16 pieces and ends with king and pawn, hence 14 White resources were captured by Black. The 20 lost resources give 20 captures. Each of eight Black pawns needs at least five moves to promote, giving 40 Black moves and earliest ply 80. ∎

Unlike the [18-piece target](target-dossier-18.md), this target does **not** force one side to make every capture. A first entry into an intermediate total-piece layer can follow either a White capture or a Black capture, so material count alone does not fix the receiving turn. The first occurrence of the final material can be caused by White capturing the last Black rook/bishop/knight, by Black capturing White's last extra resource, by Black's eighth queen promotion, or by a Black capture-promotion. Consequently the 12-piece target has a weaker turn-and-provenance frontier than the 18-piece target, despite the same eight-promotion requirement.

## Assessment

The nine-queen lower bound is a legal-history cost, not an opening DTM bound. The brief's reported 25-piece position, if certified, would actually refute a broad WDL-only exclusion of routes to this target: it reportedly has a WDL-preserving target continuation but a faster mate. That contrast would motivate a **strict DTM** cut, not prove a global one. Recovering the 20-piece and 25-piece records is the first evidence gate. Without them, expanding a high-piece search would repeat the failed pattern of chasing local examples without a compulsory opening frontier. The 18-piece target remains the better pilot for a resource cut because it fixes Black's full survival and every first-entry turn.
