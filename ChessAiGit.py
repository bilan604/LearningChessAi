class Line(object):

    def __init__(self, moves):

        self.moves = moves
        self.score = None

    def first_move(self):
        return self.moves[0]

    def last_chessmove(self):
        return self.moves[-1].move

class AiMove(object):
    """
    Takes a chess.Move()
    """
    @staticmethod
    def piece(board, tile):
        # takes a from_square?
        """Returns a Piece! Printing gives a letter, """
        return board.piece_at(tile)

    @staticmethod
    def piece_int(board, piece):
        # try to avoid?
        if board.piece_at(piece):
            return board.piece_at(piece).piece_type
        else:
            return None

    @staticmethod
    def pieces(board, color):
        # returns a SquareSet
        pieces = []
        for i in range(1, 7):
            lst = list(board.pieces(i, color))
            for item in lst:
                pieces.append(item)
        return pieces

    @staticmethod
    def attackers(board, color, tile):
        attackers = []
        if board.attackers(not color, tile):
            for t in board.attackers(not color, tile):
                attackers.append(board.piece_at(t).piece_type)
        return attackers


    @staticmethod
    def defenders(board, color, tile):
        defenders = []
        if board.attackers(color, tile):
            for t in board.attackers(color, tile):
                defenders.append(board.piece_at(t).piece_type)
        return defenders


    @staticmethod
    def old_control(board, chess_move):
        ##
        """ To square: how much tiles it the piece now attacking after a move"""
        attacking_tiles = board.attacks(chess_move.from_square)
        control_tiles = []
        for tile in attacking_tiles:
            if not board.piece_at(tile):
                control_tiles.append(tile)
        return control_tiles

    @staticmethod
    def new_control(board, chess_move):
        ##
        """ To square: how much tiles is the piece now attacking after a move"""
        board.push(chess_move)
        attacking_tiles = board.attacks(chess_move.to_square)
        control_tiles = []
        for tile in attacking_tiles:
            if not board.piece_at(tile):
                control_tiles.append(tile)
        board.pop()
        return control_tiles

    @staticmethod
    def kills(board, chess_move, color):
        if board.piece_at(chess_move.to_square) and board.piece_at(chess_move.to_square).color != color:
            return board.piece_at(chess_move.to_square).piece_type
        else:
            return None

    @staticmethod
    def check(board, chess_move):
        verdict = False
        board.push(chess_move)
        if board.is_checkmate():
            verdict = True
        board.pop()
        return verdict

    @staticmethod
    def checkmate(board, chess_move):
        verdict = False
        board.push(chess_move)
        if board.is_checkmate():
            verdict = True
        board.pop()
        return verdict

    @staticmethod
    def promotion(chess_move):
        if chess_move.promotion:
            return True
        return False

    @staticmethod
    def global_threat_changes(board, aimove):
        """
        Returns a list  two dicts of Piece(): [] or a list of attacker pieces
        """
        old_threats = {}
        pieces = AiMove.pieces(board, aimove.color)
        for tile in pieces:
            # p is a tile
            piece = AiMove.piece(board, tile) # not letter
            attackers = AiMove.attackers(board, aimove.color, tile)
            old_threats[piece] = attackers
        board.push(aimove.chess_move)
        npieces = AiMove.pieces(board, aimove.color)
        new_threats = {}
        for ntile in npieces:
            npiece = AiMove.piece(board, ntile)
            nattackers = AiMove.attackers(board, aimove.color, ntile)
            old_threats[npiece] = nattackers
        board.pop()
        return [old_threats, new_threats]

    @staticmethod
    def setUpAiMove(board, chess_move, move):
        """
        Takes a chess.Move and returns a AI.Move
        """
        move.piece = AiMove.piece(board, chess_move.from_square)
        move.old_defenders = AiMove.defenders(board, board.turn, chess_move.from_square)
        move.old_attackers = AiMove.attackers(board, board.turn, chess_move.from_square)
        move.new_defenders = AiMove.defenders(board, board.turn, chess_move.from_square)
        move.new_attackers = AiMove.attackers(board, board.turn, chess_move.from_square)
        move.old_control = AiMove.old_control(board, chess_move)
        move.new_control = AiMove.new_control(board, chess_move)
        move.kills = AiMove.kills(board, chess_move, board.turn)
        move.check = AiMove.check(board, chess_move)
        move.checkmate = AiMove.checkmate(board, chess_move)
        move.promotion = AiMove.promotion(chess_move)
        move.repeat = (chess_move in board.move_stack[-5:])
        move.pieces = AiMove.pieces(board, board.turn)
        move.threat_changes = AiMove.global_threat_changes(board, move)
        return move

    class Move(object):

        def __init__(self, color, chess_move):
            self.chess_move = chess_move
            self.color = color
            self.piece = None
            self.old_defenders = None
            self.old_attackers = None
            self.new_defenders = None
            self.new_attackers = None
            self.old_control = []
            self.new_control = []
            self.control = []
            self.kills = None
            self.check = False
            self.checkmate = False
            self.promotion = False
            self.repeat = False
            self.threat_changes = [{}, {}]

        def get_attributes(self):
            d_ = {"new_defenders": self.new_defenders, "new_attackers": self.new_attackers,
                    "old_defenders": self.old_defenders, "old_attackers": self.old_attackers,
                    "old_control": self.old_control, "new_control": self.new_control,
                    "kills": self.kills, "check": self.check, "checkmate": self.checkmate,
                  "promotion": self.promotion, "threat_changes": self.threat_changes}
            return d_

