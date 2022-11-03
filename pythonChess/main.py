from math import inf
import chess
import constants
board = chess.Board()

class ChessNegaMax:
    whites = ['P', 'N', "R", "Q", "B"]
    blacks = ["p", "n", "r", "q", "b"]

    def piecesCountHelper(self, gameState, color):
        fen = gameState.fen()
        numberOfAllPieces = 0

        if color == "white":
            for piece in self.whites:
                fen.count(piece)
                numberOfAllPieces += 1
        else:
            for piece in self.blacks:
                fen.count(piece)
                numberOfAllPieces += 1

        return numberOfAllPieces

    def materialWeightEvaluationHelper(self, gameState):
        fen = gameState.fen()
        weight = 0
        for white, black in zip(self.whites, self.blacks):
            valueOfFigure = getattr(constants, white)
            numWhite = fen.count(white)
            numBlack = fen.count(black)
            difference = (numWhite - numBlack) * valueOfFigure
            weight += difference
        return weight

    def evaluationFunction(self, gameState: chess.Board(), whoToGo) -> int:
        numOfAllWhites = self.piecesCountHelper(gameState, "white")
        numOfAllBlacks = self.piecesCountHelper(gameState, "black")
        materialWeight = self.materialWeightEvaluationHelper(gameState)

        return materialWeight * (numOfAllWhites - numOfAllBlacks) * whoToGo

    def negaMax(self, gameState: chess.Board(), depth, whoToGo) -> tuple:
        typesOfDraw = gameState.can_claim_draw() or gameState.can_claim_fifty_moves() \
                      or gameState.is_insufficient_material() or gameState.is_stalemate()

        if depth == 0 or typesOfDraw or gameState.is_checkmate():
            return self.evaluationFunction(gameState, whoToGo), None

        maxScore = -inf
        legalMoves = gameState.legal_moves
        bestMove = None
        for move in legalMoves:
            gameState.push_san(move.uci())
            score = -self.negaMax(gameState, depth - 1, whoToGo * -1)[0]
            gameState.pop()
            maxScore = max(maxScore, score)
            if score == maxScore:
                bestMove = move

        return maxScore, bestMove

    def negaScout(self,gameState: chess.Board(), depth, whoToGo, alpha, beta):
        typesOfDraw = gameState.can_claim_draw() or gameState.can_claim_fifty_moves() \
                      or gameState.is_insufficient_material() or gameState.is_stalemate()

        if depth == 0 or typesOfDraw or gameState.is_checkmate():
            return self.evaluationFunction(gameState, whoToGo), None

        maxScore = -inf
        legalMoves = gameState.legal_moves
        bestMove = None
        for move,i in  zip(legalMoves, range(len(legalMoves))):
            gameState.push_san(move.uci())
            score = -self.negaScout(gameState, depth - 1, whoToGo * -1)[0]

            if score > alpha and score < beta and i > 1 and depth == 1:
                a = -self.negaScout(gameState, depth - 1, whoToGo * -1, -beta, -score)

            gameState.pop()



chessNegaMax = ChessNegaMax()

bestMoveScore = chessNegaMax.negaMax(board, 3, 1)

print(bestMoveScore[1])

