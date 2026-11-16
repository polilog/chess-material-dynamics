# Stage B — target selection after the theorem audit

**Status:** candidate screening, not a forbidden-material theorem. The Stage A/A2 conclusion changes the choice of targets: a useful target needs a historically verified state *and* a small, provably mandatory optimal-entry frontier. Material strangeness or a local DTM witness alone is not enough.

## Verified historical and outcome-compatible controls

The four complete games below were replayed from the standard array with `python-chess` 1.11.2. The script checks every SAN move, final FEN, piece counts, and the terminal result. Terminal checkmate or stalemate proves the displayed state's WDL in our no-repetition/no-move-counter model. It says nothing about the optimality of the prefix.

| Outcome | Legal game | Final material (P,N,B,R,Q by color) | Status |
| --- | --- | --- | --- |
| W | `1.e4 e5 2.Qh5 Nc6 3.Bc4 Nf6 4.Qxf7#` | White `(8,2,2,2,1)`; Black `(7,2,2,2,1)` | A concrete element of `H_W` with 31 pieces. |
| W | `1.e4 f6 2.e5 fxe5 3.d4 g5 4.Qh5#` | White `(7,2,2,2,1)`; Black `(8,2,2,2,1)` | A 31-piece `H_W` control with all Black resources intact and no White capture. |
| L | `1.f4 e5 2.g4 exf4 3.h3 Qh4#` | White `(7,2,2,2,1)`; Black `(8,2,2,2,1)` | A concrete element of `H_L` with 31 pieces. |
| D | Loyd's `1.e3 a5 2.Qh5 Ra6 3.Qxa5 h5 4.Qxc7 Rah6 5.h4 f6 6.Qxd7+ Kf7 7.Qxb7 Qd3 8.Qxb8 Qh7 9.Qxc8 Kg6 10.Qe6` | White `(8,2,2,2,1)`; Black `(4,1,1,2,1)` | Terminal stalemate, hence a concrete element of `H_D` with 26 pieces. [Historical account](https://www.chesshistory.com/winter/extra/loyd.html). |

Machine-readable records are in [historical_witnesses.json](../data/historical_witnesses.json). Run `python3 -m pip install -r requirements.txt` and `python3 scripts/verify_historical_witnesses.py` from the repository root. The check validates the terminal witnesses, not any minimax property of their earlier positions.

The first W and L controls differ by which side loses a pawn. Their histories do not imply a color-symmetry relation for optimal play from `s₀`, because White moves first. The additional W control shows that Black can retain all 16 resources and White can avoid captures in a historically reachable White-winning state; material surplus alone cannot exclude the 18-piece pilot. The D witness has six Black resources removed and a proven terminal draw; its 19-ply legal history is **not** an upper bound on `DTD(s₀)` under `V(s₀)=D`, since intermediate positions have not been shown to remain in the D region.

## Mechanism-driven candidates

| Conditional case | Class | Established evidence | Missing decisive link | Priority |
| --- | --- | --- | --- | --- |
| W | Extreme `KP–KQ⁹` with a pawn-side win | Nine Black queens require all eight Black promotions and at least 80 elapsed plies. A historical/local-DTM witness was reported in the research brief but was **not** reproduced from the inspected release. | Verify a legal history and WDL for one position; then rule out **every** optimal opening route to the entire material class, perhaps by an independent DTM upper bound or an unavoidable early-phase resource invariant. | Medium scientific interest; low current provability. |
| W | Outcome-compatible small material after a mandatory capture frontier | The [retained local theorems](model-and-theorems.md#3-general-material-barriers-from-exact-boundaries) report exact endgame pair barriers, but their source states are not known to lie on optimal opening paths. | Find a target with verified `H_W`, then prove all optimal first entries into its layer lie in the forbidden source set. | Highest proof-method priority. |
| D-WDL | A drawn terminal material requiring irreversible captures, such as the verified 26-piece Loyd material | `H_D` membership is proved by a complete terminal witness. | A D-WDL path may cycle and has no distance rank; a material-only exclusion needs an unavoidable value barrier or stronger invariant. | Medium. |
| D-DTD | A high-cost drawn material, with the 26-piece witness as a control | DTD gives a strict distance gradient whenever finite; the promotion-fork theorem forbids one ordered segment. | Prove a **D-preserving** short terminal-draw route from `s₀` or a local DTD budget that applies to all first-entry states. A merely legal short stalemate is insufficient. | Medium until the D-preserving route is certified. |
| L | Color-reflected extreme or small-boundary classes | A 31-piece Black-mate material is verified in `H_L`; local endgame statements can be color-reflected. | An optimal opening prefix and compulsory boundary remain unproved; color reflection alone changes the moving side. | Same method priority as W, not an automatic corollary. |

The table intentionally declines to nominate an extreme material as the main theorem target. The first research objective is to obtain a compact **opening-to-frontier** lemma for one class; only then should a local boundary computation be expanded. A target with `H_v` proved but no plausible compulsory frontier is a useful control, not the best proof candidate.

## Rejected shortcuts

- Counting the number of materials in one optimal game does not bound the union over all equally optimal games.
- A path from an arbitrary winning endgame to a target cannot be prepended to an unproved optimal opening path.
- A legal cooperative stalemate does not prove that the same history is D-WDL or D-DTD optimal.
- A strict DTM exclusion need not be safe for WDL proof pruning, where the defender's slower-mate choices may still matter.
