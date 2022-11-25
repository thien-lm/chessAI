import random
import numpy as np
from easygui import *
from chess_gem import  ChessEngine
import ChessMain
import time

pieceScore = {'K': 0, 'Q': 900,'R': 500, 'B': 300, 'N': 300, 'p': 100}
# knightScores = np.array([[1, 1, 1, 1, 1, 1, 1, 1],
#                [1, 2, 2, 2, 2, 2, 2, 1],
#                [1, 2, 3, 3, 3, 3, 1, 1],
#                [1, 2, 3, 4, 4, 3, 2, 1],
#                [1, 2, 3, 4, 4, 3, 2, 1],
#                [1, 2, 3, 3, 3, 3, 1, 1],
#                [1, 2, 2, 2, 2, 2, 2, 1],               
#                [1, 1, 1, 1, 1, 1, 1, 1]])
# scorilize
knightScores = np.array(([0, 10, 20, 20 ,20, 20, 10, 10],
                 [10, 30, 50, 50, 50, 50, 30, 10],
                 [20, 55, 60, 65, 65, 60, 55, 20],
                 [20, 55, 60, 65, 65, 60, 55, 20],
                 [20, 50, 65, 70, 70, 65, 50, 20],
                 [20, 55, 60, 65, 65, 60, 55, 20],
                 [10, 30, 50, 55, 55, 50, 30, 10],
                 [0, 10, 20, 20 ,20, 20, 10, 0]))
bishopScores = np.array(([0, 20, 20, 20, 20, 20, 20, 0],
                 [20, 40, 40, 40, 40, 40, 40, 20],
                 [20, 40, 50, 60, 60, 50, 40, 20],
                 [20, 50, 50, 50, 60, 50, 50, 20],
                 [20, 40, 60, 60, 60, 60, 40, 20],
                 [20, 60, 60, 60, 60, 60, 60, 20],
                 [20, 50, 40, 40, 40, 40, 50, 20],
                 [0, 20, 20, 20, 20, 20, 20, 0]))
rookScores = np.array(([25, 25, 25, 50, 25, 50, 25, 25],
               [50, 75, 75, 75, 75, 75, 75, 50],
               [0, 25, 25, 25, 25, 25, 25, 0],
               [0, 25, 25, 25, 25, 25, 25, 0],
               [0, 25, 25, 25, 25, 25, 25, 0],
               [0, 25, 25, 25, 25, 25, 25, 0],
               [0, 25, 25, 25, 25, 25, 25, 0],
               [25, 25, 25, 50, 25, 50, 25, 25]))
queenScores = np.array(([0, 20, 20, 30, 30, 20, 20, 0],
                 [20, 40, 40, 40, 40, 40, 40, 20],
                 [20, 40, 50, 50, 50, 50, 40, 20],
                 [30, 40, 50, 50, 50, 50, 40, 30],
                 [40, 40, 50, 50, 50, 50, 40, 30],
                 [20, 40, 50, 50, 50, 50, 40, 20],
                 [20, 40, 40, 40, 40, 40, 40, 20],
                 [0, 20, 20, 30, 30, 20, 20, 0]))
whitePawnScores = np.array(([80, 80, 80, 80, 80, 80, 80, 80],
                 [70, 70, 70, 70, 70, 70, 70, 70],
                 [30, 30, 40, 50, 50, 40, 30, 30],
                 [25, 25, 30, 45, 45, 30, 25, 25],
                 [20, 20, 20, 40, 40, 20, 20, 20],
                 [25, 15, 10, 20, 20, 10, 15, 25],
                 [25, 30, 30, 0, 0, 30, 30, 25],
                 [0, 0, 0, 0 ,0, 0, 0, 0]))
blackPawnScores = np.array(([0, 0, 0, 0 ,0, 0, 0, 0],
                 [10, 30, 50, 50, 50, 50, 30, 10],
                 [25, 15, 10, 20, 20, 10, 15, 25],
                 [20, 20, 20, 40, 40, 20, 20, 20],
                 [25, 25, 30, 45, 45, 30, 25, 25],
                 [30, 30, 40, 50, 50, 40, 30, 30],
                 [70, 70, 70, 70, 70, 70, 70, 70],
                 [80, 80, 80, 80, 80, 80, 80, 80]))

# piecePosistionScores = {"wN": np.array(knightScores),
#                          "bN": np.array(knightScores[::-1]),
#                          "wB": np.array(bishopScores),
#                          "bB": np.array(bishopScores[::-1]),
#                          "wQ": np.array(queenScores),
#                          "bQ": np.array(queenScores[::-1]),
#                          "wR": np.array(rookScores),
#                          "bR": np.array(rookScores[::-1]),
#                          "wp": np.array(whitePawnScores),
#                          "bp": np.array(blackPawnScores[::-1])}

piecePosistionScores = {'N': knightScores, 'B': bishopScores, 'Q': queenScores, 'R': rookScores, 'bp': blackPawnScores, 'wp': whitePawnScores}
               

CHECKMATE = 50000
STALEMATE = 0
COUNT = 0


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
SUM = 0
def findBestMove(gs, validMoves, DEPTH, returnQueue):
    # print(gs.blackKingLocation)
    global SUM
    global nextMove
    nextMove = None
    global number_of_move 
    number_of_move = 0
    number_of_move += 1
    global COUNT 
    
    
    COUNT = 0
    global start_time
    start_time = time.time()
    #random.shuffle(validMoves)
    #findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1 )
    #findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove )
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    SUM += COUNT
    print("all node take: " + "--- %s seconds ---" % (time.time() - start_time))
    print(COUNT)
    #print(SUM/number_of_move)
    returnQueue.put(nextMove)


