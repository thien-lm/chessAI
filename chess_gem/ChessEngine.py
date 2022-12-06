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
        self.moveFunction = {  'N': self.getKnightMoves, 'R': self.getRookMoves,'Q': self.getQueenMoves, 'B': self.getBishopMoves,'p': self.getPawnMoves, 'K': self.getKingMoves }
        self.whiteToMove =  True
        self.moveLog = [] 
        self.DEPTH = 0
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.in_Check = False
        self.pins = []
        self.checks = []
        self.numberMove = 0
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
        self.enpassant_possible = ()  # coordinates for the square where en-passant capture is possible
        self.enpassant_possible_log = [self.enpassant_possible]

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move to display it later
        self.whiteToMove = not self.whiteToMove #switch turn
        # if(self.in_Check):
        #     print('check')
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved =='bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

                # enpassant move
        if move.is_enpassant_move:
            self.board[move.startRow][move.endCol] = "--"  # capturing the pawn

        # update enpassant_possible variable
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:  # only on 2 square pawn advance
            self.enpassant_possible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassant_possible = ()

        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'

            else:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol -2 ] = '--'


        self.enpassant_possible_log.append(self.enpassant_possible)

        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

        # if(move.isCaptureMove):
        #     print('this is a capture move')

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

            if move.is_enpassant_move:
                self.board[move.endRow][move.endCol] = "--"  # leave landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            self.enpassant_possible_log.pop()
            self.enpassant_possible = self.enpassant_possible_log[-1]

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
                self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
            else:
                self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        self.currentCastlingRight = tempCastleRights
        
        self.capturedMove = []
        self.nonCapturedMove = []
        for move in moves:
            if move.isCaptureMove:
                self.capturedMove.append(move) 
            else:
                self.nonCapturedMove.append(move)
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
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            direction = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + direction[0]*i
                endCol = startCol + direction[1] *i
                if 0  <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1]!='K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, direction[0], direction[1]) 
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        enemy_type = endPiece[1]

                        if(0 <= j <= 3 and enemy_type == 'R') or \
                            (4 <= j <= 7 and enemy_type == 'B') or \
                                (i == 1 and enemy_type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                    (enemy_type == 'Q') or (i == 1 and enemy_type == 'K'):
                            if possiblePin == ():
                                in_Check = True
                                checks.append((endRow, endCol, direction[0], direction[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else: 
                    break

        knightMoves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
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

        if self.whiteToMove:
            move_amount = -1
            start_row = 6
            enemy_color = "b"
            king_row, king_col = self.whiteKingLocation
        else:
            move_amount = 1
            start_row = 1
            enemy_color = "w"
            king_row, king_col = self.blackKingLocation

        if self.board[row + move_amount][col] == "--":  # 1 square pawn advance
            if not piece_pinned or pin_direction == (move_amount, 0):
                moves.append(Move((row, col), (row + move_amount, col), self.board))
                if row == start_row and self.board[row + 2 * move_amount][col] == "--":  # 2 square pawn advance
                    moves.append(Move((row, col), (row + 2 * move_amount, col), self.board))
        if col - 1 >= 0:  # capture to the left
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[row + move_amount][col - 1][0] == enemy_color:
                    moves.append(Move((row, col), (row + move_amount, col - 1), self.board))
                if (row + move_amount, col - 1) == self.enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:  # king is left of the pawn
                            # inside: between king and the pawn;
                            # outside: between pawn and border;
                            inside_range = range(king_col + 1, col - 1)
                            outside_range = range(col + 1, 8)
                        else:  # king right of the pawn
                            inside_range = range(king_col - 1, col, -1)
                            outside_range = range(col - 2, -1, -1)
                        for i in inside_range:
                            if self.board[row][i] != "--":  # some piece beside en-passant pawn blocks
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[row][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((row, col), (row + move_amount, col - 1), self.board, is_enpassant_move=True))
        if col + 1 <= 7:  # capture to the right
            if not piece_pinned or pin_direction == (move_amount, +1):
                if self.board[row + move_amount][col + 1][0] == enemy_color:
                    moves.append(Move((row, col), (row + move_amount, col + 1), self.board))
                if (row + move_amount, col + 1) == self.enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:  # king is left of the pawn
                            # inside: between king and the pawn;
                            # outside: between pawn and border;
                            inside_range = range(king_col + 1, col)
                            outside_range = range(col + 2, 8)
                        else:  # king right of the pawn
                            inside_range = range(king_col - 1, col + 1, -1)
                            outside_range = range(col - 1, -1, -1)
                        for i in inside_range:
                            if self.board[row][i] != "--":  # some piece beside en-passant pawn blocks
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[row][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((row, col), (row + move_amount, col + 1), self.board, is_enpassant_move=True))

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
        """
        Get all the king moves for the king located at row col and add the moves to the list.
        """
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.whiteToMove else "b"
        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # not an ally piece - empty or enemy
                    # place king on end square and check for checks
                    if ally_color == "w":
                        self.whiteKingLocation = (end_row, end_col)
                    else:
                        self.blackKingLocation = (end_row, end_col)
                    in_Check, pins, checks = self.checkForPinsAndChecks()
                    if not in_Check:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    # place king back on original location
                    if ally_color == "w":
                        self.whiteKingLocation = (row, col)
                    else:
                        self.blackKingLocation = (row, col)

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
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2 ):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove = True))                              

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs