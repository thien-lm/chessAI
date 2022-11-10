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
            ["bR", "--", "--", "--", "bK", "--", "--", "bR"],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', 'bp', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', 'bp', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', 'wp', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ["wR", "--", "--", "--", "wK", "--", "--", "wR"]
        ]
        self.moveFunction = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'K': self.getKingMoves, 'Q': self.getQueenMoves}
        self.whiteToMove =  True
        self.moveLog = [] 
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move to display it later
        self.whiteToMove = not self.whiteToMove #switch turn
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'

                else:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                    self.board[move.endRow][move.endCol -2 ] = '--'


        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'

                else:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                    self.board[move.endRow][move.endCol -2 ] = '--'

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # if move.isCastleMove:
        #     if move.endCol - move.startCol == 2:
        #         self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
        #         self.board[move.endRow][move.endCol + 1] = '--'

        #     else:
        #         self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
        #         self.board[move.endRow][move.endCol -2 ] = '--'

        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

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
            #undo castlingRight
            self.castleRightsLog.pop()
            # self.currentCastlingRight = self.castleRightsLog[-1]

            self.currentCastlingRight.wks = self.castleRightsLog[-1].wks
            self.currentCastlingRight.wqs = self.castleRightsLog[-1].wqs
            self.currentCastlingRight.bks = self.castleRightsLog[-1].bks
            self.currentCastlingRight.bqs = self.castleRightsLog[-1].bqs

            #undo
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else :
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'


    def updateCastleRights(self, move):

        # if move.pieceCaptured == "wR":
        #     if move.endCol == 0: #left rook
        #         self.currentCastlingRight.wqs = False
        #     elif move.endCol == 7: #right rook
        #         self.currentCastlingRight.wks = False
        # elif move.pieceCaptured == "bR":
        #     if move.endCol == 0: #left rook
        #         self.currentCastlingRight.bqs = False
        #     elif move.endCol == 7: #right rook
        #         self.currentCastlingRight.bks = False

        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False

        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False

    '''
    checking move
    '''        
    def getValidMoves(self):
        #need consider check
        i = 0

        print(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        for log in self.castleRightsLog:
            print(log.wks, log.wqs, log.bks, log.bqs, i)
            i+=1
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        #1. generate all possible move
        moves = self.getAllPossibleMoves()
        print(len(moves))
        print(self.whiteKingLocation[0], self.whiteKingLocation[1], self.blackKingLocation[0], self.blackKingLocation[1])
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        print(len(moves))
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
        # print(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        self.currentCastlingRight = tempCastleRights
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
        allyColor  = 'w' if self.whiteToMove else 'b'
        for i in range(8):
                endRow = r + kingMoves[i][0]
                endCol = c + kingMoves[i][1]
                if 0 <= endCol < 8 and 0 <= endRow < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

#        self.getCastleMoves(r, c, moves, allyColor)

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return

        #if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
        if (True):
            self.getKingsideCastleMoves(r, c, moves)
        
        #if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
        if (True):
            self.getQueensideCatleMoves(r, c, moves)
            
    def getKingsideCastleMoves(self, r, c, moves):
        print('king')
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c + 2 ):
                
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove = True))

    def getQueensideCatleMoves(self, r, c, moves):    
        if self.board[r][c-1] == '--' and self.board[r][c-2]  == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2 ) and not self.squareUnderAttack(r, c-3 ):
                print('queens')
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove = True))                              

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs