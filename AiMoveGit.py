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