import random
import re
import sys
import _start as chess
from AiLineDesk import Line as Line
from AiMoveDesk import AiMove as AiMove


def get_player(board, active_ai):
    if board.turn:
        player = active_ai.SmartAi(board, "white", "smart", active_ai)
    else:
        player = active_ai.SmartAi(board, "black", "smart", active_ai)
    return player


def get_legal_moves(board):
    moves = []
    for move in board.legal_moves:
        moves.append(move)
    return moves


def move_gives_checkmate(board, move):
    verdict = False
    board.push(move)
    if board.is_checkmate():
        verdict = True
        board.pop()
        return verdict
    else:
        board.pop()
        return verdict


def move_stops_game(board, move):
    verdict = False
    board.push(move)
    legal_moves = get_legal_moves(board)
    if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material() or board.is_game_over():
        verdict = True
        board.pop()
        return verdict
    elif not legal_moves:
        verdict = True
        board.pop()
        print("the move:", move, "stops game")
        return verdict
    else:
        board.pop()
        return verdict


def check_move_ok(board, moves):
    board = board.copy()
    for move in moves:
        board.push(move)
        if board.is_game_over():
            print(move, "breaks the game \n", board, "turn:", board.turn)
            return False
        else:
            board.pop()
    return True

def _list_lm(board):
    """
    Takes a Board.legal_moves generator
    :returns a list of string legal moves
    """
    legal_moves = str(board.legal_moves)
    lm = re.sub(" ", "", legal_moves)
    list_of_moves = (str(lm).split("(")[1][0:-2]).split(",")


def get_legal_moves(board):
    moves = []
    for move in board.legal_moves:
        moves.append(move)
    return moves


def get_legal_chessmoves(board):
    moves = []
    for move in board.legal_moves:
        moves.append(move)
    return moves


def get_pieces(board, color):
        # returns a SquareSet
    pieces = []
    for i in range(1, 7):
        lst = list(board.pieces(i, color))
        for item in lst:
            pieces.append(item)
    return pieces


class ChessGameResets(object):

    def __init__(self, board, ai1, ai2):
        self.ais = {True: ai1, False: ai2} # white, black
        self.round = 0
        self.board = board

    def play_elim(self) -> None:
        while not self.board.is_game_over():
            active_ai = self.ais[self.board.turn]
            active_player = get_player(self.board, active_ai)
            move = active_player.play()
            self.board.push(move)
            print(self.board)
            print(active_player.name, "plays", move)
            self.round += 1
            if self.board.is_checkmate():
                print(active_player.name, " won the game at round ", self.round, " via checkmate!", sep="")
                return self.ais[self.board.turn]
            elif self.board.is_game_over():
                print(active_player.name, "on round", self.round, "did not checkmate but the game is over!")
                return self.ais[not self.board.turn]
            elif self.round > 60:
                return self.ais[not self.board.turn]


