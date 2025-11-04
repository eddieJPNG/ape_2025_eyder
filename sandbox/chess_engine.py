#!/usr/bin/env python3
"""
chess_engine.py
Um motor de xadrez simples porém completo: geração de movimentos legais (incluindo roque, en passant e promoção),
avaliação básica, busca minimax com alpha-beta e tabela de transposição. Interface CLI para jogar contra o motor.
Sem bibliotecas externas.

Uso:
    python chess_engine.py

Controles:
    - No prompt, insira uma jogada em notação simples do tipo e2e4, g1f3, e7e8q (promoção para dama com sufixo q/r/b/n).
    - 'undo' reverte uma jogada.
    - 'quit' sai.
"""

import time
import random
import sys
from collections import namedtuple

# ----------------------------
# Representação do Tabuleiro
# ----------------------------
# Usamos um array de 64 casas, índice 0 = a8, 7 = h8, 56 = a1, 63 = h1 (ranks 8->1, files a->h).
# Peças: 'P','N','B','R','Q','K' maiúsculas = brancas, minúsculas = pretas, '.' = vazio

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

Piece = str

def fen_to_board(fen):
    fields = fen.split()
    rows = fields[0].split('/')
    board = []
    for row in rows:
        for ch in row:
            if ch.isdigit():
                board.extend('.' * int(ch))
            else:
                board.append(ch)
    active_color = fields[1]
    castling = fields[2]
    enpassant = fields[3]
    halfmove = int(fields[4]) if len(fields) > 4 else 0
    fullmove = int(fields[5]) if len(fields) > 5 else 1
    return board, active_color, castling, enpassant, halfmove, fullmove

def board_to_fen(board, active_color, castling, enpassant, halfmove, fullmove):
    rows = []
    for r in range(8):
        row = ''
        empty = 0
        for f in range(8):
            c = board[r*8 + f]
            if c == '.':
                empty += 1
            else:
                if empty:
                    row += str(empty); empty = 0
                row += c
        if empty: row += str(empty)
        rows.append(row)
    pos = '/'.join(rows)
    return f"{pos} {active_color} {castling} {enpassant} {halfmove} {fullmove}"

def sq_to_coords(sq):
    # sq like "e4" -> index
    file = ord(sq[0]) - ord('a')
    rank = 8 - int(sq[1])
    return rank*8 + file

