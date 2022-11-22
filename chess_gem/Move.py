class Move():
    #map keys to values
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board, is_enpassant_move = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        
        if (self.pieceMoved == 'wp' and self.endRow == 0) or ( self.pieceMoved == 'bp' and self.endRow == 7) :
            self.isPawnPromotion = True

        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"


        self.isCastleMove = isCastleMove
        self.isCaptured = self.pieceCaptured != "--"
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