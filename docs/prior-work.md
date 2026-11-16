# Relevant prior local endgame study

The previous release is preserved at commit [`457fc79d507e`](https://github.com/polilog/chess-material-dynamics/tree/457fc79d507ef5c3c78b5450f964f1df438976ca). It includes the solvers, tables, proof records, and reproduction instructions removed from the present working tree. The current project uses those findings only where they can inform a proof from the standard start.

## Findings worth carrying forward

- The release reports complete WDL/DTM/shortest-draw classifications through four pieces in its **local** model, plus selected five-piece tables. Its strict material graph retains individual edges that fail to compose into legal optimal material words. This supports retaining full-state transition relations rather than a graph of material labels alone.
- Its first-capture argument propagates a boundary exclusion to larger **local** material layers when every path must cross the boundary with the relevant side to move. Examples reported there include `KQ^a–K → KQ–K` for `a≥4` under winning-side DTM, and `KP–KQ^a → KP–K` for `a≥2` under stated WDL/DTD conditions.
- It reports local positive saturation from six pieces to every outcome-compatible target through five pieces. This is evidence against expecting a small universal *material-origin* barrier. It does not establish any path from the standard start.
- The release itself states that its local states need not have a legal opening history, its solver omits castling, and it has **no established global forbidden material from `s₀`**. These limitations are central to the revised problem, not footnotes.

The original release's `structure` command passed in this session: it checked candidate keys, 134,918 stored negative pair rows, 1,002 propagated exclusions, and legal replay of the saved positive paths. This is a structural and witness-replay check. We did **not** regenerate the large binary endgame tables or independently validate every numerical classification. The [original verification notes](https://github.com/polilog/chess-material-dynamics/blob/457fc79d507ef5c3c78b5450f964f1df438976ca/docs/reproduction.md) describe the scope of its own release checks.

## Why the old corpus is in history

Most old files classify locally legal endgame positions or verify tabulated transitions. That work is relevant background, but the central object here is the union of **all fully optimal histories from one fixed opening state**. Keeping the complete old corpus in the live tree would make local results look like answers to the new question. The exact previous source and data remain recoverable from Git history, while this working tree contains the model, proofs, evidence status, and proposed global proof mechanism.
