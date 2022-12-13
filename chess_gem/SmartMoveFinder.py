import random
import numpy as np
from easygui import *
from chess_gem import  ChessEngine, Move
import ChessMain
from copy import copy, deepcopy
import time

CHECKMATE = 500000
STALEMATE = 0
COUNT = 0
callScoreBoard = 0
callGetMove = 0

pieceScore = {'K':10000, 'Q': 1000,'R': 500, 'B': 350, 'N': 300, 'p': 100}
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
piecePosistionScores = {'wN': knightScores, 'wB': bishopScores, 'wQ': queenScores, 'wR': rookScores, 'wp': whitePawnScores, 'wK': kingScores, 'bK': blackKingScores, 'bp': blackPawnScores, 'bN': blackKnightScores, 'bR': blackRookScores, 'bB': blackBishopScores, 'bQ': blackQueenScores}


#1 ply = 1 luot di chuyen
ply = 0
#killer and history heuristic
killerMove1 = [1, 2, 3, 4, 5, 6]
killerMove2 = [1, 2, 3, 4, 5, 6]
callEnable = 0
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

prevMove = None
endGameFlag = False

#for order the PV move to the top
pvMove = []
pvTable = []
scorePV = False
followPv = False
#mvv_lva heuristic                
MVV_LVA = np.array((
    (105, 205, 305, 405, 505, 605),
    (104, 204, 304, 404, 504, 604),
    (103, 203, 303, 403, 503, 603),
    (102, 202, 302, 402, 502, 602),
    (101, 201, 301, 401, 501, 601),
    (100, 200, 300, 400, 500, 600)
))
pieceToMVV_LVA = {'p': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K' : 5}

#to enable PV scoring
def enalbePvScoring(validMoves, depth):
    global scorePV 
    global followPv
    followPv = False
    if ply < depth - 1 and depth > 1:
        for move in validMoves:
            if move.startSq == pvTable[depth - 2][ply].startSq and move.endSq == pvTable[depth - 2][ply].endSq:
            # if move.startSq == pvTable[ply][ply].startSq and move.endSq == pvTable[ply][ply].endSq:
                scorePV = True
                followPv = True
#make score for each move
def scoreMove(gs, validMoves, depth):
    global scorePV
    for move in validMoves:
        if scorePV:
            if ply < depth - 1 and depth > 1:
                if move.startSq == pvTable[depth - 2][ply].startSq and move.endSq == pvTable[depth - 2][ply].endSq:
                    move.score = 20000  
                    scorePV = False      
                    continue
        #for capture move        
        if move.isCaptureMove:
            startPiece = move.pieceMoved[1]
            endPiece = move.pieceCaptured[1]
            move.score = MVV_LVA[pieceToMVV_LVA[startPiece]][pieceToMVV_LVA[endPiece]] + 10000
        #for non cap move
        if not move.isCaptureMove:
#            score 1st killer move
            if(isinstance(killerMove1[ply], Move.Move)):
                if killerMove1[ply].startSq == move.startSq and killerMove1[ply].endSq == move.endSq:
                    move.score = 9000
            #second killer move
            elif(isinstance(killerMove2[ply], Move.Move)) :
                if killerMove2[ply].startSq == move.startSq and killerMove2[ply].endSq == move.endSq:
                    move.score = 8000
            # score history move
            else:
                if historyMoves[move.pieceMoved].get(move.endSq) != None:
                    move.score = historyMoves[move.pieceMoved][move.endSq]
            
def sort_move(gs, validMoves, depth):
    scoreMove(gs, validMoves, depth)
    validMoves.sort(reverse=True, key = lambda x: x.score)
#sort and scoring for quiesence search
def scoreMoveQuie(gs, validMoves):
    for move in validMoves:
        if move.isCaptureMove:
            startPiece = move.pieceMoved[1]
            endPiece = move.pieceCaptured[1]
            move.score = MVV_LVA[pieceToMVV_LVA[startPiece]][pieceToMVV_LVA[endPiece]] + 10000
        if not move.isCaptureMove:
            # score 1st killer move
            # if(isinstance(killerMove1[ply], Move.Move)):
            #     if killerMove1[ply].startSq == move.startSq and killerMove1[ply].endSq == move.endSq:
            #         move.score = 9000
            # #second killer move
            # elif(isinstance(killerMove2[ply], Move.Move)) :
            #     if killerMove2[ply].startSq == move.startSq and killerMove2[ply].endSq == move.endSq:
            #         move.score = 8000
            #score history move
            # else:
                if historyMoves[move.pieceMoved].get(move.endSq) != None:
                    move.score = historyMoves[move.pieceMoved][move.endSq]
def sort_move_quie(gs, validMoves):
    scoreMoveQuie(gs, validMoves)
    # print("befiore sort, ", len(validMoves))
    validMoves.sort(reverse=True, key = lambda x: x.score)
    # print("after sort, ", len(validMoves))
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

def printKiller(killerMove1, killerMove2):
    for i in range(6):
        print('first: ', killerMove1[i], 'second: ', killerMove2[i])

def findBestMove(gs, validMoves, DEPTH, returnQueue):
    global pvMove
    global nextMove
    global killerMove1
    global killerMove2
    global pvTable
    global ply
    global historyMoves
    nextMove = None
    global COUNT 
    global callGetMove
    global callEnable
    global COUNTER
    global start_time
    global scorePV
    global followPv

    global endGameFlag
    global prevMove

    COUNTER = 0
    callGetMove = 0
    callEnable = 0
    COUNT = 0
    #restore those variable each time we call findBestMove
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

    scorePV = False
    followPv = False

    pvMove.clear()

    '''non-iterate deepending version'''
    #truyen truc tiep ca list vao findMoveNega, giong nhu truyen dia chi mang trong c++
    #type in python is usually object
    # temp = DEPTH
    # score = findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1, pvMove, temp)
    # # validMoves = gs.getValidMoves()
    # # killerMove1[ply] = validMoves[9]    
    # print("score ", score)
    # print('PV move depth ', DEPTH)
    # for move in pvMove:
    #     if isinstance(move, Move.Move):
    #         print(" ", move.getChessNotation())
    # print('number of tranversed node: ', COUNT)
    # print('number of get move : ', callGetMove)

    # printKiller(killerMove1, killerMove2)




    pvTable = []
    '''iterate deepending version'''
    alpha = -500000
    beta = 500000
    for currentDepth in range(1, gs.DEPTH + 1):

        # if endGameFlag:
        #     break

        # endGameFlag = False
        # prevMove = None

        followPv = True
        COUNT = 0
        ply = 0
        callGetMove = 0
        callEnable = 0
        pvMove.clear()
        #truyen truc tiep ca list vao findMoveNega, giong nhu truyen dia chi mang trong c++
        #type in python is usually object
        tempDepth = currentDepth
        score = findMoveNegaMaxAlphaBeta(gs, validMoves, currentDepth, alpha, beta, 1 if gs.whiteToMove else -1, pvMove, tempDepth, True)
        # print('--------------------')
        # printKiller(killerMove1, killerMove2)
        #solve null move bug theo phuong phap gia cay
        if pvMove == []:
            for i in range(currentDepth - 1):
                pvMove.append(pvTable[currentDepth - 2][i])
            pvMove.append(pvTable[0][0])

        pvTable.append(deepcopy(pvMove))

        if currentDepth == gs.DEPTH:
            print('score: ', score)
            print('number of tranversed node: ', COUNT)
            print('number of get move : ', callGetMove)

        if score <= alpha or score >= beta:
            alpha = -500000
            beta = 500000
            continue
        alpha = score - 50
        beta = score + 50
    # #print pv move each depth    
    for listMove in pvTable:
        for element in listMove:
            print(element.getChessNotation(), ' ')
        print('------------')
    returnQueue.put(nextMove)
#quiesence search after reach the end
def Quiesce(alpha, beta, depth, gs, validMoves, turnMultipler, currentDepth):

    evaluation = scoreBoard(gs)
    if depth == 0:
        return evaluation
    
    if(evaluation >= beta):
        return beta

    if evaluation > alpha:
        alpha = evaluation
    #make all possiblemove
    nextMoves = gs.getValidMoves()
    #sort all captureed move
    sort_move_quie(gs, gs.capturedMove)
    for move in  gs.capturedMove:
        gs.makeMove(move)
        score = -Quiesce(-beta, -alpha, depth -1,  gs, nextMoves, -turnMultipler, currentDepth)#max(a, b) = min(-a, -b) = -max(-a, -b)
        gs.undoMove()
        if score >= beta: #prunning happend
            return beta   
        if score > alpha:
            alpha = score
    return alpha
#nega max function
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultipler, pv, tempDepth, allowNull):
    global COUNT
    global callGetMove
    global callEnable
    global nextMove
    global ply
    global followPv
    global endGameFlag
    global prevMove
    global scorePV
    COUNT += 1
    #break condition
    if depth == 0 or len(validMoves) == 0:
        # return scoreBoard(gs)
        return Quiesce(alpha, beta, 7, gs, validMoves, turnMultipler, tempDepth)
    # #null move pruning
    if allowNull and not followPv:
        if depth >= 4 and ply >= 1 and gs.isKingInCheck == False:
            gs.whiteToMove = not gs.whiteToMove
            #nullify enpassant square
            gs.enpassant_possible_log.append(None)
            allowNull = False
            ply += 1
            scoreNull = -findMoveNegaMaxAlphaBeta(gs, validMoves, depth - 1 - 2, -beta, -beta + 1, -turnMultipler, [], tempDepth, allowNull)
            allowNull = True
            ply -= 1
            gs.whiteToMove = not gs.whiteToMove
            #revert enpassant back
            gs.enpassant_possible_log.pop()
            if scoreNull >= beta:
                return beta
    #enable follow pv line
    nextMoves = gs.getValidMoves()
    callGetMove += 1

    #check if endgame
    if len(nextMoves) == 0 :
        print('seems some one will lost ____________________________________________________________')

    if followPv:
        callEnable += 1
        enalbePvScoring(nextMoves, tempDepth)
    #sortMove function
    sort_move(gs, nextMoves, tempDepth)

    for move in nextMoves:
        childPV = []
        gs.makeMove(move)
        ply += 1
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha,  -turnMultipler, childPV, tempDepth, allowNull)#max(a, b) = min(-a, -b) = -max(-a, -b)
        ply -= 1
        gs.undoMove()

        if score >= beta: #fail soft
            #none capture move cause beta cut-off == killer move
            if not move.isCaptureMove:
                # print('depth of killer: ', ply)
                if isinstance(killerMove1[ply], int):
                    killerMove2[ply] = deepcopy(move)
                else:    
                    killerMove2[ply] = deepcopy(killerMove1[ply])  
                    killerMove1[ply] = deepcopy(move)    
            return beta    
            
        if score > alpha: #better move
            alpha = score
            if depth == gs.DEPTH :
                nextMove = move            
            if not move.isCaptureMove:
                if historyMoves[move.pieceMoved].get(move.endSq) == None :
                    historyMoves[move.pieceMoved][move.endSq] = 0
                    historyMoves[move.pieceMoved][move.endSq] += 1
                else:    
                    historyMoves[move.pieceMoved][move.endSq] += depth**2
            #pv move
            bestMove = deepcopy(move)
            pv.clear()
            pv.append(bestMove)
            pv += childPV

    return alpha

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
