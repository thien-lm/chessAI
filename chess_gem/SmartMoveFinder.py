import random
import numpy as np
from easygui import *
from chess_gem import  ChessEngine, Move
import ChessMain
from copy import copy, deepcopy
import time

pieceScore = {'K': 10000, 'Q': 1000,'R': 500, 'B': 350, 'N': 300, 'p': 100}
knightScores = np.array((
                ( -5,   0,   0,   0,   0,   0,   0,  -5),
                 ( -5,   0,   0,  10,  10,   0,   0,  -5),
                 (-5,   5,  20,  20,  20,  20,   5,  -5),
                 ( -5,  10,  20,  30,  30,  20,  10,  -5),
                 (-5,  10,  20,  30,  30,  20,  10,  -5),
                 (-5,   5,  20,  10,  10,  20,   5,  -5),
                 (-5,   0,   0,   0,   0,   0,   0,  -5),
                 (-5, -10,   0,   0,   0,   0, -10,  -5)
                 ))
bishopScores = np.array((
    (0,   0,   0,   0,   0,   0,   0,   0),
     (0,   0,   0,   0,   0,   0,   0,   0),
     (0,   0,   0,  10,  10,   0,   0,   0),
     (0,   0,  10,  20,  20,  10,   0,   0),
     (0,   0,  10,  20,  20,  10,   0,   0),
     (0,  10,   0,   0,   0,   0,  10,   0),
     (0,  30,   0,   0,   0,   0,  30,   0),
     (0,   0, -10,   0,   0, -10,   0,   0)
))
rookScores = np.array((
    (50,  50,  50,  50,  50,  50,  50,  50),
    (50,  50,  50,  50,  50,  50,  50,  50),
    (0,   0,  10,  20,  20,  10,   0,   0),
     (0,   0,  10,  20,  20,  10,   0,   0),
     (0,   0,  10,  20,  20,  10,   0,   0),
     (0,   0,  10,  20,  20,  10,   0,   0),
     (0,   0,  10,  20,  20,  10,   0,   0),
     (0,   0,   0,  20,  20,   0,   0,   0)
))
kingScores = np.array((
     (0,   0,   0,   0,   0,   0,   0,   0),
     (0,   0,   5,   5,   5,   5,   0,   0),
     (0,   5,   5,  10,  10,   5,   5,   0),
     (0,   5,  10,  20,  20,  10,   5,   0),
     (0,   5,  10,  20,  20,  10,   5,   0),
     (0,   0,   5,  10,  10,   5,   0,   0),
     (0,   5,   5,  -5,  -5,   0,   5,   0),
     (0,   0,   5,   0, -15,   0,  10,   0)
))
queenScores = np.array(((0, 0, 0, 0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 0, 0, 0, 0),
                 (0, 0, 0, 0, 0, 0, 0, 0)))
whitePawnScores = np.array(((90,  90,  90,  90,  90,  90,  90,  90),
                 (30,  30,  30,  40,  40,  30,  30,  30),
                 (20,  20,  20,  30,  30,  30,  20,  20),
                 (10,  10,  10,  20,  20,  10,  10,  10),
                 (5,   5,  10,  20,  20,   5,   5,   5),
                 (0,   0,   0,   5,   5,   0,   0,   0),
                 (0,   0,   0, -10, -10,   0,   0,   0),
                 (0,   0,   0,   0,   0,   0,   0,   0)
                 ))
blackPawnScores = whitePawnScores[::-1]
blackRookScores = rookScores[::-1]
blackKnightScores = knightScores[::-1]
blackBishopScores = bishopScores[::-1]
blackQueenScores = queenScores[::-1]
blackKingScores = kingScores[::-1]

