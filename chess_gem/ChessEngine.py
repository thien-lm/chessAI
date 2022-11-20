#TODO: use numpy instead of list
import tkinter as tk
from tkinter import ttk
from logging import captureWarnings
from multiprocessing import RLock
from easygui import *
from chess import Board
from numpy import blackman
from chess_gem.Move import Move
import numpy as np

class GameState():
    def __init__(self):
        # represent a 8x8 chess Board
        # bR = black Rock
        # wR = white Rock
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])

        # self.board = [
        #     ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        #     ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--'],
        #     ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
        #     ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        # ]
        self.moveFunction = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'K': self.getKingMoves, 'Q': self.getQueenMoves}
        self.whiteToMove =  True
        self.moveLog = [] 
        self.DEPTH = 0
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.numberMove = 0
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
        # i = 0
        # print(i)
        # if move.isPawnPromotion and  move.pieceMoved == 'wp':
        #     choices = ['Q', 'B', 'N', 'R']
        #     output = choicebox('hi', 'thien dep trai vai dai', choices)
        #     self.board[move.endRow][move.endCol] = move.pieceMoved[0] + output
        #     i+=1
        # print(i)
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

    def setDepth(self):
        text = "Enter depth lv !!"
        
        # window title
        title = "thien dzai sieu cap vjppr0"
        
        # default text
        d_text = "3"
        
        # creating a enter box
        output = enterbox(text, title, d_text)
        
        # title for the message box
        title = "chose level"

        # creating a message
        self.DEPTH = int(output)


    ''' undo the lastMove'''  
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            #update king's locaiton
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
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
            self.checkMate = False
            self.staleMate = False

    def updateCastleRights(self, move):

        if move.pieceCaptured == "wR":
            if move.endCol == 0: #left rook
                self.currentCastlingRight.wqs = False
            elif move.endCol == 7: #right rook
                self.currentCastlingRight.wks = False
        elif move.pieceCaptured == "bR":
            if move.endCol == 0: #left rook
                self.currentCastlingRight.bqs = False
            elif move.endCol == 7: #right rook
                self.currentCastlingRight.bks = False

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

        # print(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        # for log in self.castleRightsLog:
        #     print(log.wks, log.wqs, log.bks, log.bqs, i)
        #     i+=1
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        moves = []
        self.in_Check, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.whiteToMove: 
            king_row = self.whiteKingLocation[0]
            king_col = self.whiteKingLocation[1]
        else:
            king_row = self.blackKingLocation[0]
            king_col = self.blackKingLocation[1]

        if self.in_Check:
            if len(self.checks) == 1: #only 1 check, block the check or move the king
                moves = self.getAllPossibleMoves()
                #to block the check you must put a piece into one of the squares between the enemy piece and your king
                check = self.checks[0] #check information
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = [] #squares that pieces can move to
                #if knight, must capture the knight or move your king, other pieces can be blocked
                if piece_checking[1] == "N":
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i) #check[2] and check[3] are the check directions
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col: #once you get to piece and check
                            break
                #get rid of any moves that don't block check or move king
                for i in range(len(moves)-1, -1, -1): #iterate through the list backwards when removing elements
                    if moves[i].pieceMoved[1] != "K": #move doesn't move king so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in valid_squares: #move doesn't block or capture piece
                            moves.remove(moves[i])
            else: #double check, king has to move
                self.getKingMoves(king_row, king_col, moves)
        else: #not in check - all moves are fine
            moves = self.getAllPossibleMoves()  
            if self.whiteToMove:
                self.getCastleMoves(7, 4, moves)
            else:
                self.getCastleMoves(0, 4, moves)

        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
            
        return moves









        # tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        # #1. generate all possible move
        # moves = self.getAllPossibleMoves()
        # # print(len(moves))
        # # print(self.whiteKingLocation[0], self.whiteKingLocation[1], self.blackKingLocation[0], self.blackKingLocation[1])
        # if self.whiteToMove:
        #     self.getCastleMoves(7, 4, moves)
        # else:
        #     self.getCastleMoves(0, 4, moves)

        # #print(len(moves))
        # #2 make move for each move
        # for i in range(len(moves) - 1, -1, -1):
        #     self.makeMove(moves[i])
        # #3 generate all opponet's move

        # #4 for each opponent move, check if they attack your king
        #     self.whiteToMove = not self.whiteToMove
        #     if self.inCheck():
        #         moves.remove(moves[i])

        # #5 if they do attack your king, not a valid move
        #     self.whiteToMove = not self.whiteToMove
        #     self.undoMove()
            
        
        # if len(moves) == 0:
        #     #print('winner appeared')
        #     #print(self.numberMove)
        #     if self.inCheck():
        #         self.checkMate = True
        #     else:
        #         self.staleMate = True
        # else:
        #     self.checkMate = False
        #     self.staleMate = False
        # # print(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        # self.currentCastlingRight = tempCastleRights
        # return moves
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


    def checkForPinsAndChecks(self) :
        pins = []
        checks = []
        in_Check = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions= ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1] *i
                if 0  <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1]) 
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]

                        if(0 <= j <= 3 and type == 'R') or \
                            (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                    (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():
                                in_Check = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else: break
        knightMoves = ((-1, 2), (-1, -2), (1, 2), (1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor  and endPiece[1] == 'N':
                    in_Check = True
                    checks.append((endRow, endCol, m[0], m[1]))
            return in_Check, pins, checks


    '''get all pawn move'''
    def getPawnMoves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove: #white pawn moves
            if self.board[row-1][col] == "--": #1 square pawn advance
                #moves.append(Move((row, col), (row-1, col), self.board)) #(start square, end square, board)
                # if row == 6 and self.board[row-2][col] == "--": #2 square pawn advance
                #     moves.append(Move((row, col), (row-2, col), self.board))
                if not piece_pinned or pin_direction == (-1, 0):
                    moves.append(Move((row, col), (row-1, col), self.board)) #(start square, end square, board)
                    if row == 6 and self.board[row-2][col] == "--": #2 square pawn advance
                        moves.append(Move((row, col), (row-2, col), self.board))


            if col - 1 >= 0: #capturing to the left - impossible if a pawn is standing in a far left column
                if self.board[row-1][col-1][0] == "b": #enemy piece to capture
                    #moves.append(Move((row, col), (row-1, col-1), self.board))
                    if not piece_pinned or pin_direction == (-1, -1):
                        moves.append(Move((row, col), (row-1, col-1), self.board))

            if col + 1 <= 7: #capturing to the right - analogical
                if self.board[row-1][col+1][0] == "b": #enemy piece to capture
                    #moves.append(Move((row, col), (row-1, col+1), self.board))
        #if not self.white_to_move: #black pawn moves
                    if not piece_pinned or pin_direction == (-1, 1):
                        moves.append(Move((row, col), (row-1, col+1), self.board))

        else: #black pawn moves
            if self.board[row+1][col] == "--": #1 suare pawn advance
                moves.append(Move((row, col), (row+1, col), self.board))
                #if row == 1 and self.board[row+2][col] == "--":
                #    moves.append(Move((row ,col), (row+2, col), self.board))
                if not piece_pinned or pin_direction == (1, 0):
                    moves.append(Move((row, col), (row+1, col), self.board))
                    if row == 1 and self.board[row+2][col] == "--":
                        moves.append(Move((row ,col), (row+2, col), self.board))

            if col - 1 >= 0:
                if self.board[row+1][col-1][0] == "w":
                #    moves.append(Move((row, col), (row+1, col-1), self.board))
                    if not piece_pinned or pin_direction == (1, -1):
                        moves.append(Move((row, col), (row+1, col-1), self.board))

            if col + 1 <= 7:
                if self.board[row+1][col+1][0] == "w":
                #    moves.append(Move((row, col), (row+1, col+1), self.board))
                    if not piece_pinned or pin_direction == (1, 1):
                        moves.append(Move((row, col), (row+1, col+1), self.board))



    def getRookMoves(self, row, col, moves):

        '''
        Get all the rook moves for the rook located at row, col and add the moves to the list.
        '''
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != "Q": #can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up, left, down, right
        enemy_color = "b" if self.whiteToMove else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7: #check for possible moves only in boundries of the board
                    # end_piece = self.board[end_row][end_col]
                    # if end_piece == "--": #empty space is valid
                    #     moves.append(Move((row, col), (end_row, end_col), self.board))
                    # elif end_piece[0] == enemy_color: #capture enemy piece
                    #     moves.append(Move((row, col), (end_row, end_col), self.board))
                    #     break
                    # else: #friendly piece
                    #     break
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--": #empty space is valid
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color: #capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else: #friendly piece
                            break
                else: #off board
                    break           


    def getKnightMoves(self, row, col, moves):
        piece_pinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2)) #up/left up/right right/up right/down down/left down/right left/up left/down
        ally_color = "w" if self.whiteToMove else "b"
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                # end_piece = self.board[end_row][end_col]
                # if end_piece[0] != ally_color: #so it's either enemy piece or empty equare 
                #     moves.append(Move((row, col), (end_row, end_col), self.board))
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color: #so it's either enemy piece or empty equare 
                        moves.append(Move((row, col), (end_row, end_col), self.board))
    
    def getBishopMoves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1)) #digaonals: up/left up/right down/right down/left
        enemy_color = "b" if self.whiteToMove else "w"    
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7: #check if the move is on board
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--": #empty space is valid
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color: #capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else: #friendly piece
                            break
                else: #off board
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

    
    def getKingMoves(self, row, col, moves):
        # king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.whiteToMove else "b"
        # for move in king_moves:
        #     end_row = row + move[0]
        #     end_col = col + move[1]
        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                # if end_piece[0] != ally_color:
                #     moves.append(Move((row, col), (end_row, end_col), self.board))


                if end_piece[0] != ally_color: #not an ally piece - empty or enemy
                    #place king on end square and check for checks
                    if ally_color == "w":
                        self.whiteKingLocation = (end_row, end_col)
                    else:
                        self.blackKingLocation = (end_row, end_col)
                    in_check, pins, checks = self.checkForPinsAndChecks()
                    if not in_check:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    # place king back on original location
                    if ally_color == "w":
                        self.whiteKingLocation = (row, col)
                    else:
                        self.blackKingLocation = (row, col)

#        self.getCastleMoves(r, c, moves, allyColor)

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return

        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
        #if (True):
            self.getKingsideCastleMoves(r, c, moves)
        
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
        #if (True):
            self.getQueensideCatleMoves(r, c, moves)
            
    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c + 2 ):
                
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove = True))

    def getQueensideCatleMoves(self, r, c, moves):    
        if self.board[r][c-1] == '--' and self.board[r][c-2]  == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2 ) and not self.squareUnderAttack(r, c-3 ):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove = True))                              

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs