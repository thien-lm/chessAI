import random

pieceScore = {'K': 0, 'Q': 10,'R': 5, 'B': 3, 'N': 3, 'p': 1}
knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],
               [1, 2, 3, 3, 3, 3, 1, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 3, 3, 3, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],               
               [1, 1, 1, 1, 1, 1, 1, 1]]
# scorilize
knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],
               [1, 2, 3, 3, 3, 3, 1, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 3, 3, 3, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],               
               [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],
               [1, 2, 3, 3, 3, 3, 1, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 3, 3, 3, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],               
               [1, 1, 1, 1, 1, 1, 1, 1]]

rookScores = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],
               [1, 2, 3, 3, 3, 3, 1, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 3, 3, 3, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],               
               [1, 1, 1, 1, 1, 1, 1, 1]]

queenScores = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],
               [1, 2, 3, 3, 3, 3, 1, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 3, 3, 3, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],               
               [1, 1, 1, 1, 1, 1, 1, 1]]

whitePawnScores = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],
               [1, 2, 3, 3, 3, 3, 1, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 3, 3, 3, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],               
               [1, 1, 1, 1, 1, 1, 1, 1]]

blackPawnScores = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],
               [1, 2, 3, 3, 3, 3, 1, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 3, 3, 3, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],               
               [1, 1, 1, 1, 1, 1, 1, 1]]

piecePosistionScores = {'N': knightScores, 'B': bishopScores, 'Q': queenScores, 'R': rookScores, 'bp': blackPawnScores, 'wp': whitePawnScores}

               

CHECKMATE = 5
STALEMATE = 0
DEPTH = 4

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
        if gs.staleMate: 
            opponentMaxScore = STALEMATE
        elif gs.checkMate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponenstMoves:
                gs.makeMove(opponentsMove)
                #gs.getValidMoves()
                if gs.checkMate:
                    score =  CHECKMATE
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

def findBestMove(gs, validMoves, returnQueue):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    #findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1 )
    #findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove )
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(nextMove)
    returnQueue.put(nextMove)


def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove 

    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        miniScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < miniScore:
                miniScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return miniScore

'''positive score is good for white'''
def scoreBoard(gs):

    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE#blackwin
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                #score it possitionally
                piecePosistionScore = 0
                if square[1] != "K":
                    if square[1] == 'p':
                        piecePosistionScore = piecePosistionScores[square][row][col]
                    else:
                        piecePosistionScore = piecePosistionScores[square[1]][row][col]
                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePosistionScore
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePosistionScore
    return score

def findMoveNegaMax(gs, validMoves, depth, turnMultipler):
    global nextMove
    if depth == 0:
        return turnMultipler * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultipler)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultipler):
    global nextMove
    if depth == 0:
        return turnMultipler * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha,  -turnMultipler)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha: #prunning happend
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

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