# Research standards

This is a mathematical research project. Every claim should state its game rules, quantifiers, evidence, and scope.

## Claim types

- **Theorem:** provide a complete proof covering every legal opponent reply and every equally optimal move when the claim requires them.
- **Verified computational certificate:** provide input positions or histories, exact solver rules and metric, a reproducible checker, and the result of running it. Identify any trusted external table or unverified binary.
- **Candidate:** say exactly which of historical reachability, WDL compatibility, and optimal reachability remain unproved.
- **Open/unknown:** absence of a found path or counterexample is not an exclusion.

## Before promoting a candidate to a result

1. Fix whether terminal states are included and whether the draw policy is D-WDL or D-DTD.
2. For historical reachability, provide a complete legal game from `s₀`; a plausible FEN is insufficient.
3. For WDL compatibility, prove at least one historically reachable state with the required value. A cooperative mate or stalemate does not determine the value of an earlier position.
4. For global exclusion, cover **all** full states of the target material that could be reached by **any** optimal opening prefix. A local endgame barrier needs an unavoidable entry argument.
5. For a minimax numerical claim, include all defender alternatives and use DTM/DTD under the stated rules. Do not use DTZ or engine evaluation as an exact DTM substitute.
6. Check whether a new conclusion is already implied by the [prior release](docs/prior-work.md) or published literature. State the exact transfer and any new lemma.

Keep prose, code comments, filenames, and committed artifacts in English. Do not commit generated binary tables or a Git commit unless the repository owner explicitly asks for one.
