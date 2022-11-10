#TODO: use numpy instead of array
from logging import captureWarnings
from multiprocessing import RLock
from chess import Board
from numpy import blackman
from chess_gem.Move import Move
class GameState():
    def __init__(self):
        # represent a 8x8 chess Board
        # bR = black Rock
        # wR = white Rock
        self.board = [
            ["--", "bN", "--", "--", "bK", "--", "bN", "--"],
            ['bp', 'bp', 'bp', '--', '--', '--', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', 'wQ', '--', 'wQ', 'bp', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', 'bp', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ["--", "wN", "wB", "wQ", "wK", "wB", "wN", "--"]
        ]
        self.moveFunction = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'K': self.getKingMoves, 'Q': self.getQueenMoves}
        self.whiteToMove =  True
        self.moveLog = [] 
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move to display it later
        self.whiteToMove = not self.whiteToMove #switch turn
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'


    ''' undo the lastMove'''  
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            #update king's locaiton
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.endRow, move.endCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.endRow, move.endCol)

    '''
    checking move
    '''        
    def getValidMoves(self):
        #need consider check
        #1. generate all possible move
        moves = self.getAllPossibleMoves()
        #2 make move for each move
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
        #3 generate all opponet's move

        #4 for each opponent move, check if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])

        #5 if they do attack your king, not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            print('winner appeared')
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return moves
#determine if current player incheck
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

#determmine if the enemy can attack square r, c
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove#switch to oppoent turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove        
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #sqr is under attack
                return True
        return False



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
    
