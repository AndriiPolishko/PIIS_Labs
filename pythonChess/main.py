"""
naming description:
    whoToMove - integer value that can be 1 (representing white) or -1 (representing black)
"""
import chess
import random

class NegaAgent:
    board = None

    def __init__(self, board: chess.Board()):
        self.board = board

    def material_balance(self):
        white = self.board.occupied_co[chess.WHITE]
        black = self.board.occupied_co[chess.BLACK]
        return (
                chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns) +
                3 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
                3 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
                5 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
                9 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens))
        )

    def numberOFPieces(self, whoToMove):
        if whoToMove == 1:
            chosen = self.board.occupied_co[chess.WHITE]
        else:
            chosen = self.board.occupied_co[chess.BLACK]
        return (
                chess.popcount(chosen & self.board.pawns) +
                (chess.popcount(chosen & self.board.knights)) +
                (chess.popcount(chosen & self.board.bishops)) +
                (chess.popcount(chosen & self.board.rooks)) +
                (chess.popcount(chosen & self.board.queens))
        )

    def evaluationFunction(self, whoToMove):
        numberOfWhites = self.numberOFPieces(1)
        numberOfBlacks = self.numberOFPieces(-1)
        materialBalance = self.material_balance()
        return materialBalance * (numberOfWhites - numberOfBlacks) * whoToMove

    """
    :returns best move to make from current board state
    """
    def negaMax(self, depth: int, whoToMove: int) -> tuple:
        if depth == 0:
            return self.evaluationFunction(whoToMove), None

        maxScore = -999
        bestMove = None
        for legalMove in self.board.legal_moves:
            score = -(self.negaMax(depth - 1, -whoToMove)[0])
            if score == 0:
                score = random.random()
            if score > maxScore:
                maxScore = score
                bestMove = legalMove
        return maxScore, bestMove

    def negaScout(self, depth: int, whoToMove: int, alpha: int, beta: int) -> tuple:
        if depth == 0:
            return self.evaluationFunction(whoToMove), None

        bestMove = None
        for legalMove in self.board.legal_moves:
            score = -(self.negaScout(depth - 1, -whoToMove, -alpha + 1, -alpha)[0])
            #  NegaScout: re-iterate
            if score > alpha and score < beta and depth > 1:
                score2 = -(self.negaScout(depth - 1, -whoToMove, -beta, -score))[0]
                score = max(score, score2)
            #  custom addition for when the board is full and 0 is returned from evaluationFunction
            if score == 0:
                score = random.random()
            if score > alpha:
                alpha = score
                bestMove = legalMove
            #  NegaScout: cut-off obsolete nodes
            if alpha >= beta:
                return alpha, bestMove
            beta = alpha + 1
        return alpha, bestMove

    def PVC(self, depth: int, whoToMove: int, alpha: int, beta: int) -> tuple:
        if depth == 0:
            return self.evaluationFunction(whoToMove), None

        bestMove = None
        for legalMove in self.board.legal_moves:
            score = -(self.PVC(depth - 1, -whoToMove, -beta, -alpha)[0])
            #  NegaScout: re-iterate
            if (score > alpha) and (score < beta):
                score = -(self.PVC(depth - 1, -whoToMove, -beta, -score))[0]
            #  custom addition for when the board is full and 0 is returned from evaluationFunction
            if score == 0:
                score = random.random()
            if score > alpha:
                alpha = score
                bestMove = legalMove
            #  NegaScout: cut-off obsolete nodes
            if alpha >= beta:
                return alpha, bestMove
            beta = alpha + 1
        return alpha, bestMove


board = chess.Board()
negaAgent = NegaAgent(board)
depth, whoToMove = 5, -1

algoType = input("Input 1 for negaMax, 2 for negaScout and 3 for PVC: ")
while not board.is_checkmate():

    print("Game state:\n")
    print(board)
    move = input("Input your move: ")
    board.push_san(move)
    if algoType == 2:
        negaMove = negaAgent.negaScout(depth, whoToMove, -9999, 9999)[1]
    elif algoType == 3:
        negaMove = negaAgent.PVC(depth, whoToMove, -9999, 9999)[1]
    else:
        negaMove = negaAgent.negaMax(depth, whoToMove)[1]
    board.push(negaMove)


# len(board.pieces(1, chess.BLACK))
#  board.is_legal()
#board.push_san("g1h3")