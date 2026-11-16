#!/usr/bin/env python3
"""Regenerate the KQQQvK turn-sensitive boundary with the released solver.

This builds a source-derived three-/four-/five-man subset; it is not an
independent move generator. Outputs stay in the ignored work directory.
"""

import argparse
import csv
import os
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
HEADERS = "\n".join(
    f"#include <{name}>"
    for name in (
        "algorithm", "array", "atomic", "cassert", "cmath", "cstdint",
        "cstring", "filesystem", "fstream", "functional", "iostream",
        "limits", "map", "mutex", "numeric", "queue", "random", "set",
        "sstream", "string", "thread", "tuple", "unordered_map",
        "unordered_set", "utility", "vector",
    )
)


def replace_unique_line(source: str, prefix: str, replacement: str) -> str:
    lines = source.splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    if len(matches) != 1:
        raise ValueError(f"Expected one source line starting with {prefix!r}")
    lines[matches[0]] = replacement
    return "\n".join(lines) + "\n"


def prepare(work: Path) -> None:
    for subdir, name in (("four", "solve.cpp"), ("four", "strict.cpp"),
                         ("five", "solve5.cpp")):
        target = work / subdir / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / "src" / subdir / name, target)

    solve = work / "four" / "solve.cpp"
    source = solve.read_text()
    source = source.replace("#include <bits/stdc++.h>", HEADERS)
    setup = next(line for line in source.splitlines() if line.startswith("void setup(){"))
    if "add(0,0,0);" not in setup:
        raise ValueError("The source setup function changed")
    subset_setup = setup.split("add(0,0,0);")[0]
    subset_setup += "add(0,0,0);add(Q,0,0);add(Q,Q,0);}"
    source = replace_unique_line(source, "void setup(){", subset_setup)
    source = replace_unique_line(
        source, "int main(){",
        "int main(){init();setup();for(int i=0;i<(int)ts.size();i++)solve(i);return 0;}",
    )
    solve.write_text(source)

    strict = work / "four" / "strict.cpp"
    source = replace_unique_line(
        strict.read_text(), "void dist_main(){",
        "void dist_main(){init();setup();load();ds.resize(ts.size());"
        "for(int i=0;i<(int)ts.size();i++)calc(i);}",
    )
    strict.write_text(source)


def run(work: Path, compiler: str) -> None:
    for subdir, source, binary, arg in (
        ("four", "solve.cpp", "solve", None),
        ("four", "strict.cpp", "strict", None),
        ("five", "solve5.cpp", "solve5", "Q"),
    ):
        directory = work / subdir
        subprocess.run(
            [compiler, "-O3", "-std=c++17", "-pthread", source, "-o", binary],
            cwd=directory, check=True,
        )
        command = [str(directory / binary)]
        if arg:
            command.append(arg)
        subprocess.run(command, cwd=directory, check=True)


def verify(work: Path) -> None:
    import chess

    for name in ("KQQQvK_stats.tsv", "KQQQvK_hist.tsv"):
        actual = (work / "five" / name).read_bytes()
        expected = (ROOT / "results" / "five" / "exact" / name).read_bytes()
        if actual != expected:
            raise AssertionError(f"Regenerated {name} differs from the release")
    with (work / "five" / "KQQQvK_stats.tsv").open() as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if [(r["turn"], r["reach_3"]) for r in rows[:2]] != [("0", "0"), ("1", "8611")]:
        raise AssertionError("Unexpected turn-sensitive reachability counts")
    if rows[2]["material"] != "audit_errors" or rows[2]["turn"] != "0":
        raise AssertionError("Bellman audit errors were recorded")
    with (ROOT / "results" / "five" / "exact" / "heavy_triples_witnesses.csv").open() as handle:
        witness = next(
            row for row in csv.DictReader(handle)
            if row["piece"] == "Q" and row["turn_black"] == "1"
            and row["target_pieces"] == "3"
        )
    board = chess.Board(witness["FEN"])
    if not board.is_valid():
        raise AssertionError("The positive witness starts at an invalid position")
    for uci in witness["UCI_moves"].split():
        move = chess.Move.from_uci(uci)
        if move not in board.legal_moves:
            raise AssertionError(f"Illegal positive-witness move: {uci}")
        board.push(move)
    if board.fen().split()[:4] != witness["target_FEN"].split()[:4]:
        raise AssertionError("The positive witness misses its stated target position")
    print("PASS KQQQvK: 0 White-to-move strict paths to KQvK; 8,611 Black-to-move paths")
    print("PASS released statistics and histograms match the regenerated subset")
    print("PASS Black-to-move positive path replays legally with python-chess")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, default=ROOT / "work" / "queen_boundary")
    parser.add_argument("--cxx", default=os.environ.get("CXX", "c++"))
    args = parser.parse_args()
    work = args.work.resolve()
    prepare(work)
    run(work, args.cxx)
    verify(work)


if __name__ == "__main__":
    main()
