#!/usr/bin/env python3
"""Regenerate the KQvKP WDL boundary in a focused source-derived subset.

The retrograde calculation reuses the released move generator. The concrete
draw-policy contrast is additionally replayed with python-chess.
"""

import argparse
import os
from pathlib import Path
import shutil
import subprocess

import chess

from reproduce_queen_boundary import HEADERS, replace_unique_line


ROOT = Path(__file__).resolve().parents[1]
CONTRAST_FEN = "k7/2p5/1Q1K4/8/8/8/8/8 w - - 0 1"


def prepare(work: Path) -> None:
    for subdir, name in (("four", "solve.cpp"), ("five", "wdl_turn.cpp")):
        target = work / subdir / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / "src" / subdir / name, target)
    solve = work / "four" / "solve.cpp"
    source = solve.read_text().replace("#include <bits/stdc++.h>", HEADERS)
    setup = next(line for line in source.splitlines() if line.startswith("void setup(){"))
    if "add(0,0,0);" not in setup:
        raise ValueError("The source setup function changed")
    subset_setup = setup.split("add(0,0,0);")[0]
    subset_setup += "add(0,0,0);for(int a=1;a<=5;a++)add(a,0,0);"
    subset_setup += "for(int b:{Q,R,BI,N,P})add(Q,b,1);}"
    source = replace_unique_line(source, "void setup(){", subset_setup)
    source = replace_unique_line(
        source, "int main(){",
        "int main(){init();setup();for(int i=0;i<(int)ts.size();i++)solve(i);return 0;}",
    )
    solve.write_text(source)


def run(work: Path, compiler: str) -> None:
    for subdir, source, binary in (("four", "solve.cpp", "solve"),
                                   ("five", "wdl_turn.cpp", "wdl_turn")):
        directory = work / subdir
        subprocess.run(
            [compiler, "-O3", "-std=c++17", "-pthread", source, "-o", binary],
            cwd=directory, check=True,
        )
        result = subprocess.run(
            [str(directory / binary)], cwd=directory, check=True,
            capture_output=subdir == "five", text=True,
        )
        if subdir == "five":
            lines = result.stdout.splitlines()
            expected = [
                "KQvKP\t-1\tdirect=361708\tqueen_turn=0\tpawn_turn=361708",
                "queen_turn_FEN\t0\t" + CONTRAST_FEN,
                "KQvKP\t0\tdirect=235211\tqueen_turn=1\tpawn_turn=235211",
            ]
            if lines != expected:
                raise AssertionError(f"Unexpected KQvKP boundary: {lines}")


def verify_contrast() -> None:
    start = chess.Board(CONTRAST_FEN)
    if not start.is_valid() or not start.is_check():
        raise AssertionError("The draw contrast must begin in legal check")
    immediate = start.copy()
    immediate.push_san("Qxc7")
    if not immediate.is_stalemate():
        raise AssertionError("Qxc7 must be a terminal draw in one ply")
    for move in start.legal_moves:
        if move.to_square == chess.C7:
            after = start.copy()
            after.push(move)
            if not after.is_stalemate():
                raise AssertionError("Capturing the pawn must immediately stalemate")
            continue
        if start.piece_at(move.from_square).piece_type != chess.KING:
            raise AssertionError("An unexpected queen reply may escape the argument")
        after = start.copy()
        after.push(move)
        if chess.Move.from_uci("c7b6") not in after.legal_moves:
            raise AssertionError("Black must be able to capture the White queen")
    longer = start.copy()
    longer.push_san("Kc6")
    if [move.uci() for move in longer.legal_moves] != ["c7b6"]:
        raise AssertionError("Black must have only the queen capture after Kc6")
    for san in ("cxb6", "Kxb6"):
        longer.push_san(san)
    if not longer.is_insufficient_material():
        raise AssertionError("The longer path must end at bare kings")
    print("PASS KQvKP: pawn-side win has no queen-turn WDL path to KPvK")
    print("PASS drawn exception: Kc6 cxb6 Kxb6 is legal; Qxc7 and Kxc7 stalemate")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, default=ROOT / "work" / "pawn_queen_boundary")
    parser.add_argument("--cxx", default=os.environ.get("CXX", "c++"))
    args = parser.parse_args()
    run_work = args.work.resolve()
    prepare(run_work)
    run(run_work, args.cxx)
    verify_contrast()


if __name__ == "__main__":
    main()