MVV_LVA = np.array((
    (105, 205, 305, 405, 505, 605),
    (104, 204, 304, 404, 504, 604),
    (103, 203, 303, 403, 503, 603),
    (102, 202, 302, 402, 502, 602),
    (101, 201, 301, 401, 501, 601),
    (100, 200, 300, 400, 500, 600)
))
pieceToMVV_LVA = {'p': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K' : 5}

piecePosistionScores = {'wN': knightScores, 'wB': bishopScores, 'wQ': queenScores, 'wR': rookScores, 'wp': whitePawnScores, 'wK': kingScores, 'bK': blackKingScores, 'bp': blackPawnScores, 'bN': blackKnightScores, 'bR': blackRookScores, 'bB': blackBishopScores, 'bQ': blackQueenScores}
               
def scoreMove(gs, validMoves):
    global ply
    for move in validMoves:
        if move.isCaptureMove:
            startPiece = move.pieceMoved[1]
            endPiece = move.pieceCaptured[1]
            move.score = MVV_LVA[pieceToMVV_LVA[startPiece]][pieceToMVV_LVA[endPiece]] + 10000
        else:#for non cap move
            # #score 1st killer move
            if(isinstance(killerMove1[ply], Move.Move)):
                if killerMove1[ply].pieceMoved == move.pieceMoved:
                    move.score = 9000
            if(isinstance(killerMove2[ply], Move.Move)):
                if killerMove2[ply].pieceMoved == move.pieceMoved:
                    move.score = 8000
            # elif killerMove2[ply].pieceMoved == move.pieceMoved:
            #     move.score = 8000
            # #score history move
            else:
                if historyMoves[move.pieceMoved].get(move.endSq) != None:
                    move.score = historyMoves[move.pieceMoved][move.endSq]

def sort_Move(gs, validMoves):
    
    scoreMove(gs, validMoves)
    # print("befiore sort, ", len(validMoves))
    validMoves.sort(reverse=True, key = lambda x: x.score)
    # print("after sort, ", len(validMoves))

CHECKMATE = 50000
STALEMATE = 0
COUNT = 0
callScoreBoard = 0
callGetMove = 0
ply = 0
killerMove1 = [1, 2, 3, 4, 5, 6]
killerMove2 = [1, 2, 3, 4, 5, 6]

historyMoves = {
    'wp' : {},
    'wR' : {},
    'wN' : {},
    'wB' : {},
    'wQ' : {},
    'wK' : {},
    'bp' : {},
    'bR' : {},
    'bN' : {},
    'bB' : {},
    'bQ' : {},
    'bK' : {}
}

pvMove = []

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
                gs.getValidMoves()
                #gs.getValidMoves()
                if gs.checkMate:
                    score =  CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else: score = -turnMultipler*scoreBoard(gs)

                if score > opponentMaxScore:
                    opponentMaxScore = score
                #    bestPlayerMove = playerMove
                gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove
SUM = 0
def findBestMove(gs, validMoves, DEPTH, returnQueue):
    
    global pvMove
    global nextMove
    global killerMove1
    global killerMove2
    global historyMoves
    global number_of_move 
    nextMove = None
    global COUNT 
    global callGetMove
    global COUNTER
    global start_time

    number_of_move = 0
    number_of_move += 1
    COUNTER = 0
    callGetMove = 0
    COUNT = 0
    
    killerMove1 = [1, 2, 3, 4, 5, 6]
    killerMove2 = [1, 2, 3, 4, 5, 6]
    historyMoves = {
    'wp' : {},
    'wR' : {},
    'wN' : {},
    'wB' : {},
    'wQ' : {},
    'wK' : {},
    'bp' : {},
    'bR' : {},
    'bN' : {},
    'bB' : {},
    'bQ' : {},
    'bK' : {}
}
    
    alpha = -50000
    beta = 50000
    for currentDepth in range(1, gs.DEPTH + 1):
        COUNT = 0
        callGetMove = 0
        pvMove.clear()
        #truyen truc tiep ca list vao findMoveNega, giong nhu truyen dia chi mang trong c++
        #type in python is usually object

        score = findMoveNegaMaxAlphaBeta(gs, validMoves, currentDepth, alpha, beta, 1 if gs.whiteToMove else -1, pvMove)
        print("score ", score)
        print('PV move depth ', currentDepth)
        for move in pvMove:
            if isinstance(move, Move.Move):
                print(" ", move.getChessNotation())
        print('number of tranversed node: ', COUNT)
        print('number of get move : ', callGetMove)

        if (score <= alpha) or score >= beta:
            alpha = -50000
            beta = 50000
            continue
        alpha = score - 50
        beta = score + 50

    returnQueue.put(nextMove)

def Quiescegeneratetrongfor(alpha, beta, depth, gs, validMoves, turnMultipler):
    
    evaluation = scoreBoard(gs)
    if depth == 0: return evaluation
    
    if(evaluation >= beta):
        return beta

    if evaluation > alpha:
        alpha = evaluation

    # validMoves = gs.getValidMoves()
    #sort_Move(gs, validMoves)
    for move in gs.capturedMove:
        gs.makeMove(move)
        nextMove = gs.getValidMoves()
        score = -Quiesce(-beta, -alpha, depth -1,  gs, nextMove, -turnMultipler)#max(a, b) = min(-a, -b) = -max(-a, -b)
        gs.undoMove()
        if score >= beta: #prunning happend
            return beta   
        if score > alpha:
            alpha = score
    return alpha

def Quiesce(alpha, beta, depth, gs, validMoves, turnMultipler):
    
    evaluation = scoreBoard(gs)
    if depth == 0: return evaluation
    
    if(evaluation >= beta):
        return beta

    if evaluation > alpha:
        alpha = evaluation

    nextMove = gs.getValidMoves()
    sort_Move(gs, gs.capturedMove)
    for move in gs.capturedMove:
        gs.makeMove(move)
        score = -Quiesce(-beta, -alpha, depth -1,  gs, nextMove, -turnMultipler)#max(a, b) = min(-a, -b) = -max(-a, -b)
        gs.undoMove()
        if score >= beta: #prunning happend
            return beta   
        if score > alpha:
            alpha = score
    return alpha

def findMoveNegaMaxAlphaBetanoob(gs, validMoves, depth, alpha, beta, turnMultipler):
    global COUNT
    global ply
    global nextMove
    global callGetMove
    COUNT += 1
    if depth == 0 or len(validMoves) == 0:
        # return scoreBoard(gs)
        return Quiesce(alpha, beta, 4, gs, validMoves, turnMultipler)
    
    
    sort_Move(gs, validMoves)
    for move in validMoves:
        gs.makeMove(move)
        ply += 1
        nextMoves = gs.getValidMoves()
        callGetMove += 1
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha,  -turnMultipler)#max(a, b) = min(-a, -b) = -max(-a, -b)
        ply -= 1
        gs.undoMove()

        if score >= beta: #fail soft
            if not move.isCaptureMove:
                killerMove2[ply] = deepcopy(killerMove1[ply])
                killerMove1[ply] = deepcopy(move)    
            return beta    

        if score > alpha: #better move
            pvMove[ply] = deepcopy(move)
            if not move.isCaptureMove:
                if historyMoves[move.pieceMoved].get(move.endSq) == None :
                    historyMoves[move.pieceMoved][move.endSq] = 0
                    historyMoves[move.pieceMoved][move.endSq] += 1
                else:    
                    historyMoves[move.pieceMoved][move.endSq] += depth**2
            alpha = score
            if depth == gs.DEPTH:
                nextMove = move
            
    return alpha

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultipler, pv):
    global COUNT
    global callGetMove
    global ply
    global nextMove
    COUNT += 1
    if depth == 0 or len(validMoves) == 0:
        # return scoreBoard(gs)
        return Quiesce(alpha, beta, 7, gs, validMoves, turnMultipler)
    
    nextMoves = gs.getValidMoves()
    callGetMove += 1
    sort_Move(gs, nextMoves)
    for move in nextMoves:
        childPV = []
        gs.makeMove(move)
        # if ply == 0 and move.getChessNotation() == 'e2a6':
        ply += 1
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha,  -turnMultipler, childPV)#max(a, b) = min(-a, -b) = -max(-a, -b)
        ply -= 1
        gs.undoMove()

        

        if score >= beta: #fail soft
            if not move.isCaptureMove:
                if isinstance(killerMove1[ply], Move.Move):
                    killerMove2[ply] = deepcopy(killerMove1[ply])
                else:
                    killerMove2[ply] = deepcopy(move)   
                killerMove1[ply] = deepcopy(move)    
            return beta    

        if score > alpha: #better move
            # print(ply)
            # pvMove[ply] = deepcopy(move)
            if not move.isCaptureMove:
                if historyMoves[move.pieceMoved].get(move.endSq) == None :
                    historyMoves[move.pieceMoved][move.endSq] = 0
                    historyMoves[move.pieceMoved][move.endSq] += 1
                else:    
                    historyMoves[move.pieceMoved][move.endSq] += depth**2
            alpha = score
            #pv move
            bestMove = deepcopy(move)
            pv.clear()
            pv.append(bestMove)
            pv += childPV
            if depth == gs.DEPTH:
                nextMove = move
            
    return alpha

