import pygame
import random, sys


WIDTH = 800
HEIGHT = 800
FPS = 30
TILESIZE = 10
TILWEIDTH = WIDTH //TILESIZE
TILEHEIGHT = HEIGHT //TILESIZE

PREVARRAY = []
for i in range(TILWEIDTH):
    ROW = []
    for j in range(TILEHEIGHT):
        ROW.append(0)
    PREVARRAY.append(ROW)

# define a few useful color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

pygame.init() #initialize pygame

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

# rules
# Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overpopulation.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

class Board:
    def __init__(self, screen):
        self.screen = screen

    def drawGrid(self):
        for i in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, GRAY, (i, 0), (i, HEIGHT))

        for j in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, GRAY, (0, j), (WIDTH, j))

    def draw(self, pos, color):
        pygame.draw.rect(self.screen, color, (pos[0] * TILESIZE, pos[1] * TILESIZE, TILESIZE, TILESIZE))


def getNeighbor(PREVARRAY, col, row):
    neighbor = 0
    if PREVARRAY[(col -1) % TILEHEIGHT][(row - 1) % TILWEIDTH] == 1:
        neighbor += 1
    if PREVARRAY[(col -1) % TILEHEIGHT][row % TILWEIDTH] == 1:
        neighbor += 1
    if PREVARRAY[(col -1) % TILEHEIGHT][(row + 1) % TILWEIDTH] == 1:
        neighbor += 1
    if PREVARRAY[col % TILEHEIGHT][(row - 1) % TILWEIDTH] == 1:
        neighbor += 1
    if PREVARRAY[col % TILEHEIGHT][(row + 1) % TILWEIDTH] == 1:
        neighbor += 1
    if PREVARRAY[(col +1) % TILEHEIGHT][(row - 1) % TILWEIDTH] == 1:
        neighbor += 1
    if PREVARRAY[(col +1) % TILEHEIGHT][row % TILWEIDTH] == 1:
        neighbor += 1
    if PREVARRAY[(col +1) % TILEHEIGHT][(row + 1) % TILWEIDTH] == 1:
        neighbor += 1
    return neighbor


#  (random.randrange(255),random.randrange(255),random.randrange(255))
def start(PREVARRAY):
    running = True
    while running:
        screen.fill(BLACK)
        board = Board(screen)
        board.drawGrid()
        clock.tick(FPS)

        #  draw the live cell
        for col in range(len(PREVARRAY)):
            for row in range(len(PREVARRAY[col])):
                if PREVARRAY[col][row] == 1:
                    pygame.draw.rect(screen,WHITE, (row*TILESIZE, col*TILESIZE, TILESIZE, TILESIZE))

        NEWARRAY = []
        for i in range(TILWEIDTH):
            ROW = []
            for j in range(TILEHEIGHT):
                ROW.append(0)
            NEWARRAY.append(ROW)

        # change the cells
        for col in range(len(PREVARRAY)):
            for row in range(len(PREVARRAY[col])):
                state = PREVARRAY[col][row]
                neighbor = getNeighbor(PREVARRAY, col, row)
                if state == 0 and neighbor == 3:
                    NEWARRAY[col][row] = 1
                elif state == 1 and (neighbor < 2 or neighbor > 3):
                    NEWARRAY[col][row] = 0
                else:
                    NEWARRAY[col][row] = state

        for event in pygame.event.get():
            # check for closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    	# updating the window
        PREVARRAY = NEWARRAY

        pygame.display.flip()

    pygame.quit()


def main():
    running = True
    while running:
        board = Board(screen)
        board.drawGrid()

        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            # check for closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start(PREVARRAY)
                    running = False

        if click[0]:
            pos = (mouse_pos[0]//TILESIZE, mouse_pos[1]//TILESIZE)
            # save the status of the board in array
            PREVARRAY[pos[1]][pos[0]] = 1
            board.draw(pos, WHITE)
        if click[2]:
            pos = (mouse_pos[0]//TILESIZE, mouse_pos[1]//TILESIZE)
            # save the status of the board in array
            PREVARRAY[pos[1]][pos[0]] = 0
            board.draw(pos, BLACK)


    	# updating the window
        pygame.display.flip()

    pygame.quit()

main()
