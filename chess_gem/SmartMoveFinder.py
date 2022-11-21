import random
import numpy as np
from easygui import *
from chess_gem import  ChessEngine
import ChessMain

pieceScore = {'K': 100000, 'Q': 900,'R': 500, 'B': 300, 'N': 300, 'p': 100}
# knightScores = np.array([[1, 1, 1, 1, 1, 1, 1, 1],
#                [1, 2, 2, 2, 2, 2, 2, 1],
#                [1, 2, 3, 3, 3, 3, 1, 1],
#                [1, 2, 3, 4, 4, 3, 2, 1],
#                [1, 2, 3, 4, 4, 3, 2, 1],
#                [1, 2, 3, 3, 3, 3, 1, 1],
#                [1, 2, 2, 2, 2, 2, 2, 1],               
#                [1, 1, 1, 1, 1, 1, 1, 1]])
# scorilize
knightScores = np.array([[0, 10, 20, 20 ,20, 20, 10, 10],
                 [10, 30, 50, 50, 50, 50, 30, 10],
                 [20, 55, 60, 65, 65, 60, 55, 20],
                 [20, 55, 60, 65, 65, 60, 55, 20],
                 [20, 50, 65, 70, 70, 65, 50, 20],
                 [20, 55, 60, 65, 65, 60, 55, 20],
                 [10, 30, 50, 55, 55, 50, 30, 10],
                 [0, 10, 20, 20 ,20, 20, 10, 0]])


bishopScores = np.array([[0, 20, 20, 20, 20, 20, 20, 0],
                 [20, 40, 40, 40, 40, 40, 40, 20],
                 [20, 40, 50, 60, 60, 50, 40, 20],
                 [20, 50, 50, 50, 60, 50, 50, 20],
                 [20, 40, 60, 60, 60, 60, 40, 20],
                 [20, 60, 60, 60, 60, 60, 60, 20],
                 [20, 50, 40, 40, 40, 40, 50, 20],
                 [0, 20, 20, 20, 20, 20, 20, 0]])

rookScores = np.array([[25, 25, 25, 50, 25, 50, 25, 25],
               [50, 75, 75, 75, 75, 75, 75, 50],
               [0, 25, 25, 25, 25, 25, 25, 0],
               [0, 25, 25, 25, 25, 25, 25, 0],
               [0, 25, 25, 25, 25, 25, 25, 0],
               [0, 25, 25, 25, 25, 25, 25, 0],
               [0, 25, 25, 25, 25, 25, 25, 0],
               [25, 25, 25, 50, 25, 50, 25, 25]])

queenScores = np.array([[0, 20, 20, 30, 30, 20, 20, 0],
                 [20, 40, 40, 40, 40, 40, 40, 20],
                 [20, 40, 50, 50, 50, 50, 40, 20],
                 [30, 40, 50, 50, 50, 50, 40, 30],
                 [40, 40, 50, 50, 50, 50, 40, 30],
                 [20, 40, 50, 50, 50, 50, 40, 20],
                 [20, 40, 40, 40, 40, 40, 40, 20],
                 [0, 20, 20, 30, 30, 20, 20, 0]])

whitePawnScores = np.array([[80, 80, 80, 80, 80, 80, 80, 80],
                 [70, 70, 70, 70, 70, 70, 70, 70],
                 [30, 30, 40, 50, 50, 40, 30, 30],
                 [25, 25, 30, 45, 45, 30, 25, 25],
                 [20, 20, 20, 40, 40, 20, 20, 20],
                 [25, 15, 10, 20, 20, 10, 15, 25],
                 [25, 30, 30, 0, 0, 30, 30, 25],
                 [0, 0, 0, 0 ,0, 0, 0, 0]])

blackPawnScores = np.array([[0, 0, 0, 0 ,0, 0, 0, 0],
                 [10, 30, 50, 50, 50, 50, 30, 10],
                 [25, 15, 10, 20, 20, 10, 15, 25],
                 [20, 20, 20, 40, 40, 20, 20, 20],
                 [25, 25, 30, 45, 45, 30, 25, 25],
                 [30, 30, 40, 50, 50, 40, 30, 30],
                 [70, 70, 70, 70, 70, 70, 70, 70],
                 [80, 80, 80, 80, 80, 80, 80, 80]])

piecePosistionScores = {'N': knightScores, 'B': bishopScores, 'Q': queenScores, 'R': rookScores, 'bp': blackPawnScores, 'wp': whitePawnScores}

               

CHECKMATE = 500000
STALEMATE = 0
COUNT = 0
# DEPTH = 3
# def defineDepth(): 
#     # message to be displayed
#     text = "Enter depth lv !!"
        
#         # window title
#     title = "thien dzai sieu cap vjppr0"
        
#         # default text
#     d_text = "3"
        
#         # creating a enter box
#     output = enterbox(text, title, d_text)
        
#         # title for the message box
#     title = "chose level"
        
#         # creating a message
#     global DEPTH
#     DEPTH = int(output)
# print(DEPTH)

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

def findBestMove(gs, validMoves, DEPTH, returnQueue):
    global nextMove
    nextMove = None
    global COUNT 
    COUNT = 0
    random.shuffle(validMoves)
    #findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1 )
    #findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove )
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(COUNT)
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
    global COUNT
    COUNT += 1
    global nextMove
    if depth == 0:
        return turnMultipler * scoreBoard(gs)
    validMoves = sortMove(gs, validMoves)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha,  -turnMultipler)
        if score > maxScore:
            maxScore = score
            if depth == gs.DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha: #prunning happend
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

'''Score the board base on the material'''

def sortMove(gs, moveList):
    # random.shuffle(moveList)
    moveList = moveList[::-1]
    score = []
    for i in range(len(moveList)):
        gs.makeMove(moveList[i])
        score.append(scoreBoard(gs))
        gs.undoMove()
    newListA = []
    newListB = moveList

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
        score[maxLocation] = -1000000
        if checkJ:
            newListA.append(moveList[maxLocation])
            newListB.pop(maxLocation)

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