def findMoveNegaMaxAlphaBetafake(gs, validMoves, depth, alpha, beta, turnMultipler):
    global COUNT
    global ply
    global nextMove
    if depth == 0 or len(validMoves) == 0:
        return scoreBoard(gs)
    COUNT += 1
    print('before ', len(validMoves))
    sort_Move(gs, validMoves)
    print('after ',len(validMoves) )
    # validMoves = sortMove(gs, validMoves, turnMultipler)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        ply += 1
        nextMoves = gs.getValidMoves()
        gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha,  -turnMultipler)#max(a, b) = min(-a, -b) = -max(-a, -b)
        if score > maxScore:
            
            maxScore = score
            if depth == gs.DEPTH:
                nextMove = move
        ply -= 1
        gs.undoMove()

        if maxScore > alpha: #prunning happend
            if not move.isCaptureMove:
                if historyMoves[move.pieceMoved].get(move.endSq) == None :
                    historyMoves[move.pieceMoved][move.endSq] = 0
                    historyMoves[move.pieceMoved][move.endSq] += 1
                else:    
                    historyMoves[move.pieceMoved][move.endSq] += depth**2
                alpha = maxScore

        if alpha >= beta:
            if not move.isCaptureMove:
                killerMove2[ply] = deepcopy(killerMove1[ply])
                killerMove1[ply] = deepcopy(move)
            break
    return maxScore