class ChessAi(object):
    """
    The chess AI:
    """
    MaxDepth = 16
    IsWhite = {"white": True, "black": False}
    IsSmart = {"smart": True, "dumb": False, "human": False}
    piece_values = {1: 10.0, 2: 30.0, 3: 35.0, 4: 50.0, 5: 90.0, 6: 2.0}
    # InverseConstant = 100
    # OldDefConstant = -0.6
    # NewDefConstant = 0.6
    # OldAtkConstant = 1
    # NewAtkConstant = -0.8
    # KillConstant = 2.2
    # CMConstant = 120
    PromotionConstant = 1000
    piece_to_int = {"p": 1, "n": 2, "b": 3, "r": 4, "q": 5, "k": 6}
    piece_values_str = {"p": 10.0, "n": 30.0, "b": 35.0, "r": 50.0, "q": 90.0, "k": 2.0}

    def __init__(self, inv, oldD, newD, oldA, newA, kill, CM, CC, PC, TCC):
        self.InverseConstant = inv
        self.OldDefConstant = oldD
        self.NewDefConstant = newD
        self.OldAtkConstant = oldA
        self.NewAtkConstant = newA
        self.KillConstant = kill
        self.CMConstant = CM
        self.ControlConstant = CC
        self.PromotionConstant = PC
        self.ThreatChangesConstant = TCC

    class AssessScorer(object):
        """
        No CM
        """
        def __init__(self, aimove, ai):
            self.aimove = aimove
            self.ai = ai

        def scoring_system(self, attributes, info):
            """ Takes a list of string attributes """
            score = 0
            #for item in attributes:
            #    score += ChessAi.Offense[info[attr]] * ChessAi.AttributeContants[item] * info[item]

            return score

        def score(self):

            score = 0.0
            attr = self.aimove.get_attributes()
            ChessAi = self.ai
            IC = ChessAi.InverseConstant
            if attr["old_defenders"]:
                for defender in attr["old_defenders"]:
                    if defender != 6:
                        score += (IC/ChessAi.piece_values[defender]) * ChessAi.OldDefConstant * (ChessAi.piece_values[self.aimove.piece.piece_type])
                    else:
                        score += (40*ChessAi.piece_values[defender]) * (ChessAi.piece_values[self.aimove.piece.piece_type])

            if attr["new_defenders"]:
                for defender in attr["new_defenders"]:
                    if defender != 6:
                        score += (IC/ChessAi.piece_values[defender]) * ChessAi.NewDefConstant * (ChessAi.piece_values[self.aimove.piece.piece_type])
                    else:
                        score += (40*ChessAi.piece_values[defender]) * (ChessAi.piece_values[self.aimove.piece.piece_type])

            if attr["old_attackers"]:
                for attacker in attr["old_attackers"]:
                    score += (IC/ChessAi.piece_values[attacker]) * ChessAi.OldAtkConstant * ChessAi.piece_values[self.aimove.piece.piece_type]

            if attr["new_attackers"]:
                for attacker in attr["new_attackers"]:
                    score -= (IC/ChessAi.piece_values[attacker]) * ChessAi.NewAtkConstant * ChessAi.piece_values[self.aimove.piece.piece_type]

            if attr["kills"]:  # does not support king atm
                score += ChessAi.piece_values[attr["kills"]] * ChessAi.KillConstant

            if attr["check"]:
                score += (IC/ChessAi.piece_values[self.aimove.piece.piece_type])

            if self.aimove.piece.piece_type == 6:
                score -= 8000

            control_change = len(attr["new_control"]) - len(attr["old_control"])
            score += ChessAi.ControlConstant * control_change * (IC/ChessAi.piece_values[self.aimove.piece.piece_type])

            if attr["checkmate"]:
                score += ChessAi.CMConstant * (IC/ChessAi.piece_values[self.aimove.piece.piece_type]) * ChessAi.piece_values[6]

            if self.aimove.repeat:
                score -= 5000

            if attr["promotion"]:
                score += ChessAi.PromotionConstant

            if attr["threat_changes"]:
                temp_score = 0
                for piece0 in attr["threat_changes"][0]:
                    for attacker in attr["threat_changes"][0][piece0]:  # for that piece's attackers
                        temp_score += (IC / ChessAi.piece_values[attacker]) * ChessAi.NewAtkConstant * ChessAi.piece_values[piece0.piece_type]
                for piece1 in attr["threat_changes"][1]:
                    for attacker in attr["threat_changes"][0][piece1]:  # for that piece's attackers
                        temp_score -= (IC / ChessAi.piece_values[attacker]) * ChessAi.ThreatChangesConstant * ChessAi.piece_values[piece1.piece_type]
                #print("temp gtc score:", temp_score)
                score += temp_score


            ## Stablizer
            score = int(score) // 100


            self.aimove.score = score
            return self.aimove.score

        def get_score(self):
            return self.score()

    class RecuAssess(object):

        def __init__(self, board, ChessAi):
            self.board = board.copy()
            self.color = board.turn
            self.depth = 1
            self.base_depth = 1
            self.cm_lines = []
            self.special_lines = []
            self.ChessAi = ChessAi

        def make_aimove(self, chess_move):
            ai_move = AiMove.Move(self.color, chess_move)
            move = AiMove.Move(board.turn, chess_move)
            return AiMove.setUpAiMove(self.board, chess_move, move)

        def score_aimove(self, aimove):
            """ beta, in compare_moves """
            scorer = self.ChessAi.AssessScorer(aimove, self.ChessAi)
            score = scorer.get_score()
            return score

        def score_line(self, line):
            """ keep """
            #adscore, enemyadscore = 0, 0
            score, enemy_score = 0, 0
            cboard = self.board.copy()
            for i in range(len(line.moves)):
                aimove = AiMove.Move(cboard.turn , line.moves[i])
                AiMove.setUpAiMove(cboard, aimove.chess_move,aimove)
                cboard.push(line.moves[i])


                if aimove.color == self.color:
                    score += self.score_aimove(aimove)
                    #adscore += self.score_aimove(aimove)
                else:
                    enemy_score += self.score_aimove(aimove)
                    #enemyadscore += self.score_aimove(aimove)
            line.score = (score - (0.8 * enemy_score))
            return line.score

        def pick_line(self, lines):
            """ per move """
            top_score = -100000
            top_line = 0
            for line in lines:
                if type(line) == int:
                    pass
                else:
                    line.score = self.score_line(line)
                    if line.score > top_score:
                        top_score, top_line = line.score, line
            return top_line

        def prune_lines(self, lines):
            print("pruning")
            new_lines = []
            scores = []
            for line in lines:
                scores.append(self.score_line(line))

            for line in lines:
                if line.score > 1:
                    new_lines.append(line)
            return new_lines

        def add_depth_line(self, line):
            """
            Takes a line and returns lines
            ! needs move pruning
            """
            cboard = self.board.copy()
            for move in line.moves:
                cboard.push(move)
            new_legal_moves = get_legal_chessmoves(cboard)  # copy() ?
            if new_legal_moves:
                new_lines_set = []
                for move in new_legal_moves:
                    new_moves = line.moves.copy() + [move]
                    new_lines_set.append(Line(new_moves))  # the line
                return new_lines_set
            else:
                #print("No legal moves for player TURN:", board.turn)
                ## unused
                if cboard.is_checkmate():
                    self.cm_lines.append(line)
                return [line]

        def recu_explore_lines(self, lines):
            self.depth += 1
            if self.depth < ChessAi.MaxDepth:
                new_lines_cache = []
                for line in lines:
                    new_lines = self.add_depth_line(line)
                    if new_lines:
                        for line in new_lines:
                            new_lines_cache.append(line)
                    return self.recu_explore_lines(new_lines_cache)
            else:
                self.depth = self.base_depth
                #print(len(lines))
                return lines

        def compare_moves(self, chess_moves):
            top_line_set = []
            for move in chess_moves:
                line = Line([move])
                lines = self.recu_explore_lines([line])
                top_line = self.pick_line(lines)
                top_line_set.append(top_line)
            #for line in top_line_set:
                #print("line:", line.moves, "\n", line.score)
            best_line = self.pick_line(top_line_set)

            return best_line.first_move()

        def choose_move(self):
            legal_chessmoves = get_legal_chessmoves(self.board)
            best_move = self.compare_moves(legal_chessmoves)
            if self.cm_lines:
                #("CM lines:", self.cm_lines)
                for line in self.cm_lines:
                    if self.score_line(line) > 10000:
                        return line.moves[0]
            return best_move

    class SmartAi(object):

        def __init__(self, board, color, smart, ai):
            self.color = ChessAi.IsWhite[color]
            self.human = (smart == "human")
            self.smart = ChessAi.IsSmart[smart]
            self.board = board
            self.name = color
            self.ai = ai

        def playSmart(self):
            #print("It is ", self.name, "'s turn: ", sep="")
            engine = ChessAi.RecuAssess(self.board, self.ai)
            chosen_move = engine.choose_move()
            return chosen_move

        def playDumb(self):
            #print("It is ", self.name, "'s turn: ", sep="")
            legal_chessmoves = get_legal_moves(self.board)
            chosen_move = legal_chessmoves[random.randint(0, len(legal_chessmoves)-1)]
            return chosen_move

        def play(self):
            if self.human:
                moves = get_legal_moves(self.board)
                strmoves = []
                strmoves_display = {}
                for move in moves:
                    strmoves.append(move.uci())
                for i in range(len(strmoves)):
                    strmoves_display[i] = strmoves[i]
                print("These are your legal moves:\n", strmoves_display)
                print(moves[4], moves[4])
                valid = False
                while not valid:
                    ans = re.sub(" ","", input("What move?: "))
                    if ans in strmoves:
                        valid = True
                for i in range(strmoves):
                    if strmoves[i] == ans:
                        return moves[i]

            elif self.smart:
                move = self.playSmart()
                #print(self.name, "plays", move, "[smart]")
                #print(self.board.move_stack)
                return move

            else:
                move = self.playDumb()
                #print(self.name, "plays", move, "[dumb]")
                return move


