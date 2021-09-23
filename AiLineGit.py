class Line(object):

    def __init__(self, moves):

        self.moves = moves
        self.score = None

    def first_move(self):
        return self.moves[0]

    def last_chessmove(self):
        return self.moves[-1].move