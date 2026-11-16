# Methods, evidence, and next steps

## What existing mathematics supplies

| Result | Precise use here | Missing chess-specific step |
| --- | --- | --- |
| Finite reachability games are memorylessly determined. The attractor is the least fixed point adding a winner's state with **some** move inward and a defender's state with **all** moves inward ([Finkbeiner, Theorem 9.1](https://finkbeiner.groups.cispa.de/teaching/automata-games-verification-15/downloads/notes.pdf)). | Establish WDL regions and the quantifier distinction between a jointly optimal path to material and a player forcing that material. | A tractable invariant or cut that covers all equally optimal opening branches. |
| Quantitative reachability games have value recurrences and may require care in describing optimal strategies ([Brihaye et al., 2015](https://drops.dagstuhl.de/storage/00lipics/lipics-vol042-concur2015/LIPIcs.CONCUR.2015.297/LIPIcs.CONCUR.2015.297.pdf)). Multi-strategies formally retain sets of permitted actions ([Brihaye and Goeminne](https://arxiv.org/abs/2308.09625)). | Keep **every** WDL/DTM tie and every defender reply, rather than selecting a principal variation. | A compact representation of all optimal chess continuations from `s₀`. |
| Sound abstract interpretation overapproximates concrete reachability under a proved simulation or transfer condition ([Cousot and Cousot, 1977](https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml)). | Absence of a target from a sound abstract optimal-path graph proves concrete absence. | An abstraction sharp enough to prove absence without first solving the whole game. |
| Generalized chess from arbitrary `n×n` positions is EXPTIME-complete ([Fraenkel and Lichtenstein, 1981](https://kubokovac.eu/zlozitost/mat/chessExptime.pdf)). Generalized retrograde reachability and cooperative mate are PSPACE-complete ([Brunner et al., 2020](https://arxiv.org/abs/2010.09271)). | Warns against treating historical reachability or WDL as a cheap subroutine. | A reduction for this **fixed-opening, material-projection, no-draw-counter** problem. None is supplied by those papers. |
| A proof game gives an explicit legal history from the standard array ([Elkies and Stanley](https://math.mit.edu/~rstan/chess/spg.pdf)); proof-number search prioritizes nodes in AND/OR proof trees ([Allis et al., 1994](https://research.tilburguniversity.edu/en/publications/proof-number-search-2/)). | Certify historical membership and search small strategic subproblems. | Proof games do not certify optimal prefixes; search order is not a mathematical exclusion. |
| Syzygy provides 50-move-rule WDL and DTZ, not the present no-counter DTM or DTD ([python-chess Syzygy documentation](https://python-chess.readthedocs.io/en/v1.9.2/syzygy.html)). | Cross-check carefully matched local endgame facts. | Rule and metric conversion, plus independent predecessor verification. |

No located theorem about pawn or proof-game kernels was verified to preserve both history from `s₀` and all WDL/DTM-optimal prefixes. Pawn capture accounting remains useful as a **necessary** historical condition, not a substitute for a strategic proof.

## Three proof mechanisms worth pursuing

1. **Mandatory boundary.** Prove that every optimal path to a target crosses a small, exactly classified set of full states with a fixed incoming turn. An endgame exclusion is then a valid global exclusion. Merely showing a barrier from one possible source material is insufficient.
2. **Sound path abstraction.** Track material, side to move, WDL, DTM/DTD rank bounds, and irreversible resources. Prove every concrete optimal move is represented. If a target is absent from the abstract reachable set, it is absent from the concrete set. Abstract edges cannot be concatenated without checking that their middle positions agree.
3. **Incompatible phases.** Use resource monotonicity and rank descent to show that every proposed material route requires mutually incompatible events. This can forbid a long material word even when each single material edge exists somewhere.

For the first mechanism, a sound first-capture formulation is useful. Let `F_N` be the **full states** first entering the `N`-piece layer on optimal paths from `s₀`. Every path to fewer pieces crosses a capture from some state in `F_N` or a later state of the same layer. A universal exclusion from a sound overapproximation of all such states transfers downward. Existence of an optimal continuation from an arbitrary locally legal `N`-piece position does **not** imply that position has an optimal prefix from the opening.

For a decisive path, DTM supplies a strictly decreasing integer rank. If a proposed material word requires transition edges with source-distance sets `E₁,…,Eₖ`, it can occur only if there are `d₁>…>dₖ` with `dᵢ∈Eᵢ`; quiet moves consume additional rank. This is a necessary multi-step test, not a sufficient path certificate. For D-WDL, cycles and arbitrarily long play are possible, so the same rank argument is unavailable.

## Candidate materials and evidence status

| Case | Candidate or control | Historical/WDL evidence | Global obstacle |
| --- | --- | --- | --- |
| W | Initial material minus Black's f-pawn | `1.e4 e5 2.Qh5 Nc6 3.Bc4 Nf6 4.Qxf7#` is a legal White mate. This proves one member of `H_W`; it is only a control. | No exclusion from `R_W` is known. |
| W | `KP–KQ⁹` with a White win | The earlier research brief reports local certificates; they are **unverified here** and absent from the inspected previous release. | Eight Black promotions and at least 80 plies precede the target; no bound on `DTM(s₀)` connects that cost to optimal play. |
| D-WDL | A terminal no-capture stalemate with all 32 pieces | A recorded 12-move construction exists ([historical account with moves](https://www.chesshistory.com/winter/winter08.html)). Its material is already the opening material, so it is not a forbidden-material candidate. | A cooperative stalemate history need not stay in the minimax D region; it does not bound `DTD(s₀)`. |
| D-DTD | Nonterminal heavy-piece material after `KP–K` | The [promotion-fork theorem](result.md) excludes this **order** of materials. | The heavy-piece material may occur through another path or as terminal stalemate. |
| L | Color-reflected heavy-piece endgame families | Prior local tables study them; no historical optimal opening prefix is certified. `1.f3 e5 2.g4 Qh4#` is a simple control proving `H_L` contains the opening material. | Exchanging colors changes which side moves first at the standard start. |

An extreme-looking material is not a theorem target until its legal history and at least one compatible WDL state are certified. An arbitrary legal FEN is not enough. Conversely, a historical witness with the right WDL is still not an optimal opening witness.

## Immediate research task

Build a **first-entry frontier certificate** for a small target family. It must give (a) an independently checkable cover of every optimal prefix from `s₀` that can enter the target's material layer and (b) a local proof that every covered entry fails to reach the target under the same rules. Prove the cover before enlarging the endgame computation. If the cover depends on an unknown opening WDL or DTM, state that dependency explicitly rather than treating it as an established result.

Local exclusions can prune a DTM-optimal *trajectory* only after their source class is unavoidable. They cannot automatically remove moves from a proof of the opening's WDL: a defender's move that is suboptimal for DTM may still be relevant to the win/draw/loss argument.