# def scoreBoard(gs):

#     if gs.checkMate:
#         if gs.whiteToMove:
#             return -CHECKMATE#blackwin
#         else:
#             return CHECKMATE
#     elif gs.staleMate:
#         return STALEMATE

#     score = 0
#     for row in range(8):
#         for col in range(8):
#             square = gs.board[row][col]
#             if square != "--":
#                 #score it possitionally
#                 piecePosistionScore = 0
#                 if square[1] != "K":
#                     if square[1] == 'p':
#                         piecePosistionScore = piecePosistionScores[square][row][col]
#                     else:
#                         piecePosistionScore = piecePosistionScores[square[1]][row][col]
#                 if square[0] == 'w':
#                     score += pieceScore[square[1]] + piecePosistionScore
#                 elif square[0] == 'b':
#                     score -= pieceScore[square[1]] + piecePosistionScore
#     return score

# def scoreBoard(game_state):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    # if game_state.checkMate:
    #     if game_state.whiteToMove:
    #         return -CHECKMATE  # black wins
    #     else:
    #         return CHECKMATE  # white wins
    # elif game_state.staleMate:
    #     return STALEMATE
    # score = 0
    # is_endgame = False
    # white_has_queen = False
    # black_has_queen = False
    # white_additional_pieces = 0
    # black_additional_pieces = 0
    # for row in game_state.board:
    #     for piece in row:
    #         if piece == "wQ":
    #             white_has_queen = True
    #         if piece == "bQ":
    #             black_has_queen = True
    #         if piece == "wR" or piece == "wB" or piece == "wN":
    #             white_additional_pieces += 1
    #         if piece == "bR" or piece == "bB" or piece == "bN":
    #             black_additional_pieces += 1
    # if (not white_has_queen and not black_has_queen) or (white_has_queen and white_additional_pieces < 2) or (
    #         black_has_queen and black_additional_pieces < 2):
    #     is_endgame = True

    # for row in range(len(game_state.board)):
    #     for col in range(len(game_state.board[row])):
    #         piece = game_state.board[row][col]
    #         if piece != "--":
    #             piece_position_score = 0
    #             if piece[1] != "K":
    #                 piece_position_score = piecePosistionScores[piece][row][col]
    #             if piece[0] == "w":
    #                 score += pieceScore[piece[1]] + piece_position_score
    #             if piece[0] == "b":
    #                 score -= pieceScore[piece[1]] + piece_position_score

    # return score




def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultipler):
    global COUNT
    COUNT += 1
    global start_time
    # if COUNT == 1000:
    #     print("1000 node take: " + "--- %s seconds ---" % (time.time() - start_time))
    global nextMove
    if depth == 0 or len(validMoves) == 0:
        return turnMultipler * scoreBoard(gs)
    validMoves = sortMove(gs, validMoves, turnMultipler)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha,  -turnMultipler)#max(a, b) = min(-a, -b) = -max(-a, -b)
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


def sortMove(gs, moveList, turnMultipler):
    # random.shuffle(moveList)
    moveList = tuple(moveList[::-1])
    score = []
    for i in range(len(moveList)):
        gs.makeMove(moveList[i])
        score.append(scoreBoard(gs))#10000 node of scorematerial faster than 10k node scoreboard
        gs.undoMove()
    newListA = []
    newListB = list(moveList)
    list_loca = []
    if turnMultipler == 1:
        for i in range(min(len(moveList), 8)):
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
        for i in range(min(len(moveList), 8)):
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
        


    return newListA + newListB


    # if turnMultipler == 1:
    #     for i in range(min(len(moveList), 6)):
    #         maxScore = -1000000
    #         maxLocation = 0
    #         global checkJ
    #         checkJ = False 
    #         for j in range(len(moveList)):
    #             if score[j] > maxScore:
    #                 checkJ = True
    #                 maxScore = score[j]
    #                 maxLocation = j
    #         score[maxLocation] = -1000000
    #         if checkJ:
    #             newListA.append(moveList[maxLocation])
    #             newListB.pop(maxLocation)

    # if turnMultipler == -1:
    #     for i in range(min(len(moveList), 6)):
    #         maxScore = 1000000
    #         maxLocation = 0
    #         checkJ = False 
    #         for j in range(len(moveList)):
    #             if score[j] < maxScore:
    #                 checkJ = True
    #                 maxScore = score[j]
    #                 maxLocation = j
    #         score[maxLocation] = 1000000
    #         if checkJ:
    #             newListA.append(moveList[maxLocation])
    #             newListB.pop(maxLocation)

    # return newListA + newListB


    #if turnMultipler == 1:
    # for i in range(min(len(moveList), 6)):
    #     maxScore = -1000000
    #     maxLocation = 0
    #     global checkJ
    #     checkJ = False 
    #     for j in range(len(moveList)):
    #         if score[j] > maxScore:
    #             checkJ = True
    #             maxScore = score[j]
    #             maxLocation = j
    #     score[maxLocation] = -1000000
    #     if checkJ:
    #         newListA.append(moveList[maxLocation])
    #         newListB.pop(maxLocation)

    #     # if turnMultipler == 1: 
    # return newListA + newListB
def scoreMaterial(board):

    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score
