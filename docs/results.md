# Consolidated results and data guide

All rows use `v` to separate White and Black material (e.g. `KQNPvKR`); `WDL` is +1/0/-1 relative to White. A material word omits ordinary moves between material changes; FEN and UCI columns specify a concrete witness including those moves. Piece counts include kings. Blank witness columns on NO or UNKNOWN rows are intentional. `NO_WDL` denotes nonexistence of an outcome, not a dynamic barrier.

## Exact four-man layer

- 36 color-canonical tables; 66 color-sensitive materials; 146 admissible material/outcome classes (40 W, 66 D, 40 L). Exact computations use 200,026,881 valid canonical table entries; board reflections and color symmetry are used, and counts are not counts of distinct physical FENs.
- 2,332,500,906 legal move checks from nondead states; 1,992,044,906 WDL-preserving moves; 542,878,788 finite strict DTM/DTD-0 moves. This is a 72.75% reduction in those concrete moves, not in the number of material edges.
- 240 DTD-0-infinite canonical draws (184 KRvKP, 56 KPvKP); all have finite fresh DTD-3. 641,650 draws improve, maximum fresh DTD-3 is 16 plies. The 240 shortest repetition witnesses are retained.
- WDL: 356 edges, 1,280 YES / 24 NO material words, 14 minimal forbidden words, all 517 candidate endpoint pairs reachable.
- Strict: all 356 edges still possible; 940 YES / 364 NO words, 180 minimal obstructions, 488 YES / 29 NO endpoint pairs. DTD-0 and fresh DTD-3 have identical material-word statuses in this bounded universe (not asserted for higher layers). 62 pairs have a single feasible starting turn. 108 words fail the edge-distance budget condition.

Files in `results/four/`: `vertices.csv`, `edges.csv` (DTD-0 and DTD-3 witnesses in distinct columns), `paths.csv` (all three models in one final table), `pairs.csv` (status and witness-word reference), `turn_pairs.csv`, `forbidden_wdl_edges.csv`, `minimal_obstructions.csv`, `budget_obstructions.csv`, `summary.json`, distance statistics/histogram, move audit and repetition witnesses. The path universe is the set of nonempty material-changing words allowed by the WDL material graph. Pairs outside that transitive closure are excluded already by WDL. A pair with NO inside this universe is a real false positive of the projected graph.

The 29 strict-only endpoint exclusions are found directly by filtering `pairs.csv` on `wdl_status=YES, strict_status=NO`. They comprise 2 decisive and 27 draw cases. The full list is not duplicated in prose. Similarly, the 62 turn-sensitive pairs are those with exactly one turn flag set in `turn_pairs.csv`.

## Five-man layer and global reachability

`results/five/classification.csv`: 220 color-sensitive materials; 660 candidates; 582 YES, 78 NO. The 582 consist of 181 W, 220 D, 181 L. This existence classification is complete, independent of whether the strict material graph is complete.

`results/global/strict_witnesses.csv`: 1,020 certificate records. 292 records prove 146 targets through four men from five men, separately for DTD-0 and DTD-3; 728 records prove all targets through five men from six men in both models. Among the 728, exactly 582 concern five-man targets and use a single capture; the other 146 have full compatible paths to smaller material. A draw tail is included where needed to establish the exact DTD of a five-man target; some tails lead to a smaller exact table rather than a terminal draw. The `proof` column identifies the proof type, not a separate external dependency. Reproduction reconstructs finite minimax/liveness checks using the exact <=4 tables. All global positive records are directly rechecked by the final verifier.

`results/five/edges.csv`: 3,412 candidates with exactly one material-changing move, comprising capture, capture-promotion, and quiet promotion. Current counts: 1,784 YES, 192 NO, 1,436 UNKNOWN. The negative reasons include target-turn incompatibility, lack of the required promoted piece on the final rank, an alternative promotion with a superior WDL, and exhaustive five-man exclusions. `target_capture` is an optional additional proof move after a promotion, not part of the material edge.

`results/five/pairs_to_lower.csv`: 29,000 candidate pairs; 1,981 YES, 24,034 NO, 2,985 UNKNOWN. `results/five/pairs_same_layer.csv`: 113,340 distinct same-layer candidate pairs; 316 YES, 110,884 NO, 2,140 UNKNOWN. The latter omits identity pairs. The large negative counts largely come from elementary material/WDL restrictions, not strict time optimality alone. UNKNOWN entries must not be treated as absent edges when proving exclusions. Positive pair witnesses are concrete paths, not arbitrary abstract concatenations.

