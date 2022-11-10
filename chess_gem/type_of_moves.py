from chess_gem.Move import Move
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