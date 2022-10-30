#TODO: use numpy instead of array

from logging import captureWarnings
from multiprocessing import RLock
from chess import Board
from numpy import blackman


class GameState():
    def __init__(self):
        # represent a 8x8 chess Board
        # bR = black Rock
        # wR = white Rock
        self.board = [
            ["--", "bN", "bB", "bQ", "bK", "bB", "bN", "--"],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', 'wR', '--', '--', 'bp', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', 'bp', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ["--", "wN", "wB", "wQ", "wK", "wB", "wN", "--"]
        ]
        self.moveFunction = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'K': self.getKingMoves, 'Q': self.getQueenMoves}
        self.whiteToMove =  True
        self.moveLog = [] 

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move to display it later
        self.whiteToMove = not self.whiteToMove #switch turn

    ''' undo the lastMove'''  
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
    '''
    checking move
    '''        
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    '''
    all moves without check
    '''

    def getAllPossibleMoves(self):
        moves = []

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunction[piece](r, c, moves)

        return moves                

    '''get all pawn move'''

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == '--':
                moves.append(Move((r, c), (r-1, c), self.board))#moves: possible move
                if r == 6 and self.board[r-2][c] == '--':#2 move first time
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c - 1 >= 0:#cap left
                if self.board[r-1][c-1][0] == 'b':#enemy piece to cap
                    moves.append(Move((r, c), (r-1, c-1), self.board))

            if c+1 <= 7: #cap right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else:
            if r+1 <= 7 and self.board[r+1][c] == '--':
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == '--':#2 move first time
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c + 1 <= 7 and r + 1 <= 7:#cap right
                if self.board[r+1][c+1][0] == 'w':#enemy piece to cap
                    moves.append(Move((r, c), (r+1, c+1), self.board))

            if c - 1 >= 0 and r + 1 <= 7: #cap left
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))                                


    def getRookMoves(self, r, c, moves):
        # temp1 = r
        # temp2 = c
        # if self.whiteToMove:
        #     #right
        #     if c + 1 <= 7:
        #         temp2 += 1
        #         while self.board[temp1][temp2] == '--':
        #             moves.append(Move((r,c), (temp1, temp2), self.board))
        #             temp2 += 1
        #             if temp2 > 7 : break
        #             if self.board[temp1][temp2][0] == 'b':
        #                 moves.append(Move((r,c), (temp1, temp2), self.board))
        #                 break
        #     #left
        #     temp2 = c
        #     if c - 1 >= 0:
        #         temp2 -= 1
        #         moves.append(Move((r, c), (r, 0), self.board))
        #         while self.board[temp1][temp2] == '--':
        #             moves.append(Move((r, c), (temp1, temp2), self.board))
        #             temp2 -= 1
        #             if temp2 < 0 : break
        #             if self.board[temp1][temp2][0] == 'b':
        #                 moves.append(Move((r,c), (temp1, temp2), self.board))
        #                 break

        #     temp2 = c
        #     if c - 1 >= 0:
        #         temp2 -= 1
        #         moves.append(Move((r, c), (r, 0), self.board))
        #         while self.board[temp1][temp2] == '--':
        #             moves.append(Move((r, c), (temp1, temp2), self.board))
        #             temp2 -= 1
        #             if temp2 < 0 : break
        #             if self.board[temp1][temp2][0] == 'b':
        #                 moves.append(Move((r,c), (temp1, temp2), self.board))
        #                 break

        directions = ((-1, 0), (1, 0), (0, 1), (0, -1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endCol < 8 and 0 <= endRow < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                     break    
                                       


    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-1, 2), (-1, -2), (1, 2), (1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
        ally  = 'w' if self.whiteToMove else 'b'
        for k in knightMoves:
                endRow = r + k[0]
                endCol = c + k[1]
                if 0 <= endCol < 8 and 0 <= endRow < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece != ally:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (1, 1), (1, -1), (-1, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endCol < 8 and 0 <= endRow < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                     break    
                              
    def getQueenMoves(self, r, c, moves):
        directions = ((-1, -1), (1, 1), (1, -1), (-1, 1), (-1, 0), (1, 0), (0, 1), (0, -1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endCol < 8 and 0 <= endRow < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                     break                    

    
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, 1), (-1, -1), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (1, 0))
        ally  = 'w' if self.whiteToMove else 'b'
        for i in range(8):
                endRow = r + kingMoves[i][0]
                endCol = c + kingMoves[i][1]
                if 0 <= endCol < 8 and 0 <= endRow < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != ally:
                        moves.append(Move((r, c), (endRow, endCol), self.board))                            
    

class Move():
    #map keys to values
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        #print(self.moveID)


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]        