def idx_to_sq(i):
    rank = 8 - (i // 8)
    file = i % 8
    return f"{chr(ord('a')+file)}{rank}"

# ----------------------------
# Helpers de peças e cores
# ----------------------------
WHITE_PIECES = set("PNBRQK")
BLACK_PIECES = set("pnbrqk")

def is_white(p):
    return p in WHITE_PIECES

def is_black(p):
    return p in BLACK_PIECES

def color_of(p):
    if p == '.': return None
    return 'w' if p.isupper() else 'b'

# ----------------------------
# Movimento e Estado
# ----------------------------
Move = namedtuple('Move', 'from_sq to_sq piece captured promotion is_castle is_enpassant prev_castling prev_enpassant prev_halfmove')

class GameState:
    def __init__(self, fen=START_FEN):
        self.board, self.active_color, self.castling, self.enpassant, self.halfmove, self.fullmove = fen_to_board(fen)
        self.move_history = []
        # Transposition key: simple Zobrist-like pseudo using random seeds for each piece-square + side + castling/enpassant
        self.zobrist_table = None
        self.transposition = {}
        self.init_zobrist()

    def init_zobrist(self):
        random.seed(0xC0FFEE)  # deterministic pseudo-zobrist
        self.zobrist_table = {}
        pieces = list("PNBRQKpnbrqk")
        for p in pieces:
            for sq in range(64):
                self.zobrist_table[(p, sq)] = random.getrandbits(64)
        self.zobrist_table[('side', 0)] = random.getrandbits(64)
        # castling rights bits
        for c in ['K','Q','k','q']:
            self.zobrist_table[('cast', c)] = random.getrandbits(64)
        # enpassant file bits
        for f in range(8):
            self.zobrist_table[('ep', f)] = random.getrandbits(64)
        self.current_zobrist = self.compute_zobrist()

    def compute_zobrist(self):
        h = 0
        for sq, p in enumerate(self.board):
            if p != '.':
                h ^= self.zobrist_table[(p, sq)]
        if self.active_color == 'b':
            h ^= self.zobrist_table[('side', 0)]
        for c in self.castling:
            if c != '-':
                h ^= self.zobrist_table[('cast', c)]
        if self.enpassant != '-':
            file = ord(self.enpassant[0]) - ord('a')
            h ^= self.zobrist_table[('ep', file)]
        return h

    def push_move(self, move):
        # save state
        self.move_history.append(move)
        # update zobrist incrementally for speed
        # but for simplicity recalc after move
        self.board[move.to_sq] = move.promotion if move.promotion else move.piece
        self.board[move.from_sq] = '.'
        # handle captured removal (en passant)
        if move.is_enpassant:
            # captured pawn is behind to_sq depending on side
            if move.piece.isupper():
                cap_sq = move.to_sq + 8
            else:
                cap_sq = move.to_sq - 8
            self.board[cap_sq] = '.'
        # handle castling rook move
        if move.is_castle:
            # king side or queen side?
            if move.to_sq % 8 == 6:  # king side
                rook_from = move.to_sq + 1
                rook_to = move.to_sq - 1
            else:  # queen side
                rook_from = move.to_sq - 2
                rook_to = move.to_sq + 1
            self.board[rook_to] = self.board[rook_from]
            self.board[rook_from] = '.'

        # update castling rights and enpassant target, halfmove, fullmove
        self.castling = move.prev_castling if hasattr(move, 'prev_castling') else self.castling
        self.enpassant = '-'  # reset then set below if pawn double move
        if move.piece.upper() == 'P' and abs(move.to_sq - move.from_sq) == 16:
            # set enpassant
            ep_sq = (move.from_sq + move.to_sq) // 2
            self.enpassant = idx_to_sq(ep_sq)
        # update halfmove
        if move.piece.upper() == 'P' or move.captured != '.':
            self.halfmove = 0
        else:
            self.halfmove += 1
        if self.active_color == 'b':
            self.fullmove += 1
        # switch side
        self.active_color = 'b' if self.active_color == 'w' else 'w'
        # recompute zobrist
        self.current_zobrist = self.compute_zobrist()

    def pop_move(self):
        if not self.move_history:
            return
        move = self.move_history.pop()
        # reverse move
        self.active_color = 'b' if self.active_color == 'w' else 'w'
        if self.active_color == 'b':
            self.fullmove -= 1
        # move piece back
        self.board[move.from_sq] = move.piece
        # restore captured
        if move.is_enpassant:
            # restore captured pawn behind to_sq
            if move.piece.isupper():
                cap_sq = move.to_sq + 8
                self.board[cap_sq] = 'p'
            else:
                cap_sq = move.to_sq - 8
                self.board[cap_sq] = 'P'
            self.board[move.to_sq] = '.'
        else:
            self.board[move.to_sq] = move.captured
        # handle castling rook revert
        if move.is_castle:
            if move.to_sq % 8 == 6:
                rook_from = move.to_sq + 1
                rook_to = move.to_sq - 1
            else:
                rook_from = move.to_sq - 2
                rook_to = move.to_sq + 1
            self.board[rook_from] = self.board[rook_to]
            self.board[rook_to] = '.'
        # restore castling, enpassant, halfmove
        self.castling = move.prev_castling
        self.enpassant = move.prev_enpassant
        self.halfmove = move.prev_halfmove
        # recompute zobrist
        self.current_zobrist = self.compute_zobrist()

    def make_move_struct(self, from_sq, to_sq, promotion=None):
        piece = self.board[from_sq]
        captured = self.board[to_sq]
        is_enpassant = False
        is_castle = False
        # detect en passant capture
        if piece.upper() == 'P' and to_sq == (sq_to_coords(self.enpassant) if self.enpassant != '-' else -1):
            # direct index compare might not match; instead check move matches enpassant file and correct rank
            pass
        # Better detect enpassant: if pawn moves diagonally and captured square empty and enpassant target matches to_sq
        if piece.upper() == 'P' and captured == '.':
            from_file = from_sq % 8
            to_file = to_sq % 8
            if abs(from_file - to_file) == 1:
                # maybe enpassant
                if self.enpassant != '-':
                    ep_sq = sq_to_coords(self.enpassant)
                    if to_sq == ep_sq:
                        is_enpassant = True
                        # captured pawn is behind
                        if piece.isupper():
                            captured = 'p'
                        else:
                            captured = 'P'
        # detect castling
        if piece.upper() == 'K' and abs((from_sq % 8) - (to_sq % 8)) == 2:
            is_castle = True
        m = Move(from_sq=from_sq, to_sq=to_sq, piece=piece, captured=captured,
                 promotion=promotion, is_castle=is_castle, is_enpassant=is_enpassant,
                 prev_castling=self.castling, prev_enpassant=self.enpassant, prev_halfmove=self.halfmove)
        return m

    def print_board(self):
        print("  +-----------------+")
        for r in range(8):
            row = self.board[r*8:(r+1)*8]
            print(8-r, '|', ' '.join(row), '|')
        print("  +-----------------+")
        print("    a b c d e f g h")
        print(f"Side: {self.active_color}  Castling: {self.castling}  Enpassant: {self.enpassant}  Move: {self.fullmove}  Halfmove: {self.halfmove}")

# ----------------------------
# Geração de Movimentos
# ----------------------------
# Directions for sliding pieces and knights, etc.
KNIGHT_OFFSETS = [-17,-15,-10,-6,6,10,15,17]
KING_OFFSETS = [-9,-8,-7,-1,1,7,8,9]
# sliding directions as offsets for bishop/rook/queen
BISHOP_DIRS = [-9,-7,7,9]
ROOK_DIRS = [-8,-1,1,8]
QUEEN_DIRS = BISHOP_DIRS + ROOK_DIRS

def on_board(i):
    return 0 <= i < 64

def file_of(i):
    return i % 8

def rank_of(i):
    return i // 8

def same_file(i, j):
    return file_of(i) == file_of(j)

def generate_pseudo_legal_moves(state: GameState):
    """Gera movimentos pseudo-legais (não necessariamente deixando o rei em xeque)."""
    moves = []
    board = state.board
    me = state.active_color
    for i, p in enumerate(board):
        if p == '.': continue
        if (me == 'w' and p.islower()) or (me == 'b' and p.isupper()):
            continue
        if p.upper() == 'P':
            generate_pawn_moves(state, i, moves)
        elif p.upper() == 'N':
            generate_knight_moves(state, i, moves)
        elif p.upper() == 'B':
            generate_sliding_moves(state, i, BISHOP_DIRS, moves)
        elif p.upper() == 'R':
            generate_sliding_moves(state, i, ROOK_DIRS, moves)
        elif p.upper() == 'Q':
            generate_sliding_moves(state, i, QUEEN_DIRS, moves)
        elif p.upper() == 'K':
            generate_king_moves(state, i, moves)
    return moves

def generate_pawn_moves(state, i, moves):
    board = state.board
    p = board[i]
    dir_forward = -8 if p.isupper() else 8
    start_rank = 6 if p.isupper() else 1
    promote_rank = 0 if p.isupper() else 7
    to_sq = i + dir_forward
    # forward one
    if on_board(to_sq) and board[to_sq] == '.':
        if rank_of(to_sq) == promote_rank:
            for prom in ['Q','R','B','N']:
                promotion = prom if p.isupper() else prom.lower()
                moves.append(state.make_move_struct(i, to_sq, promotion=promotion))
        else:
            moves.append(state.make_move_struct(i, to_sq, promotion=None))
            # forward two
            if rank_of(i) == start_rank:
                to2 = i + 2*dir_forward
                if board[to2] == '.':
                    moves.append(state.make_move_struct(i, to2, promotion=None))
    # captures
    for df in (-1, 1):
        file = file_of(i) + df
        if 0 <= file < 8:
            cap_sq = i + dir_forward + df
            if on_board(cap_sq):
                target = board[cap_sq]
                if target != '.' and color_of(target) and color_of(target) != color_of(p):
                    if rank_of(cap_sq) == promote_rank:
                        for prom in ['Q','R','B','N']:
                            promotion = prom if p.isupper() else prom.lower()
                            moves.append(state.make_move_struct(i, cap_sq, promotion=promotion))
                    else:
                        moves.append(state.make_move_struct(i, cap_sq, promotion=None))
    # en passant
    if state.enpassant != '-':
        ep_idx = sq_to_coords(state.enpassant)
        # enpassant capture occurs when pawn moves diagonally to ep square
        for df in (-1, 1):
            if file_of(i) + df == file_of(ep_idx) and rank_of(ep_idx) == rank_of(i) + ( -1 if p.isupper() else 1 ):
                moves.append(state.make_move_struct(i, ep_idx, promotion=None))

def generate_knight_moves(state, i, moves):
    board = state.board
    p = board[i]
    for off in KNIGHT_OFFSETS:
        to = i + off
        if not on_board(to): continue
        # avoid wrap around
        if abs(file_of(i) - file_of(to)) > 2: continue
        target = board[to]
        if target == '.' or color_of(target) != color_of(p):
            moves.append(state.make_move_struct(i, to, promotion=None))

def generate_sliding_moves(state, i, dirs, moves):
    board = state.board
    p = board[i]
    for d in dirs:
        to = i + d
        while on_board(to) and abs(file_of(to) - file_of(to - d)) <= 1:
            target = board[to]
            if target == '.':
                moves.append(state.make_move_struct(i, to, promotion=None))
            else:
                if color_of(target) != color_of(p):
                    moves.append(state.make_move_struct(i, to, promotion=None))
                break
            to += d

def generate_king_moves(state, i, moves):
    board = state.board
    p = board[i]
    for off in KING_OFFSETS:
        to = i + off
        if not on_board(to): continue
        if abs(file_of(i) - file_of(to)) > 1: continue
        target = board[to]
        if target == '.' or color_of(target) != color_of(p):
            moves.append(state.make_move_struct(i, to, promotion=None))
    # castling rights
    if p.isupper() and state.active_color == 'w':
        if 'K' in state.castling:
            # white king side: e1->g1 indices: e1=60 g1=62
            if state.board[61] == '.' and state.board[62] == '.':
                # TODO: check squares not attacked
                moves.append(state.make_move_struct(i, i+2, promotion=None))
        if 'Q' in state.castling:
            if state.board[59] == '.' and state.board[58] == '.' and state.board[57] == '.':
                moves.append(state.make_move_struct(i, i-2, promotion=None))
    if p.islower() and state.active_color == 'b':
        if 'k' in state.castling:
            if state.board[5] == '.' and state.board[6] == '.':
                moves.append(state.make_move_struct(i, i+2, promotion=None))
        if 'q' in state.castling:
            if state.board[3] == '.' and state.board[2] == '.' and state.board[1] == '.':
                moves.append(state.make_move_struct(i, i-2, promotion=None))

# ----------------------------
# Legality: detectar xeque e filtrar movimentos ilegais
# ----------------------------
def is_square_attacked(state, sq, by_color):
    board = state.board
    # pawns
    if by_color == 'w':
        # white pawns attack from below (sq+7, sq+9)
        for off in (-9, -7):
            src = sq + off
            if on_board(src) and file_of(src) != file_of(sq):
                p = board[src]
                if p == 'P': return True
    else:
        for off in (9,7):
            src = sq + off
            if on_board(src) and file_of(src) != file_of(sq):
                p = board[src]
                if p == 'p': return True
    # knights
    for off in KNIGHT_OFFSETS:
        src = sq + off
        if on_board(src) and abs(file_of(src) - file_of(sq)) <= 2:
            p = board[src]
            if p != '.' and color_of(p) == by_color and p.upper() == 'N':
                return True
    # bishops/queens diagonals
    for d in BISHOP_DIRS:
        src = sq + d
        while on_board(src) and abs(file_of(src) - file_of(src - d)) <= 1:
            p = board[src]
            if p != '.':
                if color_of(p) == by_color and (p.upper() == 'B' or p.upper() == 'Q'):
                    return True
                break
            src += d
    # rooks/queens straights
    for d in ROOK_DIRS:
        src = sq + d
        while on_board(src) and abs(file_of(src) - file_of(src - d)) <= 1:
            p = board[src]
            if p != '.':
                if color_of(p) == by_color and (p.upper() == 'R' or p.upper() == 'Q'):
                    return True
                break
            src += d
    # king
    for off in KING_OFFSETS:
        src = sq + off
        if on_board(src) and abs(file_of(src) - file_of(sq)) <= 1:
            p = board[src]
            if p != '.' and color_of(p) == by_color and p.upper() == 'K':
                return True
    return False

def filter_legal_moves(state, moves):
    legal = []
    for m in moves:
        state.push_move(m)
        # find king square of the side that moved? Actually we need to check opponent's attack to our king after move
        # find own king:
        king = 'K' if state.active_color == 'b' else 'k'  # since we switched side after push
        king_sq = None
        for i, p in enumerate(state.board):
            if p == king:
                king_sq = i; break
        if king_sq is None:
            # illegal: king captured (shouldn't normally happen)
            ok = False
        else:
            # if king is attacked by opponent (which is current active_color), move illegal
            ok = not is_square_attacked(state, king_sq, state.active_color)
        state.pop_move()
        if ok:
            legal.append(m)
    return legal

# ----------------------------
# Avaliação
# ----------------------------
PIECE_VALUES = {'P':100, 'N':320, 'B':330, 'R':500, 'Q':900, 'K':20000,
                'p':-100, 'n':-320, 'b':-330, 'r':-500, 'q':-900, 'k':-20000}

# piece-square tables small heuristic (white perspective). We'll use symmetrical for black.
PST = {
    'P': [
         0,  0,  0,  0,  0,  0,  0,  0,
         5, 10, 10,-20,-20, 10, 10,  5,
         5, -5,-10,  0,  0,-10, -5,  5,
         0,  0,  0, 20, 20,  0,  0,  0,
         5,  5, 10, 25, 25, 10,  5,  5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
         0,  0,  0,  0,  0,  0,  0,  0
    ],
    'N': [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ],
    'B': [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ],
    'R': [
         0,  0,  0,  5,  5,  0,  0,  0,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
         5, 10, 10, 10, 10, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0
    ],
    'Q': [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
         -5,  0,  5,  5,  5,  5,  0, -5,
          0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ],
    'K': [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
         20, 20,  0,  0,  0,  0, 20, 20,
         20, 30, 10,  0,  0, 10, 30, 20
    ]
}

def pst_value(piece, sq):
    if piece == '.': return 0
    key = piece.upper()
    tbl = PST.get(key)
    if tbl is None: return 0
    # for white, table index = sq; for black, mirror vertically
    if piece.isupper():
        return tbl[sq]
    else:
        return -tbl[63 - sq]

def evaluate(state: GameState):
    score = 0
    for i, p in enumerate(state.board):
        if p == '.': continue
        score += PIECE_VALUES.get(p, 0)
        score += pst_value(p, i)
    # perspective: positive -> white advantage; we will return score for side to move as perspective
    return score

# ----------------------------
# Search: Minimax + Alpha-Beta + Iterative Deepening + TT
# ----------------------------
INF = 10**9

class Searcher:
    def __init__(self):
        self.nodes = 0
        self.start_time = 0
        self.time_limit = None
        self.best_line = []
        self.tt = {}  # zobrist -> (depth, score, flag, best_move)
        # flags: 'EXACT', 'LOWER', 'UPPER'

    def time_exceeded(self):
        if self.time_limit is None: return False
        return (time.time() - self.start_time) >= self.time_limit

    def order_moves(self, state, moves):
        # simple move ordering: captures first (by value), promotions, else random
        scored = []
        for m in moves:
            score = 0
            if m.captured != '.':
                score += abs(PIECE_VALUES.get(m.captured, 0)) - abs(PIECE_VALUES.get(m.piece, 0))
            if m.promotion:
                score += 900
            # prefer center moves lightly
            file = file_of(m.to_sq)
            rank = rank_of(m.to_sq)
            center_dist = abs(file-3.5)+abs(rank-3.5)
            score -= center_dist
            scored.append((score, m))
        scored.sort(key=lambda x: -x[0])
        return [m for _, m in scored]

    def search(self, state: GameState, max_depth=4, time_limit=2.0):
        self.start_time = time.time()
        self.time_limit = time_limit
        best_move = None
        best_score = -INF
        for depth in range(1, max_depth+1):
            self.nodes = 0
            score, move = self.alphabeta_root(state, depth)
            if not self.time_exceeded():
                best_move, best_score = move, score
                self.best_line = [move]
                # optional: could store PV via TT
            else:
                break
        return best_move, best_score

    def alphabeta_root(self, state, depth):
        alpha = -INF
        beta = INF
        best_move = None
        moves = generate_pseudo_legal_moves(state)
        moves = filter_legal_moves(state, moves)
        moves = self.order_moves(state, moves)
        for m in moves:
            state.push_move(m)
            val = -self.alphabeta(state, depth-1, -beta, -alpha)
            state.pop_move()
            if self.time_exceeded():
                break
            if val > alpha:
                alpha = val
                best_move = m
        return alpha, best_move

    # def alphabeta(self, state, depth, alpha, beta):
    #     self.nodes += 1
    #     if self.time_exceeded():
    #         return 0
    #     # check repetition? omitted for simplicity
    #     # transposition lookup
    #     zob = state.current_zobrist
    #     if zob in self.tt:
    #         entry = self.tt[zob]
    #         e_depth, e_score, e_flag, e_move = entry
    #         if e_depth >= depth:
    #             if e_flag == 'EXACT':
    #                 return e_score
    #             elif e_flag == 'LOWER' and e_score > alpha:
    #                 alpha = e_score
    #             elif e_flag == 'UPPER' and e_score < beta:
    #                 beta = e_score
    #             if alpha >= beta:
    #                 return e_score
    #     if depth == 0:
    #         return quiescence(self, state, alpha, beta)
    #     moves = generate_pseudo_legal_moves(state)
    #     moves = filter_legal_moves(state, moves)
    #     if not moves:
    #         # checkmate or stalemate
    #         # find our king
    #         king = 'K' if state.active_color == 'w' else 'k'
    #         king_sq = None
    #         for i,p in enumerate(state.board):
    #             if p == king:
    #                 king_sq = i; break
    #         if king_sq is None or is_square_attacked(state, king_sq, 'b' if state.active_color=='w' else 'w'):
    #             return -INF + (100 - depth)  # checkmate: bad
    #         else:
    #             return 0  # stalemate
    #     moves = self.order_moves(state, moves)
    #     best_score = -INF
    #     best_move = None
    #     for m in moves:
    #         state.push_move(m)
    #         score = -self.alphabeta(state, depth-1, -beta, -alpha)
    #         state.pop_move()
    #         if self.time_exceeded():
    #             return 0
    #         if score > best_score:
    #             best_score = score
    #             best_move = m
    #         if score > alpha:
    #             alpha = score
    #         if alpha >= beta:
    #             break
    #     # store in TT
    #     flag = 'EXACT'
    #     if best_score <= alpha_orig := alpha:
    #         flag = 'UPPER'
    #     if best_score >= beta:
    #         flag = 'LOWER'
    #     self.tt[zob] = (depth, best_score, flag, best_move)
    #     return best_score

    def alphabeta(self, state, depth, alpha, beta):
    self.nodes += 1
    if self.time_exceeded():
        return 0
    # check repetition? omitted for simplicity
    # transposition lookup
    zob = state.current_zobrist
    if zob in self.tt:
        entry = self.tt[zob]
        e_depth, e_score, e_flag, e_move = entry
        if e_depth >= depth:
            if e_flag == 'EXACT':
                return e_score
            elif e_flag == 'LOWER' and e_score > alpha:
                alpha = e_score
            elif e_flag == 'UPPER' and e_score < beta:
                beta = e_score
            if alpha >= beta:
                return e_score
    if depth == 0:
        return quiescence(self, state, alpha, beta)
    moves = generate_pseudo_legal_moves(state)
    moves = filter_legal_moves(state, moves)
    if not moves:
        # checkmate or stalemate
        # find our king
        king = 'K' if state.active_color == 'w' else 'k'
        king_sq = None
        for i,p in enumerate(state.board):
            if p == king:
                king_sq = i; break
        if king_sq is None or is_square_attacked(state, king_sq, 'b' if state.active_color=='w' else 'w'):
            return -INF + (100 - depth)  # checkmate: bad
        else:
            return 0  # stalemate
    moves = self.order_moves(state, moves)
    best_score = -INF
    best_move = None
    alpha_orig = alpha  # Adicionada esta linha para definir alpha_orig
    for m in moves:
        state.push_move(m)
        score = -self.alphabeta(state, depth-1, -beta, -alpha)
        state.pop_move()
        if self.time_exceeded():
            return 0
        if score > best_score:
            best_score = score
            best_move = m
        if score > alpha:
            alpha = score
        if alpha >= beta:
            break
    # store in TT
    flag = 'EXACT'
    if best_score <= alpha_orig:  # Agora alpha_orig está definido
        flag = 'UPPER'
    if best_score >= beta:
        flag = 'LOWER'
    self.tt[zob] = (depth, best_score, flag, best_move)
    return best_score

def quiescence(searcher: Searcher, state: GameState, alpha, beta):
    stand_pat = evaluate(state)
    if stand_pat >= beta:
        return beta
    if stand_pat > alpha:
        alpha = stand_pat
    # generate captures only
    moves = generate_pseudo_legal_moves(state)
    moves = [m for m in moves if m.captured != '.']
    moves = filter_legal_moves(state, moves)
    moves.sort(key=lambda m: abs(PIECE_VALUES.get(m.captured, 0)) - abs(PIECE_VALUES.get(m.piece, 0)), reverse=True)
    for m in moves:
        state.push_move(m)
        score = -quiescence(searcher, state, -beta, -alpha)
        state.pop_move()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha

# ----------------------------
# CLI e Notação
# ----------------------------
def parse_move_input(s, state):
    s = s.strip()
    if len(s) < 4:
        return None
    from_sq = sq_to_coords(s[0:2])
    to_sq = sq_to_coords(s[2:4])
    promotion = None
    if len(s) >= 5:
        ch = s[4].lower()
        if ch in 'qrbn':
            promotion = ch.upper() if state.active_color == 'w' else ch
    # validate move among legal moves
    candidates = generate_pseudo_legal_moves(state)
    candidates = filter_legal_moves(state, candidates)
    for m in candidates:
        if m.from_sq == from_sq and m.to_sq == to_sq:
            # promotion acceptance
            if m.promotion:
                if promotion:
                    # match promotion piece
                    if m.promotion.lower() == promotion.lower():
                        return m
                    else:
                        continue
                else:
                    # if move requires promotion but user didn't supply, default to queen
                    default_prom = 'Q' if state.active_color == 'w' else 'q'
                    return state.make_move_struct(from_sq, to_sq, promotion=default_prom)
            else:
                return m
    return None

# ----------------------------
# Main Play Loop
# ----------------------------
def human_vs_engine():
    state = GameState()
    searcher = Searcher()
    while True:
        state.print_board()
        if state.active_color == 'w':
            prompt = "White move (e2e4): "
        else:
            prompt = "Black move (e7e5): "
        user = input(prompt).strip()
        if user == 'quit':
            break
        if user == 'undo':
            state.pop_move()
            continue
        if user == 'engine':
            # engine plays for side to move
            print("Engine thinking...")
            m, score = searcher.search(state, max_depth=3, time_limit=1.0)
            if m is None:
                print("No move found.")
                continue
            print("Engine plays:", idx_to_sq(m.from_sq) + idx_to_sq(m.to_sq))
            state.push_move(m)
            continue
        if user == 'flip':
            # debug: flip colors
            state.active_color = 'b' if state.active_color == 'w' else 'w'
            continue
        # try parse as move
        move = parse_move_input(user, state)
        if move:
            state.push_move(move)
            # auto engine reply?
            # continue loop
        else:
            print("Jogada inválida. Use notação 'e2e4' ou 'g1f3'. Comando 'undo', 'engine', 'quit'.")

def engine_vs_engine(depth=3, time_per_move=1.0, moves=50):
    state = GameState()
    s1 = Searcher()
    s2 = Searcher()
    for ply in range(moves):
        state.print_board()
        print(f"Move {ply+1}, side {state.active_color}")
        searcher = s1 if state.active_color == 'w' else s2
        m, score = searcher.search(state, max_depth=depth, time_limit=time_per_move)
        if m is None:
            print("No move found, game over.")
            break
        print("Engine plays:", idx_to_sq(m.from_sq) + idx_to_sq(m.to_sq), "score", score)
        state.push_move(m)
        # small pause
        time.sleep(0.1)
    state.print_board()

def main():
    print("Python Chess Engine (CLI)")
    print("Commands: 'play' (human vs engine), 'engine' (engine vs engine), 'quit'")
    while True:
        cmd = input(">")
        if cmd.strip() == 'quit':
            break
        elif cmd.strip() == 'play':
            human_vs_engine()
        elif cmd.strip() == 'engine':
            engine_vs_engine()
        else:
            print("Comando inválido. Use 'play', 'engine', ou 'quit'.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaindo.")
