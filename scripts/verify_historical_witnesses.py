#!/usr/bin/env python3
"""Replay short historical terminal witnesses; this is not an optimality test."""

import json
from pathlib import Path

import chess


ROOT = Path(__file__).resolve().parents[1]
WITNESSES = ROOT / "data" / "historical_witnesses.json"
PIECES = (chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN)


def material(board: chess.Board, color: chess.Color) -> list[int]:
    return [len(board.pieces(piece, color)) for piece in PIECES]


def verify(record: dict) -> None:
    board = chess.Board()
    for move in record["san"].split():
        board.push_san(move)
    assert len(board.move_stack) == record["plies"], record["id"]
    assert board.fen() == record["fen"], record["id"]
    assert material(board, chess.WHITE) == record["material"]["white"], record["id"]
    assert material(board, chess.BLACK) == record["material"]["black"], record["id"]
    outcome = record["terminal"]
    if outcome == "white_win":
        assert board.is_checkmate() and board.turn == chess.BLACK, record["id"]
    elif outcome == "black_win":
        assert board.is_checkmate() and board.turn == chess.WHITE, record["id"]
    elif outcome == "draw_stalemate":
        assert board.is_stalemate(), record["id"]
    else:
        raise ValueError(f"Unknown terminal outcome: {outcome}")


def main() -> None:
    records = json.loads(WITNESSES.read_text())
    for record in records:
        verify(record)
        print(f"PASS {record['id']}: {record['plies']} plies, {record['terminal']}")


if __name__ == "__main__":
    main()
