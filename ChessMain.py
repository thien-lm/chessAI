import imp
from tkinter import TRUE
import pygame as p
from chess_gem import ChessEngine, SmartMoveFinder
import sys
from multiprocessing import Process, Queue
from easygui import *



WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 24
IMAGES = {}

#bug after video 03 : white space can kill a chess element

'''
init a global dict of image, will call one
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece +'.png'), (SQ_SIZE, SQ_SIZE))
   #acess image by images[piece]

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)#dRaw square
    #addin suggestion
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)#draw pieces


def drawBoard(screen):
    global colors
    colors = [p.Color('white'), p.Color('forestgreen')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[ ( (r+c) % 2 ) ]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r* SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):       
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r* SQ_SIZE, SQ_SIZE, SQ_SIZE)) 

def main():
    
    # creating a message
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    gs.setDepth()

    validMoves = gs.getValidMoves()
    global moveMade
    moveMade = False #flag when a move is made
    animate = False #flag when animate
    #print(gs.board) # this is a board representation
    loadImages()
    running = True

    numMove = 0

    sqSelected = () #no quare selected, keep track last  click
    playerClicks = [] # keep track player click
    gameOver = False
    playerOne = False#if a human is playing, human play white, AI playing = false
    playerTwo = False#same as above but for black
    AIThinking = False
    moveFinderProcess = None
    moveUndone = False

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or(not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                sys.exit()
            #mouse handler    
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()#mouse location(x,y)
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = () #click same square == undo action 
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2  and humanTurn: #after second click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board) 
                    #    print(move.getChessNotation())
                        print(len(validMoves))
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                print('Valid Move')
                                if(move.isCastleMove == True): print('this is a valid move')
                                moveMade = True
                                animate = True
                                sqSelected = () #reset user click
                                playerClicks = [] 
                        if not moveMade:
                            playerClicks = [sqSelected]

            #key Handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:#press z to undo
                    gs.undoMove()
                    #print('undo')
                    moveMade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True

                    #validMoves = gs.getValidMoves()
                if e.key == p.K_r:#reset game
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True

        #AI move Finder
        if not gameOver and not humanTurn and not moveUndone:
            if gs.whiteToMove:
                if not AIThinking:
                    AIThinking = True
                    #print('thinking')
                    returnQueue = Queue()
                    moveFinderProcess = Process(target=SmartMoveFinder.findBestMove, args = (gs, validMoves, gs.DEPTH, returnQueue))
                    moveFinderProcess.start()
                    # AIMove = SmartMoveFinder.findBestMove(gs, validMoves)
                if not moveFinderProcess.is_alive():
                    #print('done thinking')
                    AIMove = returnQueue.get()    
                    if AIMove is None:
                        AIMove = SmartMoveFinder.findRandomMove(validMoves)
                    gs.makeMove(AIMove)
                    numMove += 1
                    #print(AIMove.getChessNotation())
                    moveMade = True
                    animate = True
                    AIThinking = False
            else:
                AIMove = SmartMoveFinder.findGreedy(gs, validMoves)

                AIMove = None
                if AIMove is None:
                    AIMove = SmartMoveFinder.findRandomMove(validMoves)
                gs.makeMove(AIMove)
                numMove += 1
                print(AIMove.getChessNotation())
                moveMade = True
                animate = True


        if moveMade:
            if animate: 
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            moveUndone = False



        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            #print(numMove)
            if gs.whiteToMove:
                drawText(screen, "black wins by checkmate")
            else:
                drawText(screen, 'white wins by checkmate')
                # gs = ChessEngine.GameState()
                # validMoves = gs.getValidMoves
                sqSelected = ()
                playerClicks = []
                moveMade = False
                animate = False
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')
            #main()
        clock.tick(MAX_FPS)
        p.display.flip()     


    '''highlight square'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
                s = p.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100) #transparency value ->0 tranparent, 255: opaque
                s.fill(p.Color('blue'))
                screen.blit(s, (c * SQ_SIZE, r* SQ_SIZE))
                #hight lightmove from that square
                s.fill(p.Color('yellow'))
                for move in validMoves:
                    if(move.startRow == r and move.startCol == c):
                        screen.blit(s, (SQ_SIZE * move.endCol, SQ_SIZE * move.endRow))

def animateMove(move, screen, board, clock):
    global colors
    #coords = [] #list of coord that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 1#frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = ((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        #earse the piece moved form it ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rect
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont('Helvitca', 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))

# def setDepth():
#     text = "Enter depth lv !!"
    
#     # window title
#     title = "thien dzai sieu cap vjppr0"
    
#     # default text
#     d_text = "3"
    
#     # creating a enter box
#     output = enterbox(text, title, d_text)
    
#     # title for the message box
#     title = "chose level"
    
#     # creating a message
#     DEPTH = int(output)   
#     return DEPTH


    


if __name__ == "__main__":
    
    main()