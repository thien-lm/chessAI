import random

pieceScore = {'K': 0, 'Q': 10,'R': 5, 'B': 3, 'N': 3, 'p': 1}
CHECKMATE = 1000
STALEMATE = 0

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findGreedy(gs, validMoves):
    turnMultipler = 1 if gs.whiteToMove else -1

    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    #opponentMaxScore = -CHECKMATE
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponenstMoves = gs.getValidMoves()
        opponentMaxScore = -CHECKMATE
        for opponentsMove in opponenstMoves:
            gs.makeMove(opponentsMove)
            if gs.checkMate:
                score = -turnMultipler * CHECKMATE
            elif gs.staleMate:
                score = STALEMATE
            else: score = -turnMultipler*scoreMaterial(gs.board)

            if score > opponentMaxScore:
                opponentMaxScore = score
            #    bestPlayerMove = playerMove
            gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove


'''Score the board base on the material'''

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score