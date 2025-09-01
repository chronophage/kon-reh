__all__ = []
__version__ = "0.1.0"
if __name__ == "__main__":
    g = GameState()
    g.begin_turn()  # A turn 1
    print("\n".join(g.snapshot()["grid_rows_top_7_to_0"]))

    # A: develop a Red HL 1 (homeward-left = South for A) is illegal on first turn; try OL 2 (onward exact for Red)
    a_reds = g.pieces_of("A", PType.RED)
    pid = a_reds[0]
    mv = [m for m in g.legal_moves_for(pid) if m.dir_label in ("OL","OR") and m.steps == 2][0]
    g.apply_move(mv)  # A plays
    g._finish_turn_and_switch()  # not needed; apply_move calls finish automatically

    # B: opening double—two moves, not same piece
    g.begin_turn()
    b_orange = g.pieces_of("B", PType.ORANGE)[0]
    m1 = [m for m in g.legal_moves_for(b_orange) if m.dir_label in ("OL","OR") and m.steps == 3][0]
    g.apply_move(m1)
    # second move (different piece)
    b_red = [x for x in g.pieces_of("B", PType.RED) if x != b_orange][0]
    m2 = [m for m in g.legal_moves_for(b_red) if m.dir_label in ("OL","OR") and m.steps == 2][0]
    g.apply_move(m2)

    # A turn again
    g.begin_turn()
    print("To move:", g.snapshot()["to_move"]
