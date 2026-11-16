# Optimal Material Reachability in Chess

Which material compositions can occur in a game where **every move by both players is optimal from the standard starting position**?

This project studies that question in a precise chess model without draw claims or automatic draws by move count or repetition. It separates three facts that are easy to conflate: a material can occur in a legal game, it can occur in a position with a given theoretical outcome, and it can occur after a fully optimal prefix from the opening.

## Research progress

The [Stage A analysis](docs/stage-a-complexity.md) proves a reduction in an explicit game family: even with a guaranteed winning start and a single material resource that can only disappear, deciding whether an outcome-compatible material is missing from all strict optimal paths can encode another game's WDL result. This is **not** a reduction for orthodox chess. It shows why a smaller answer and monotone material alone do not make the chess question easier.

The [Stage A2 audit](docs/stage-a2-literature.md) checks exact theorems about reachability games, quantitative optimal play, abstraction soundness, generalized chess, historical reachability, and endgame-table metrics. It identifies the missing chess-specific step: a sound, useful cover of **all** optimal first entries from `s₀` into a chosen material layer.

[Stage B](docs/stage-b-targets.md) screens mechanism-driven materials and records three independently replayed historical terminal witnesses: White mate with 31 pieces, Black mate with 31 pieces, and a 26-piece stalemate. These establish `H_W`, `H_L`, and `H_D` examples, respectively; none proves an optimal opening path or a forbidden material.

[Stages D–F](docs/stages-d-f.md) prove a rank-budget first-entry barrier: a complete cover of optimal entries with local DTM smaller than the legal distance to a target would exclude that target without knowing opening DTM. No such cover has yet been certified for a concrete forbidden material. The document records the best conditional conclusion in each W, D-WDL, D-DTD, and L case.

### Conditional chess restriction

In the draw model where both players use the shortest path to a terminal draw as a tie-breaker, an optimal game that reaches `KP–K` cannot later reach a **nonterminal** `KQ–K` or `KR–K` for the same side. In particular, neither of these material sequences can occur:

```text
KP–K → KQ–K → K–K
KP–K → KR–K → K–K
```

The proof uses the legal choice to promote to a bishop or knight, immediately creating a dead position. It does not need the value or mate distance of the opening. A queen or rook promotion that itself causes stalemate is a terminal exception; the theorem does not exclude its material. See the [complete statement and proof](docs/result.md).

This is a **conditional trajectory restriction**, not a proof that any material is absent from every optimal opening game. A related shorter observation was already present in the previous local release; no novelty claim is made for it. The main conjecture remains open for a White win, a draw under either draw policy, and a Black win.

## Research map

| Document | Purpose |
| --- | --- |
| [Problem and rules](docs/problem.md) | Full state, optimality, material sets, and four conditional cases |
| [Stage A: complexity](docs/stage-a-complexity.md) | Formal reduction, exact dependencies, and limits for chess |
| [Stage A2: theorem audit](docs/stage-a2-literature.md) | Source-specific transfer map and the missing lemma |
| [Stage B: target screening](docs/stage-b-targets.md) | Verified historical controls and ranked candidate mechanisms |
| [Stage C: existence attempts](docs/stage-c-existence.md) | Failed counting, horizon, and local-barrier arguments with exact missing conditions |
| [Stages D–F: barrier and conclusions](docs/stages-d-f.md) | Proved transfer criterion, chess attempts, four-case status, and application limits |
| [Proved result](docs/result.md) | Self-contained proof, terminal exception, and supporting lemmas |
| [Methods and next steps](docs/methods.md) | Literature, proof mechanisms, candidate targets, and missing links |
| [Prior local study](docs/prior-work.md) | Relevant endgame findings from the previous release and their limits |
| [Research standards](CONTRIBUTING.md) | Evidence and reproducibility requirements for new claims |

## Scope and status

- **Proved in this investigation:** the abstract-game reduction and its limits; the rank-budget first-entry criterion; the draw-policy inclusion; and a 79/80-ply historical lower bound for nine queens. The promotion-fork proof is given self-containedly, with prior-work provenance.
- **Available as prior local evidence:** small-endgame transition and path results in [release `457fc79`](https://github.com/polilog/chess-material-dynamics/tree/457fc79d507ef5c3c78b5450f964f1df438976ca). Their model omits castling and does not certify optimal prefixes from the opening.
- **Open:** whether any outcome-compatible, historically reachable material is absent from every fully optimal game from the standard start.

The former endgame data and solvers remain accessible in Git history at the linked release. The current working tree focuses on results that bear directly on the opening-position question. The short historical witnesses are reproducible with `python3 -m pip install -r requirements.txt` followed by `python3 scripts/verify_historical_witnesses.py`. No chess engine evaluation is treated as a proof of the starting position's value.

Stages A–F now have explicit interim conclusions. The research remains active: no candidate has yet passed the required combination of historical witness, compatible WDL proof, and global exclusion from all optimal opening paths.