### Eight exact five-man tables

| Canonical material | max DTM, White/Black to move | max DTD-0, White/Black to move |
| --- | --- | --- |
| KQQQvK | 5 / 8 | — / 0 |
| KQQRvK | 7 / 12 | — / 0 |
| KQRRvK | 7 / 14 | — / 0 |
| KRRRvK | 9 / 14 | — / 0 |
| KBBBvK | 31 / 38 | 1 / 2 |
| KBBNvK | 65 / 66 | 2 / 3 |
| KBNNvK | 67 / 68 | 4 / 8 |
| KNNNvK | 41 / 42 | 8 / 9 |

Dashes mean no drawn positions with that starting turn. DTD-3 equals DTD-0 for these eight materials. Combined: 419,821,014 valid canonical entries; 5,873,081,857 legal move checks in exhaustive audits; zero recorded Bellman-equation violations. Heavy-triple draws are stalemates. Minor-triple DTD uses cooperative mate reachability to distinguish dead positions. Exact statistics, distance histograms, positive witnesses and per-turn target reachability counts are in `results/five/exact/`. The `_stats.tsv` files end with a four-field audit record (`audit_errors`, value, `legal_moves`, count); heavy histograms use 254 for draws, while minor histograms record wins and DTD-0 draws separately. These are final per-material solver outputs, not search logs. The `turn_pairs.csv` table combines the exact endpoint counts. The material-specific C++ solvers regenerate all eight.

The remaining 102 of 110 color-canonical five-man materials do not yet have complete strict position tables. No complete strict five-man DTM/DTD classification or global strict seven-man saturation is claimed.

## Reusable larger-layer exclusions

`results/propagation/certified_pairs.csv` contains 1,002 distinct saved pair exclusions from formal five- through eight-man starts to small targets. Counts: 58 at 5, 142 at 6, 286 at 7, 516 at 8. These are the union of the earlier material-boundary and turn-sensitive propagation sets. All are revalidated by conservative closure over the final non-NO graph and exact smaller-layer boundary data in `scripts/check_structure.py`. They are not an exhaustive classification of all larger-layer pairs, and not all have a WDL-positive contrast witness. The general theorems in `model-and-theorems.md` cover arbitrary formal sizes without enumerating them. Large formal materials need not have a legal history from the opening.

## Secondary WDL results

These results are retained as a comparison and foundation, not as claims of strict time optimality.

- All 146 <=4 targets have WDL-preserving witnesses from eight men. All 582 five-man targets have WDL witnesses from six men; the best recorded witnesses reach 560 from seven and 450 from eight. `five_targets_best_witness.csv` contains the best retained path for each target; `reachability_from7.csv` gives the final seven-man matrix. The strictly stronger six-man certificates in `global/strict_witnesses.csv` independently cover all 582 from six men.
- `six_classification.csv`: 715 materials, 2,145 outcome candidates, 1,995 possible and 150 impossible (640 W,715 D,640 L). Existence classification follows published ChessDB statistics and elementary no-mate restrictions. 1,869 have recorded concrete six-man positions in the registry; not every positive class has an independently computed full table. `reachability_from7.csv`: 2,723 admissible targets through six; 2,555 YES, 168 UNKNOWN. All decisive targets are YES; 22 five-man and 146 six-man draw targets remain UNKNOWN. There is no dynamic global NO in that matrix. Higher WDL heights are lower bounds only.
- `absolute_position_barriers.csv`: 4,332 concrete two-/three-man positions with no WDL-preserving immediate predecessor. Of these 1,816 have no geometric predecessor, 248 have only predecessors where the game has ended, and 2,268 have a game-legal predecessor but none of the same WDL. The latter include 128 KQ draws, 2,120 KB draws and 20 live KP draws (both colors included). These are absolute by the last-move theorem. The total audited physical states were 3,898,392. `position_reachability.csv` gives exact <=4-to-<=3 counts; `live_barrier_predecessors.csv` contains all 42 predecessors of a concrete live KP draw (all W). No exhaustive analogous four-man-target/ five-man-predecessor calculation has been completed.
- `proofs/wdl_proofs.json` is a single retained final dependency graph (base minimax trees, reverse-lift trees, five-/seven-man proof nodes). It is not a directory of search iterations. Two externally anchored decisive positions are explicitly listed in `proofs/external_wdl_anchors.csv`. The verifier checks the proof graph and the final WDL witness paths, conditional on these two published WDL values.
