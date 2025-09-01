# Core rules engine stubs (expand later).
class Game:
    def __init__(self):
        self.turn = 1
        self.state = {}

    def legal_moves(self):
        return []

    def apply(self, move):
        pass
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Iterable, Literal
import enum

Coord = Tuple[int, int]
Side = Literal["A", "B"]

# ------------------------- Constants & Geometry -------------------------

BOARD_MIN, BOARD_MAX = 0, 7
CENTRAL_FOUR: Set[Coord] = {(3, 3), (4, 3), (3, 4), (4, 4)}

HOME_APEX: Dict[Side, Coord] = {"A": (0, 0), "B": (7, 7)}
SANCTUMS: Tuple[Coord, Coord] = ((7, 0), (0, 7))  # two corners; opposites of one another
OPPOSITE_SANCTUM = {SANCTUMS[0]: SANCTUMS[1], SANCTUMS[1]: SANCTUMS[0]}

GLOBAL_GREEN_CAP = 6

# Movement lanes (cardinal on the diamond)
DIRS = {
    "N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)
}

def lanes_for(side: Side) -> Dict[str, Coord]:
    """Return the four lane vectors labelled OL/OR/HL/HR for a side."""
    if side == "A":
        return {"OL": DIRS["N"], "OR": DIRS["E"], "HL": DIRS["S"], "HR": DIRS["W"]}
    else:
        return {"OL": DIRS["S"], "OR": DIRS["W"], "HL": DIRS["N"], "HR": DIRS["E"]}

def is_on_board(p: Coord) -> bool:
    return BOARD_MIN <= p[0] <= BOARD_MAX and BOARD_MIN <= p[1] <= BOARD_MAX

def add(a: Coord, b: Coord) -> Coord:
    return (a[0] + b[0], a[1] + b[1])

def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# ------------------------- Pieces & State -------------------------

class PType(enum.Enum):
    BLUE = "B"
    ORANGE = "O"
    RED = "R"
    GREEN = "G"

@dataclass
class Piece:
    pid: int
    side: Side
    kind: PType
    pos: Optional[Coord]  # None if captured/removed (off-board)

@dataclass
class BlueLife:
    """Tracks everything that resets on Reforge."""
    used_hop: bool = False
    used_disp: bool = False
    rooted: bool = False
    left_home: bool = False  # has this life ever left Home Apex?
    banned_seed_sanctums: Set[Coord] = field(default_factory=set)

    # Central Four timing:
    cross_stay_consec: int = 0                 # consecutive own turns ended in Cross
    cross_exclusion_own_turns: int = 0         # cannot enter Cross while >0

    def specials_used_count(self) -> int:
        return (1 if self.used_hop else 0) + (1 if self.used_disp else 0)

    def reset_for_reforge(self):
        self.used_hop = False
        self.used_disp = False
        self.rooted = False
        self.left_home = False
        self.banned_seed_sanctums.clear()
        self.cross_stay_consec = 0
        self.cross_exclusion_own_turns = 0

@dataclass
class PlayerState:
    side: Side
    blue_pid: int
    blue_life: BlueLife = field(default_factory=BlueLife)
    reforge_countdown: Optional[int] = None  # 5 .. 0 (None when not active)
    # For Cross timing detection across turns:
    blue_in_cross_at_turn_start: bool = False

@dataclass
class Move:
    """
    A single-player action. For B's opening double-move, two Moves are applied
    in one 'turn'. A move can be a piece slide (with optional Blue special),
    and can request seeding if Blue ends on a Sanctum.
    """
    pid: int
    dir_label: str            # "OL","OR","HL","HR"
    steps: int                # slide length (0 allowed for Blue to special-in-place)
    blue_special: Optional[Literal["hop", "disp"]] = None
    special_dir: Optional[str] = None          # lane for the special ("OL"/"OR"/"HL"/"HR")
    seed_if_possible: bool = False             # request Twin Apex Seed if legal

