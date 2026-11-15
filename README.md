# Chess Material Dynamics

**Exact endgame reachability under WDL, distance-to-mate, and shortest-draw optimality.**

This research project asks which material compositions can occur along strictly optimal chess games, and whether constraints proved in small endgames can rule out entire trajectories from larger positions. It studies both individual material transitions and the compatibility of whole sequences. A material graph is used as a conservative abstraction, not as a substitute for positional reachability.

[Краткое описание на русском](docs/ru.md)

## Current results

The primary model is **DTM + DTD**: the winner minimizes the number of plies to mate, the loser maximizes it, and in a draw both players minimize the time to a WDL-preserving terminal draw. DTD-0 ends at stalemate/dead position; DTD-3 also ends at automatic third occurrence from a fresh history. See [the model and theorems](docs/model-and-theorems.md) for precise definitions.

| Result | Status |
| --- | --- |
| Exact WDL, DTM, DTD-0 and fresh DTD-3, up to four men | Complete in the stated model |
| Four-man material classes | 66 materials, 146 admissible material/outcome pairs |
| Four-man material edges | 356 strict edges; 62 additional WDL-forbidden candidate edges |
| Four-man material words | 1,304 candidates; 940 strict YES, 364 NO |
| Four-man endpoint pairs | 488 strict YES, 29 NO (all 517 WDL-reachable) |
| Five-man WDL existence | 220 materials, 582 admissible pairs, 78 impossible outcomes |
| Global strict reachability from five men | 146/146 targets through four men |
| Global strict reachability from six men | 728/728 targets through five men |
| Exact five-man DTM/DTD tables | 8 color-canonical materials (16/220 color-sensitive materials) |
| Five-man strict edges | 1,784 YES / 192 NO / 1,436 UNKNOWN |
| Five-man strict pairs to smaller layers | 1,981 YES / 24,034 NO / 2,985 UNKNOWN |
| Five-man strict same-layer pairs | 316 YES / 110,884 NO / 2,140 UNKNOWN |

**The five-man strict graph is not complete.** There is no established finite global material-origin barrier for any admissible target through five men. Pairwise barriers, however, already yield general theorems for arbitrarily large formal materials.

### Main scientific findings

- Strict time optimality retains about 27.25% of concrete WDL-preserving moves up to four men, yet all 356 individual material edges survive. It eliminates 340 further material words and 29 endpoint pairs. Thus even endpoint reachability in the projected material graph is not exact.
- 62 small-layer pairs are reachable only with a particular initial side to move. A first-capture boundary fixes the receiving side to move, making these conditional exclusions useful on larger layers.
- Global reachability is saturated from six men for all 728 admissible targets through five men, with individual compatible FEN/UCI certificates. This is not an induction claim for seven or more men.
- General DTM barriers include `KQ^a v K -> KQvK` for `a >= 4`, `KQ^a R v K -> KRvK` for `a >= 3`, and `KB^a NN v K -> KNNvK` for `a >= 1` (decisive outcome preserved). The boundary proof is computationally exhaustive at the relevant small material.
- Under shortest-draw optimality, a one-sided material with at least five men cannot reach a drawn `KQvK` or `KRvK`. A separate family excludes `KPvK` from `KPvKQ^a`, `a >= 2`, for a pawn-side win even under WDL, and for a draw under DTD.
- A secondary WDL experiment establishes 2,555/2,723 targets through six men from seven men (168 UNKNOWN), and 2,268 genuine absolute WDL position barriers through three men. These results do **not** imply strict reachability.

Read the [consolidated results](docs/results.md), [proofs and definitions](docs/model-and-theorems.md), and [reproduction guide](docs/reproduction.md). No claim of solving chess, novelty priority, or historical reachability from the opening is made.

## Repository layout

```text
results/
  four/          exact small-layer classifications and witness paths
  five/          final partial strict matrices and eight exact materials
  global/        all strict certificates from five and six men
  propagation/   certified larger-layer pair exclusions
  wdl/           secondary WDL classification and positional barriers
proofs/          WDL proof dependency graph and two external anchors
src/             C++17 retrograde solvers and Python checkers
scripts/         reproducible build and verification entry points
docs/            mathematical model, results, data format, limitations
```

There are no historical ZIP files, search-batch logs, obsolete matrices, compiled executables or multi-gigabyte tablebases in the repository. The proof dependency graph is retained because it supports the WDL results. Final result tables are read-only inputs to the checkers; generated data go to `work/`.

## Quick start

Python 3.10+; for exhaustive calculation, a C++17 compiler (tested with GCC), Linux/WSL, and NumPy. The complete computation requires several GB of RAM and at least 12 GB of free storage. A full run is a substantial computation, not a quick unit test.

```bash
python -m pip install -r requirements.txt
python scripts/reproduce.py structure
python scripts/reproduce.py certificates
```

The first command checks all final table keys, the negative pair closures, and the legality of positive witness paths without binary tablebases. The second generates or reuses the exact <=4 tablebases and checks all 1,020 strict certificate records (146 targets from five men in two draw models, plus 728 targets from six men). It also checks all four-man positive material paths under WDL, DTM and DTD.

Other stages:

```bash
python scripts/reproduce.py four
python scripts/reproduce.py five
python scripts/reproduce.py wdl
python scripts/reproduce.py wdl-four
python scripts/reproduce.py full
```

The full stage reruns all completed calculations, not the unresolved five-man search. See the [verification record](docs/reproduction.md#release-verification) for what was actually rerun in this release.

## Interpretation and scope

The model uses local legal positions, no castling or move-count rules, and an explicit automatic-repetition convention. It is not the full FIDE game. WDL is White-relative (`+1`, `0`, `-1`); all distances are in plies; material includes both kings. Table counts use the documented canonicalization, not counts of distinct physical boards. A `YES` is an existential witness, a `NO` is a proved exclusion in the model, and `UNKNOWN` is neither.

A shorter-mate or shorter-draw preference does not by itself certify the WDL of an unknown position. In particular, DTD describes cooperative tie-breaking **after** preserving the independently established minimax draw, not a drawing strategy against a player who refuses a short draw.

## External reference

The earlier WDL classification of six-man materials and two exact decisive WDL anchors use the published [ChessDB endgame statistics](https://www.chessdb.cn/egtb_infoc.html). The five-man existence classification is independently supported by the strict certificates and elementary no-mate arguments. The included retrograde tables have been audited internally, but have not undergone a complete independent binary comparison with external tablebases.