def sortMove(gs, moveList, turnMultipler):
    # random.shuffle(moveList)
    global COUNTER
    COUNTER += 1
    global start_time
    start_time = time.time()
    # moveList = tuple(moveList[::-1])
    score = []
    for i in range(len(moveList)):
        gs.makeMove(moveList[i])
        score.append(scoreBoard(gs))#10000 node of scorematerial faster than 10k node scoreboard
        gs.undoMove()
    newListA = []
    newListB = list(moveList)
    list_loca = []
    if turnMultipler == 1:
        for i in range(min(len(moveList), 6)):
            maxScore = -1000000
            maxLocation = 0
            global checkJ
            checkJ = False 
            for j in range(len(moveList)):
                if score[j] > maxScore:
                    checkJ = True
                    maxScore = score[j]
                    maxLocation = j
                    list_loca.append(maxLocation)
            score[maxLocation] = -1000000
            if checkJ:
                newListA.append(moveList[maxLocation])


    if turnMultipler == -1:
        for i in range(min(len(moveList), 6)):
            maxScore = 1000000
            maxLocation = 0
            checkJ = False 
            for j in range(len(moveList)):
                if score[j] < maxScore:
                    checkJ = True
                    maxScore = score[j]
                    maxLocation = j
                    list_loca.append(maxLocation)
            score[maxLocation] = 1000000
            if checkJ:
                newListA.append(moveList[maxLocation])

    for i in range(len(list_loca)):
        newListB[list_loca[i]] = "null"

    newListB = [i for i in newListB if i != "null"]
        
    # print("sort all move take: " + "--- %s seconds ---" % (time.time() - start_time))

    return newListA + newListB


def scoreMaterial(board):

    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score

'''Score the board base on the material'''
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE#blackwin
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in range(8):
        for col in range(8):
            square = gs.board[row][col]
            if square != "--":
                #score it possitionally
                piecePosistionScore = 0
                piecePosistionScore = piecePosistionScores[square][row][col]
                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePosistionScore
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePosistionScore
    return score if gs.whiteToMove else -score
