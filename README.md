# Optimal Material Reachability in Chess

Which material compositions can occur in a game where **every move by both players is optimal from the standard starting position**?

This project studies that question in a precise chess model without draw claims or automatic draws by move count or repetition. It separates three facts that are easy to conflate: a material can occur in a legal game, it can occur in a position with a given theoretical outcome, and it can occur after a fully optimal prefix from the opening.

## Current result

In the draw model where both players use the shortest path to a terminal draw as a tie-breaker, an optimal game that reaches `KP–K` cannot later reach a **nonterminal** `KQ–K` or `KR–K` for the same side. In particular, neither of these material sequences can occur:

```text
KP–K → KQ–K → K–K
KP–K → KR–K → K–K
```

The proof uses the legal choice to promote to a bishop or knight, immediately creating a dead position. It does not need the value or mate distance of the opening. A queen or rook promotion that itself causes stalemate is a terminal exception; the theorem does not exclude its material. See the [complete statement and proof](docs/result.md).

This is a **conditional trajectory restriction**, not a proof that any material is absent from every optimal opening game. The main conjecture remains open for a White win, a draw under either draw policy, and a Black win.

## Research map

| Document | Purpose |
| --- | --- |
| [Problem and rules](docs/problem.md) | Full state, optimality, material sets, and four conditional cases |
| [Proved result](docs/result.md) | Self-contained proof, terminal exception, and supporting lemmas |
| [Methods and next steps](docs/methods.md) | Literature, proof mechanisms, candidate targets, and missing links |
| [Prior local study](docs/prior-work.md) | Relevant endgame findings from the previous release and their limits |
| [Research standards](CONTRIBUTING.md) | Evidence and reproducibility requirements for new claims |

## Scope and status

- **Proved here:** the promotion-fork restriction, inclusion between the two draw reachability sets, and a 79/80-ply historical lower bound for nine queens.
- **Available as prior local evidence:** small-endgame transition and path results in [release `457fc79`](https://github.com/polilog/chess-material-dynamics/tree/457fc79d507ef5c3c78b5450f964f1df438976ca). Their model omits castling and does not certify optimal prefixes from the opening.
- **Open:** whether any outcome-compatible, historically reachable material is absent from every fully optimal game from the standard start.

The former endgame data and solvers remain accessible in Git history at the linked release. The current working tree focuses on results that bear directly on the opening-position question. No chess engine evaluation is treated as a proof of the starting position's value.