class Ai_pvp(object):

    def __init__(self, ini_constants):
        self.ai_dict = {}
        self.constants = ini_constants

    def constant_to_ai(self, N):
        return ChessAi(N[0], N[1], N[2], N[3], N[4], N[5], N[6], N[7], N[8], N[9])

    def generate_new_ai(self,constants, lasso):
        N = []
        for i in range(len(constants)):
            multiplier = 0  # percent
            for j in range(10):
                multiplier += random.randrange(-8, 14)
            multiplier /= (0.5 * lasso)
            change = (constants[i]*multiplier)/100
            N.append(constants[i] + change)  # int???
        return N

    def make_ais(self, constants, lasso):
        self.ai_dict = {}
        brackets = []
        for i in range(1, 3):
            bracket = []
            for i in range(1, 3):
                new_c = self.generate_new_ai(constants, lasso)
                new_ai = self.constant_to_ai(new_c)
                bracket.append(new_ai)
                self.ai_dict[new_ai] = new_c
            brackets.append(bracket)
        return brackets

    def pvp(self, bracket):
        board = chess.Board()
        board.reset()
        ai1 = bracket[0]
        ai2 = bracket[1]
        game = ChessGameResets(board, ai1, ai2)
        winner = game.play_elim()
        print("AI with", self.ai_dict[winner], "\n was a bracket winner!!!")
        return winner

    def pvp_arena(self):
        constants = self.constants.copy()
        for lasso in range(10, 17):
            ais = self.make_ais(constants, lasso)
            b1winner = self.pvp(ais[0])
            b2winner = self.pvp(ais[1])
            winner = self.pvp([b1winner, b2winner])
            constants = self.ai_dict[winner]
            print(lasso, "bracket ended")


sys.setrecursionlimit(10000)
board = chess.Board()
ini_c = [467.584, -0.68304, 0.98006727, 0.892354, -1.3343, 2.6132, 135.0864, 23.13309090, 4215.650, 10.94]

trainer = Ai_pvp(ini_c)
trainer.pvp_arena()
