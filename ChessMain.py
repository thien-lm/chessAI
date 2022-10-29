import imp
from tkinter import TRUE
import pygame as p
from chess_gem import ChessEngine
import sys

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

def drawGameState(screen, gs):
    drawBoard(screen)#dRaw square
    #addin suggestion
    drawPieces(screen, gs.board)#draw pieces

def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]
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
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()

    validMoves = gs.getValidMoves()
    moveMade = False #flag when a move is made
    #print(gs.board) # this is a board representation
    loadImages()
    running = True

    sqSelected = () #no quare selected, keep track last  click
    playerClicks = [] # keep track player click
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                sys.exit()
            #mouse handler    
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()#mouse location(x,y)
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = () #click same square == undo action 
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: #after second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board) 
                    print(move.getChessNotation())
                    print(len(validMoves))
                    if move in validMoves:
                        gs.makeMove(move)
                        print('moved')
                        moveMade = True
                    sqSelected = () #reset user click
                    playerClicks = [] 

            #key Handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:#press z to undo
                    gs.undoMove()
                    print('undo')
                    moveMade = True
                    validMoves = gs.getValidMoves()
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False



        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()     


main()    
