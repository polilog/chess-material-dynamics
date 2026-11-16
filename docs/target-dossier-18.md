# First target dossier: `KP–KQ⁹R²B²N²`

**Target:** White has king and one pawn; Black has king, nine queens, two rooks, two bishops, and two knights. There are 18 pieces in total. The original brief reports a historically reachable White-winning position and a strict local 19-to-18-piece continuation with DTM 3 at its source. No FEN, move history, or value proof for that report was found in the current repository, its available Git history, or the other accessible local chess files. The target is therefore **not yet certified as a member of `H_W`**. The lemmas below are necessary conditions on *any* legal history to it and do not depend on that report.

## Resource ledger

**Lemma 1 (full survival and exclusive captures).** In every legal history from the standard start to this target:

1. Black's original queen survives, every one of Black's eight original pawns promotes exactly once and specifically to a queen, and all original Black rooks, bishops, and knights survive. No Black resource is captured at any earlier time.
2. White never captures a Black piece. Black captures exactly 14 White pieces. The surviving White pawn is one of White's original pawns; White's other 14 original resources, apart from the king, are eventually removed by Black captures. Some of those resources could have promoted before being captured.
3. The first entry into **each** total-piece layer `n=31,30,…,18` occurs immediately after a Black capture, with White to move. At first entry into the 19-piece layer, Black has 16 pieces and White has king, the eventual surviving pawn, and one other piece. At first entry into the 18-piece layer, Black has 16 and White has king plus that pawn.

**Proof.** Nine Black queens require the original queen and all eight pawn resources; a pawn can promote only once. Thus none of these nine resources was captured, and each pawn's final promotion type was queen. All two original rooks, bishops, and knights are also present in the target: no pawn resource remains available to replace one by underpromotion. Black's original 16 resources therefore survive throughout the history. A White capture would permanently remove one, so White never captures. White starts with 16 pieces and ends with two; each of the 14 losses must be a Black capture. A promotion changes piece type but not total count. Therefore every drop from 32 down to 18 pieces is a Black capture, and the turn after each first entry is White's. The 19- and 18-piece distributions follow by subtracting from Black's constant 16. ∎

**Lemma 2 (promotion and final-event constraints).** At least 40 Black pawn moves and 80 elapsed plies precede the target. Its **first occurrence** is after a Black move and has White to move. The move creating it is exactly one of the following event types:

- Black captures White's penultimate nonking resource after all eight Black promotions are complete;
- Black makes the eighth queen promotion after White has already been reduced to king and one pawn;
- Black captures that White resource while making the eighth queen promotion.

If the target state's theoretical value is W, that first occurrence is nonterminal.

**Proof.** Each of eight Black pawns needs at least five moves to promote, giving 40 Black moves and earliest ply 80. The target's two required facts, “White has only king and pawn” and “Black has nine queens,” become true only through Black captures and Black promotions. A White move cannot first make either fact true under Lemma 1. The final missing fact can therefore be supplied by a Black capture, a Black promotion, or one move doing both. White moves next. A White-win terminal checkmate would have Black to move; a terminal draw has value D; and a Black-win terminal has value L. Hence a White-valued first target state is nonterminal. ∎

## What the ledger does and does not cover

The ledger is an outcome-independent **event cover** of all legal target histories. It proves the incoming turn and three last-event types without enumerating boards. It does not bound `DTM` at 19 or 18 pieces, and it does not prove that any target-directed first-entry state is reached by an optimal opening prefix. Black may promote some pawns before or after the 19-piece entry; same-layer quiet moves and promotions must remain in any relation used for a global proof.

**Conditional check on the reported DTM-3 witness.** Suppose a White-winning first-entry 19-piece state has DTM 3 and a fully strict continuation to the 18-piece target before mate. White moves first, Black moves second, and White mates third. By Lemma 2, the target can first appear only after Black's second-ply move. That move must capture White's last extra resource and either find all nine Black queens already present or simultaneously make the eighth queen promotion by capture. There is no time for a separate later promotion. This does not validate the reported witness, but it is a precise check its FEN/UCI record must pass.

The reported local 19-to-18 witness, if recovered, would be a useful counterexample to any claim that the event ledger **alone** forbids a strict local route. The actual missing lemma is narrower: every **opening-optimal** first entry compatible with this ledger must fail to continue optimally to the target. That lemma has not been proved. The [queen-only barrier](result.md#transferred-queen-only-dtm-barrier) is a calibration of exact model transfer, but it does not apply to this 18-piece target: Black still has rooks, bishops, and knights, and White retains a pawn.

## A verified resource-control game

`1.e4 f6 2.e5 fxe5 3.d4 g5 4.Qh5#` is a legal seven-ply White mate with Black's full 16-piece complement intact and no White capture. Black captured White's e-pawn. The record `white_mate_black_full_31` in [historical_witnesses.json](../data/historical_witnesses.json) is replayed by the [witness checker](../scripts/verify_historical_witnesses.py). It does **not** reach the 18-piece target. It shows that Black's complete material survival and White's lack of captures are compatible with a White-winning historical position; a simple “more Black material means White cannot win” argument is false.

## Decision gate

The first gate is still open: obtain the claimed 18-piece PGN/FEN and exact WDL/DTM certificate, or construct a new historical White-winning witness. If that fails, do not use this target in an `H_W\R_W` theorem. If it succeeds, classify the three last-event cases at the 19-/18-piece frontier. A successful exclusion must cover *all* first-entry positions with a fully optimal prefix, not just the supplied witness. If this requires a distinct local lemma for each board, switch target or abstraction as required by the [research strategy](research-strategy.md).
