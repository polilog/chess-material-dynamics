# Reproduction and validation

## Environment and commands

Python 3.10+, NumPy, GCC with C++17/pthreads, Linux or WSL (the word solver uses POSIX mmap). Suggested several GB RAM and >=12 GB free disk. Install requirements, then run from the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/reproduce.py structure
python scripts/reproduce.py certificates
```

The `structure` stage checks the complete five-man candidate universe, all final negative pair closures, all 1,002 saved propagated exclusions and legal replay of every published strict YES path. It requires no binary tables. `certificates` generates the 36 WDL tables if absent, then DTM/DTD-0 and fresh DTD-3 distances, checks all four-man positive path certificates and rechecks all 1,020 strict global records. The latter include exact target distances, bounded minimax and liveness, all required opponent moves, and draw alternatives; they are not just UCI replays.

The remaining stages are:

- `four`: full direct move audit, strict word/endpoint bitset enumeration, repetition calculation/audit, budget and turn checks. The script compares all released strict statuses to the regenerated classifications. `wdl-four` also performs the full exact WDL word enumeration from the independently generated material graph and checks the 1,304 WDL statuses.
- `five`: regenerates the eight completed five-man tables, checks numeric statistics and minor-material endpoint counts, rechecks the 192 direct NO filters and all 1,784 positive edges, 1,981 positive lower pairs, and 316 same-layer positive pairs. It does not solve the other 102 color-canonical materials.
- `wdl`: rechecks the saved WDL proof graph and witnesses, regenerates predecessor flags through four men, expands to physical boards and compares all 4,332 absolute positional barriers.
- `full`: all of the above. `--rebuild` regenerates the <=4 tablebase binaries even if they are already present. `--work /path/to/workdir` selects a different generated workspace; default `work/` is ignored by git. `CXX` selects the compiler. All results in `results/` remain unchanged.

The C++ solvers use a canonical material dependency order: captures reduce piece count, and promotions reduce pawn count. DTM is calculated via retrograde distance buckets. DTD-0 uses terminal seeds and shortest-path propagation within the WDL draw class. Four-man DTD-3 uses exact 4-cycle detection, shortest prefix propagation and the residual 6-cycle test. The resulting bound is <=16, so 8-cycle or longer repetitions cannot improve it. The exact material-word solver stores position-indexed suffix bitsets; it recomputes the high-distance draw cases for DTD-3. `path_repeat` updates working bitsets in place, so the runner always regenerates the DTD-0 masks first.

The released C++ and Python sources are organized by purpose. Python checks use a separately implemented board move generator. The eight selected five-man solvers use symmetry and identical-piece combinadic indexing; C++ direct audits check all legal moves, Python tests additionally sample states and recover explicit paths. The 728 strict global targets are certified using finite minimax or exact small-table reductions; a full six-man tablebase is unnecessary for these positive existence claims. UNKNOWN rows remain untouched.

## Release verification

This consolidated release rechecked the following against the existing computed tables and saved final proof data:

| Check | Result |
| --- | --- |
| Candidate universes, pair upper closure | PASS: 134,918 NO pair rows, 1,002 propagated exclusions |
| Legal replay of all released strict positive paths | PASS |
| Four-man WDL / DTM+DTD-0 / DTM+DTD-3 path witnesses | PASS: 1,280 / 940 / 940 |
| Strict global records | PASS: 1,020; zero failures |
| Five-man strict positive edges / same-layer pairs / lower pairs | PASS: 1,784 / 316 / 1,981 |
| Direct five-man NO edge filters | PASS: 192 using previously generated exact target statistics |
| WDL proof graph and final seven-/eight-man witnesses | PASS: 16,381 proof-tree nodes, 2 explicitly trusted external WDL anchors |
| Absolute positional barrier list | PASS: 4,332 expanded positions, 2,268 genuine WDL barriers, using previously computed predecessor flags |
| All C++ sources | PASS: C++17 syntax compilation |

The four-man and selected five-man numerical tables were originally computed exhaustively and audited before consolidation. The full clean unpack-to-finish regeneration of billions of move checks was **not** rerun for this release. The final checkers were run against the existing generated tables; some full-stage scripts combine those previously tested components with a new orchestrator. No claim of complete independent external tablebase comparison is made. The WDL six-man existence classification is based on published statistics, with two external decisive anchors explicitly listed; the seven-man WDL proof graph check is conditional on their correctness. The main strict global certificates do not use those two external anchors.

## Data conventions

FEN clocks in witness files are normalized to 0/1; castling is disabled. All distances are plies. White-relative WDL `1,0,-1` is not the sign of the side-to-move tablebase value. Canonical counts use solver-specific symmetry/index conventions; do not combine these with physical-board counts without multiplicity weighting. CSV `YES` means a concrete existential witness; `NO` means an exclusion proved by the indicated model and method; `UNKNOWN` means no proof has been retained. For the five-man matrices, `status_both_models` refers to the common strict status for DTM and both draw variants, with UNKNOWN left conservative. The WDL results use the distinct WDL-only model. The exact five-man endpoint counts include only submaterials of the solved sources; missing targets outside the possible submaterial universe are impossible by material constraints.

## Remaining work

Complete the 102 missing color-canonical five-man strict tables, then reclassify all 1,436 unknown direct edges and the remaining endpoint pairs. Develop complete handling of arbitrary repetition histories only if the application requires it. Search live-target and source-specific barriers with exact boundary sets; do not treat an unobserved witness as a NO. Establish historical reachability separately before drawing conclusions about actual opening play. No strict global saturation claim beyond six-man starts, and no solution of the standard initial chess position, is made.