@dataclass
class PlantChoice:
    """
    If a banner is planted (during Reforge), caller must specify one of:
      - place="apex" and optionally pay_pid (a Green) or pay_runner_if_green=True
      - place="sanctum" and sanctum:Coord (that Blue cannot Seed from same Sanctum this life)
      - place="home"
    """
    place: Literal["apex", "sanctum", "home"]
    sanctum: Optional[Coord] = None
    pay_pid: Optional[int] = None
    pay_runner_if_green: bool = True

class KonrehError(Exception): ...
class IllegalMove(KonrehError): ...
class GameOver(KonrehError): ...

# ------------------------- Game State -------------------------

class GameState:
    def __init__(self):
        self.pieces: Dict[int, Piece] = {}
        self.next_pid = 1
        self.current: Side = "A"
        self.turn_index_by_side = {"A": 0, "B": 0}

        # Opening double-move control
        self.b_opening_double_pending = True       # True until B finishes their first 2 moves
        self._double_first_pid: Optional[int] = None
        self._double_moves_done: int = 0

        # Create initial setup
        self.players: Dict[Side, PlayerState] = {
            "A": PlayerState(side="A", blue_pid=-1),
            "B": PlayerState(side="B", blue_pid=-1),
        }
        self._setup_initial_positions()

        # Derived
        self.game_over: bool = False
        self.winner: Optional[Side] = None

    # ----- Setup -----

    def _new_piece(self, side: Side, kind: PType, pos: Coord) -> int:
        pid = self.next_pid
        self.next_pid += 1
        self.pieces[pid] = Piece(pid=pid, side=side, kind=kind, pos=pos)
        return pid

    def _setup_initial_positions(self):
        # Ranks from each Home Apex outward (lengths 1-2-3-4)
        # Using A Home at (0,0), B Home at (7,7)
        # We mirror placements by symmetry.
        def lay_for(side: Side):
            hx, hy = HOME_APEX[side]
            # local basis: OL increases y (for A) or decreases y (for B)
            L = lanes_for(side)
            # Make a small helper to place along a diagonal-ish fan from home
            # We'll just place to match the document: R1 Blue, R2 two Oranges,
            # R3 Red-Green-Red, R4 four Reds (filling the "row" 4 squares away).
            # We'll compute four "frontier" squares per band along the OL/OR/HL/HR
            # but we can map them explicitly per side with a simple pattern.

            # Rank 1: Home apex = Blue
            bpid = self._new_piece(side, PType.BLUE, HOME_APEX[side])
            self.players[side].blue_pid = bpid

            # Rank 2: length 2 along Onward axes from home (one OL, one OR)
            r2_ol = add(HOME_APEX[side], L["OL"])
            r2_or = add(HOME_APEX[side], L["OR"])
            self._new_piece(side, PType.ORANGE, r2_ol)
            self._new_piece(side, PType.ORANGE, r2_or)

            # Rank 3: positions 2 steps away but along both OL/OR (a little diamond band).
            # We'll pick three squares roughly centered in front of home apex.
            # Compute two-step OL, OR, and the "between" by adding OL+OR.
            r3_c = add(HOME_APEX[side], add(L["OL"], L["OR"]))          # middle
            r3_ol2 = add(HOME_APEX[side], add(L["OL"], L["OL"]))        # OL twice
            r3_or2 = add(HOME_APEX[side], add(L["OR"], L["OR"]))        # OR twice
            # Place Red – Green – Red left to right from player's view (OL side considered "left")
            self._new_piece(side, PType.RED, r3_ol2)
            self._new_piece(side, PType.GREEN, r3_c)
            self._new_piece(side, PType.RED, r3_or2)

            # Rank 4: four Reds: OL*3, OL*2+OR*1, OL*1+OR*2, OR*3
            r4 = [
                add(HOME_APEX[side], add(add(L["OL"], L["OL"]), L["OL"])),
                add(HOME_APEX[side], add(add(L["OL"], L["OL"]), L["OR"])),
                add(HOME_APEX[side], add(L["OL"], add(L["OR"], L["OR"]))),
                add(HOME_APEX[side], add(add(L["OR"], L["OR"]), L["OR"])),
            ]
            for p in r4:
                self._new_piece(side, PType.RED, p)

        lay_for("A")
        lay_for("B")

    # ------------------------- Helpers -------------------------

    def side_of(self, pid: int) -> Side:
        return self.pieces[pid].side

    def pos_of(self, pid: int) -> Coord:
        pos = self.pieces[pid].pos
        if pos is None:
            raise IllegalMove("Piece is not on board.")
        return pos

    def piece_at(self, c: Coord) -> Optional[int]:
        for p in self.pieces.values():
            if p.pos == c:
                return p.pid
        return None

    def pieces_of(self, side: Side, kind: Optional[PType] = None) -> List[int]:
        return [
            p.pid for p in self.pieces.values()
            if p.side == side and p.pos is not None and (kind is None or p.kind == kind)
        ]

    def greens_total_on_board(self) -> int:
        return sum(1 for p in self.pieces.values() if p.pos is not None and p.kind == PType.GREEN)

    # ------------------------- ZoC -------------------------

    def zoc_squares(self, enemy: Side) -> Set[Coord]:
        z: Set[Coord] = set()
        for pid in self.pieces_of(enemy):
            p = self.pieces[pid]
            c = p.pos
            if c is None:
                continue
            for d in DIRS.values():
                n = add(c, d)
                if is_on_board(n):
                    z.add(n)
        return z

    # ------------------------- Movement Legality -------------------------

    def _onward_exact(self, kind: PType) -> int:
        return {PType.RED: 2, PType.ORANGE: 3, PType.GREEN: 4, PType.BLUE: 5}[kind]

    def _home_max(self, kind: PType) -> int:
        return {PType.RED: 1, PType.ORANGE: 2, PType.GREEN: 3, PType.BLUE: 4}[kind]

    def _dir_is_onward(self, side: Side, dir_label: str) -> bool:
        return dir_label in ("OL", "OR")

    def _vector_for(self, side: Side, dir_label: str) -> Coord:
        return lanes_for(side)[dir_label]

    # path stepping with ZoC stopping rules
    def _path_is_legal_slide(
        self, pid: int, start: Coord, dir_label: str, steps: int
    ) -> Tuple[bool, Optional[Coord], Optional[int]]:
        """Return (ok, dest, captured_pid) for a displacement slide (no Blue special here)."""
        mover = self.pieces[pid]
        v = self._vector_for(mover.side, dir_label)
        enemy = "A" if mover.side == "B" else "B"
        zoc = self.zoc_squares(enemy)

        if steps == 0:
            # Only legal as a pre-special Blue 'slide 0'; for others, disallow here.
            return (mover.kind == PType.BLUE, start, None)

        exact = self._onward_exact(mover.kind) if self._dir_is_onward(mover.side, dir_label) else None
        cap: Optional[int] = None
        cur = start

        for s in range(1, steps + 1):
            cur = add(cur, v)
            if not is_on_board(cur):
                return (False, None, None)

            occ = self.piece_at(cur)
            # Collision: cannot pass through any piece
            if occ is not None:
                if s == steps and self.pieces[occ].side != mover.side:
                    cap = occ  # capture by displacement allowed on final square
                else:
                    return (False, None, None)

            # ZoC: entering enemy ZoC ends move immediately; cannot 'pass through' ZoC
            if cur in zoc and s < steps:
                return (False, None, None)

        # Exactness
        if exact is not None and steps != exact:
            return (False, None, None)
        # Homeward length must be <= max
        if exact is None:
            if steps < 1 or steps > self._home_max(mover.kind):
                return (False, None, None)

        return (True, cur, cap)

    # ------------------------- Blue Specials -------------------------

    def _blue_special_ok(
        self, pid: int, kind: Literal["hop", "disp"], dir_label: str
    ) -> Tuple[bool, Optional[Coord], Optional[int]]:
        blue = self.pieces[pid]
        assert blue.kind == PType.BLUE
        v = self._vector_for(blue.side, dir_label)

        if kind == "disp":
            dst = add(blue.pos, v)
            if not is_on_board(dst):
                return (False, None, None)
            occ = self.piece_at(dst)
            if occ is not None and self.pieces[occ].side != blue.side:
                return (True, dst, occ)
            return (False, None, None)

        # hop
        mid = add(blue.pos, v)
        dst = add(mid, v)
        if not is_on_board(mid) or not is_on_board(dst):
            return (False, None, None)
        occ_mid = self.piece_at(mid)
        occ_dst = self.piece_at(dst)
        if occ_mid is None or occ_dst is not None:
            return (False, None, None)
        if self.pieces[occ_mid].side == blue.side:
            return (False, None, None)
        return (True, dst, occ_mid)

    # ------------------------- Reforge Placement -------------------------

    def _apply_reforge_placement(
        self, side: Side, choice: PlantChoice, runner_pid: int
    ):
        ps = self.players[side]
        # Clear old Blue (already captured earlier; ensure pid is off)
        blue_pid = ps.blue_pid
        blue_piece = self.pieces[blue_pid]
        blue_piece.pos = None  # ensure off-board

        # Place
        if choice.place == "home":
            dst = HOME_APEX[side]

        elif choice.place == "sanctum":
            if choice.sanctum not in SANCTUMS:
                raise IllegalMove("Invalid Sanctum.")
            if self.piece_at(choice.sanctum) is not None:
                raise IllegalMove("Sanctum occupied.")
            dst = choice.sanctum
            ps.blue_life.banned_seed_sanctums.add(dst)

        elif choice.place == "apex":
            # Pay with a Green (runner if Green allowed)
            greens = self.pieces_of(side, PType.GREEN)
            if choice.pay_pid is not None:
                if choice.pay_pid not in greens:
                    raise IllegalMove("Selected green not available to sacrifice.")
                self.pieces[choice.pay_pid].pos = None
            else:
                # If runner is green and flag set, it can pay cost itself
                runner_is_green = self.pieces[runner_pid].kind == PType.GREEN
                if runner_is_green and choice.pay_runner_if_green:
                    # runner already removed below; cost satisfied
                    pass
                else:
                    # Sacrifice any other green if present
                    other = [g for g in greens if g != runner_pid]
                    if not other:
                        raise IllegalMove("No green available to sacrifice for Apex placement.")
                    self.pieces[other[0]].pos = None
            # Destination is enemy Home Apex
            enemy = "A" if side == "B" else "B"
            dst = HOME_APEX[enemy]
        else:
            raise IllegalMove("Invalid reforge placement option.")

        # Put Blue back
        if self.piece_at(dst) is not None:
            raise IllegalMove("Reforge destination occupied.")
        blue_piece.pos = dst
        # Refresh life
        ps.blue_life.reset_for_reforge()

    # ------------------------- Turn Engine -------------------------

    def begin_turn(self):
        """Advance per-turn timers and unroot Blue at start of its side's turn."""
        s = self.current
        self.turn_index_by_side[s] += 1

        # Unroot Blue at start of its own turn (if rooted)
        ps = self.players[s]
        if ps.blue_pid in self.pieces:
            if ps.blue_life.rooted:
                ps.blue_life.rooted = False

        # Cross exclusion countdown decrements at start of own turns
        if ps.blue_life.cross_exclusion_own_turns > 0:
            ps.blue_life.cross_exclusion_own_turns -= 1

        # Remember whether Blue was in Cross at start
        ps.blue_in_cross_at_turn_start = False
        bpos = self.pieces[ps.blue_pid].pos
        if bpos is not None and bpos in CENTRAL_FOUR:
            ps.blue_in_cross_at_turn_start = True

        # Opening double-move context
        if s == "B" and self.b_opening_double_pending:
            self._double_moves_done = 0
            self._double_first_pid = None

    def _finish_turn_and_switch(self):
        s = self.current
        ps = self.players[s]

        # Cross stay accounting: if Blue ends turn in Cross, increment; else if it was in Cross at start and left now, start exclusion
        bpos = self.pieces[ps.blue_pid].pos
        if bpos is not None and bpos in CENTRAL_FOUR:
            ps.blue_life.cross_stay_consec += 1
            if ps.blue_life.cross_stay_consec > 3:
                raise IllegalMove("Illegal: Blue would end a 4th consecutive own turn in the Central Four.")
        else:
            # Left Cross this turn?
            if ps.blue_in_cross_at_turn_start:
                ps.blue_life.cross_stay_consec = 0
                ps.blue_life.cross_exclusion_own_turns = 2

        # Reforge countdown ticking for defender (the side whose Blue was captured)
        for side in ("A", "B"):
            p = self.players[side]
            if p.reforge_countdown is not None:
                if side == s:
                    # it was their turn; after their turn, decrement
                    p.reforge_countdown -= 1
                    if p.reforge_countdown <= 0:
                        self.game_over = True
                        self.winner = "A" if side == "B" else "B"
                        raise GameOver(f"Reforge failed: {side} loses. Winner: {self.winner}")

        # Switch side or handle B's opening double
        if self.current == "B" and self.b_opening_double_pending:
            if self._double_moves_done < 2:
                # still in same "turn"
                return  # do not switch yet
            else:
                # finished double
                self.b_opening_double_pending = False

        # Switch
        self.current = "A" if self.current == "B" else "B"

    # ------------------------- Public API -------------------------

    def legal_moves_for(self, pid: int) -> List[Move]:
        """Enumerate slide (and slide→special for Blue) moves for this piece. Seeding is optional (choose with Move.seed_if_possible)."""
        p = self.pieces[pid]
        if p.pos is None or p.side != self.current:
            return []
        if p.kind == PType.BLUE and self.players[p.side].blue_life.rooted:
            return []  # rooted Blue cannot move
        # Opening double: cannot move same piece twice
        if self.current == "B" and self.b_opening_double_pending and self._double_first_pid is not None:
            if pid == self._double_first_pid:
                return []

        moves: List[Move] = []
        L = lanes_for(p.side)

        # Slide lengths
        if p.kind == PType.BLUE:
            # allow 0 (special-only)
            lengths = [0]
        else:
            lengths = []

        # Onward exact, Homeward up-to
        onward_exact = self._onward_exact(p.kind)
        home_max = self._home_max(p.kind)

        for lbl in ("OL", "OR"):
            ok, _, _ = self._path_is_legal_slide(pid, p.pos, lbl, onward_exact)
            if ok:
                moves.append(Move(pid=pid, dir_label=lbl, steps=onward_exact))

        for lbl in ("HL", "HR"):
            for k in range(1, home_max + 1):
                ok, _, _ = self._path_is_legal_slide(pid, p.pos, lbl, k)
                if ok:
                    moves.append(Move(pid=pid, dir_label=lbl, steps=k))

        if p.kind == PType.BLUE:
            # also generate "slide 0" (stay) → then special
            moves.append(Move(pid=pid, dir_label="HL", steps=0))  # label arbitrary when steps=0

            # add slide→special combos (we won't fold Seed here—caller can set seed_if_possible)
            blu = self.players[p.side].blue_life
            # cannot enter Cross if under exclusion
            def _would_land_in_cross(pos: Coord) -> bool:
                return pos in CENTRAL_FOUR

            gen: List[Move] = []
            for m in list(moves):  # slide primitives
                # Check Cross exclusion on landing
                if m.steps > 0:
                    v = self._vector_for(p.side, m.dir_label)
                    dst = p.pos
                    for _ in range(m.steps):
                        dst = add(dst, v)
                    if _would_land_in_cross(dst) and blu.cross_exclusion_own_turns > 0:
                        continue
                gen.append(m)

            moves = gen

            # specials
            if not blu.used_disp:
                for lbl in ("OL", "OR", "HL", "HR"):
                    ok, _, _ = self._blue_special_ok(pid, "disp", lbl)
                    if ok:
                        # We will attach 'disp' to each legal slide primitive (including 0)
                        for base in gen:
                            # no special→slide (we are slide→special only)
                            moves.append(Move(pid=pid, dir_label=base.dir_label, steps=base.steps,
                                              blue_special="disp", special_dir=lbl))

            if not blu.used_hop:
                for lbl in ("OL", "OR", "HL", "HR"):
                    ok, _, _ = self._blue_special_ok(pid, "hop", lbl)
                    if ok:
                        for base in gen:
                            moves.append(Move(pid=pid, dir_label=base.dir_label, steps=base.steps,
                                              blue_special="hop", special_dir=lbl))

        return moves

    def apply_move(self, move: Move, plant_choice: Optional[PlantChoice] = None):
        """Apply one move. Handles capture, Seed (if requested and legal), Cross timing, Crown Stagger, and Reforge planting/placement."""
        if self.game_over:
            raise GameOver("Game already finished.")

        s = self.current
        p = self.pieces.get(move.pid)
        if p is None or p.pos is None or p.side != s:
            raise IllegalMove("Piece not available or wrong side.")

        ps = self.players[s]

        # Opening double: enforce no same piece twice
        if s == "B" and self.b_opening_double_pending and self._double_first_pid is not None:
            if move.pid == self._double_first_pid:
                raise IllegalMove("Cannot move the same piece twice during B's opening double move.")

        # Pre-calc opponent for ZoC
        enemy = "A" if s == "B" else "B"

        # ----- Slide -----
        start = p.pos
        ok, dst, cap = self._path_is_legal_slide(move.pid, start, move.dir_label, move.steps)
        if not ok:
            raise IllegalMove("Illegal slide path.")
        # Cross exclusion pre-check for Blue landing
        if p.kind == PType.BLUE and dst in CENTRAL_FOUR and ps.blue_life.cross_exclusion_own_turns > 0:
            raise IllegalMove("Blue cannot enter Central Four during exclusion.")

        # Move to dst; handle capture by displacement (non-Blue or Blue slide capture)
        runner_planted = False
        captured_blue_side: Optional[Side] = None

        if cap is not None:
            # capture displaced piece
            cap_piece = self.pieces[cap]
            if cap_piece.kind == PType.BLUE:
                captured_blue_side = cap_piece.side
            cap_piece.pos = None

        # Apply slide
        p.pos = dst

        # Mobilization 'first departure' detection (for Seed delay)
        mobilization_block = False
        if p.kind == PType.BLUE:
            life = ps.blue_life
            if not life.left_home:
                # If the Blue started on Home apex and moved away this move, this is the first departure; block Seed
                if start == HOME_APEX[s] and p.pos != HOME_APEX[s]:
                    mobilization_block = True
                    life.left_home = True

        # ----- Blue special (optional) -----
        used_special_now = False
        special_kill_blue: Optional[Side] = None
        if p.kind == PType.BLUE and move.blue_special:
            if move.steps < 0:
                raise IllegalMove("Invalid slide length.")
            # Cannot special -> slide (we already slid; OK)
            # Validate specials usage
            life = ps.blue_life
            if move.blue_special == "disp" and life.used_disp:
                raise IllegalMove("Blue displacement already used this life.")
            if move.blue_special == "hop" and life.used_hop:
                raise IllegalMove("Blue hop already used this life.")

            ok2, dst2, cap2 = self._blue_special_ok(move.pid, move.blue_special, move.special_dir or "OL")
            if not ok2:
                raise IllegalMove("Illegal Blue special.")

            # Resolve special
            if cap2 is not None:
                cap_piece = self.pieces[cap2]
                if cap_piece.kind == PType.BLUE:
                    special_kill_blue = cap_piece.side
                cap_piece.pos = None
            p.pos = dst2

            used_special_now = True
            if move.blue_special == "disp":
                life.used_disp = True
            else:
                life.used_hop = True

            # Crown Stagger: if this was the second special this life, root at end of turn
            will_stagger = (life.specials_used_count() == 2)
        else:
            will_stagger = False

        # ----- Central Four illegal end check is done at turn end (4th stay) -----

        # ----- Seed (optional) -----
        if p.kind == PType.BLUE and move.seed_if_possible:
            # Ending square must be a Sanctum and opposite Sanctum empty
            if p.pos in SANCTUMS:
                opp = OPPOSITE_SANCTUM[p.pos]
                if self.piece_at(opp) is None:
                    # global cap check
                    if self.greens_total_on_board() >= GLOBAL_GREEN_CAP:
                        pass  # cannot seed
                    else:
                        # mobilization delay
                        if mobilization_block:
                            pass
                        elif p.pos in ps.blue_life.banned_seed_sanctums:
                            pass
                        else:
                            # Seed spawns a Green on opposite Sanctum
                            self._new_piece(s, PType.GREEN, opp)
                            # Root the Blue until next own turn
                            ps.blue_life.rooted = True

        # ----- Reforge capture handling -----
        # If a Blue was captured this move, start the defender's countdown = 5
        if captured_blue_side or special_kill_blue:
            victim = captured_blue_side or special_kill_blue
            defender = self.players[victim]
            defender.reforge_countdown = 5
            # Clear victim Blue off board
            self.pieces[defender.blue_pid].pos = None
            # Reset their life (fresh on reforge)
            defender.blue_life.reset_for_reforge()

        # ----- Reforge planting (if runner ended on enemy home apex) -----
        # Note: ZoC does not prevent planting.
        enemy_home = HOME_APEX[enemy]
        if p.pos == enemy_home:
            # Only relevant if current side was under countdown (they are planting to restore)
            pl = self.players[s]
            if pl.reforge_countdown is not None:
                # Remove runner from play
                runner_pid = p.pid
                self.pieces[runner_pid].pos = None
                # Apply placement choice
                if plant_choice is None:
                    raise IllegalMove("PlantChoice required when planting a banner.")
                self._apply_reforge_placement(s, plant_choice, runner_pid)
                pl.reforge_countdown = None  # success

        # ----- Crown Stagger rooting at end of turn -----
        if will_stagger:
            ps.blue_life.rooted = True

        # ----- Opening double-move accounting -----
        if s == "B" and self.b_opening_double_pending:
            self._double_moves_done += 1
            if self._double_moves_done == 1:
                self._double_first_pid = move.pid

        # ----- Finish turn or keep B's double -----
        self._finish_turn_and_switch()

    # --------- Convenience ---------

    def snapshot(self) -> Dict[str, object]:
        """Small dict snapshot for debugging/printing."""
        grid = [["." for _ in range(8)] for _ in range(8)]
        for p in self.pieces.values():
            if p.pos is None: continue
            x, y = p.pos
            mark = p.kind.value.lower() if p.side == "B" else p.kind.value
            grid[7 - y][x] = mark
        return {
            "to_move": self.current,
            "A_turn": self.turn_index_by_side["A"],
            "B_turn": self.turn_index_by_side["B"],
            "grid_rows_top_7_to_0": [" ".join(r) for r in grid],
            "A_blue": {
                "pos": self.pieces[self.players["A"].blue_pid].pos,
                "life": self.players["A"].blue_life.__dict__,
                "reforge": self.players["A"].reforge_countdown,
            },
            "B_blue": {
                "pos": self.pieces[self.players["B"].blue_pid].pos,
                "life": self.players["B"].blue_life.__dict__,
                "reforge": self.players["B"].reforge_countdown,
            },
        }
