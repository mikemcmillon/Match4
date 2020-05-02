import os
import pygame
import math
import time

# Set my basic colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Initialize pygame
HEIGHT = 700
WIDTH = 700
ROWS = 6
COLS = 7
SQUARE = 100
RADIUS = SQUARE//2 - 5
FPS = 30  # Frames per second
pygame.init()  # Turns on pygame
pygame.font.init() # Allows us to set a font type for words on the screen
pygame.mixer.init()  # Turns on sound in pygame
font = pygame.font.SysFont('Times New Roman', 30)
icon = pygame.image.load(os.path.join('images', 'letter-m.png'))
pygame.display.set_icon(icon)
os.environ['SDL_VIDEO_WINDOW_POS'] = '400,200'   # Sets where your game window appears on the screen
window = pygame.display.set_mode((WIDTH, HEIGHT))
window.fill(BLACK)
pygame.display.set_caption('Match Four')
CLOCK = pygame.time.Clock()

board = []
def set_board():
    global board
    board = []
    for r in range(ROWS):
        board.append([])
        for c in range(COLS):
            board[r].append(0)

def draw_board():
    pygame.draw.rect(window, BLUE, (0, 100, WIDTH, HEIGHT-100))
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == 0:
                pygame.draw.circle(window, BLACK, (c * SQUARE + SQUARE//2, (ROWS-r) * SQUARE + SQUARE//2), RADIUS)
            elif board[r][c] == 1:
                pygame.draw.circle(window, RED, (c * SQUARE + SQUARE// 2, (ROWS-r) * SQUARE + SQUARE// 2), RADIUS)
            else:
                pygame.draw.circle(window, YELLOW, (c * SQUARE + SQUARE// 2, (ROWS-r) * SQUARE + SQUARE// 2), RADIUS)
    pygame.display.update()

def winner():
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if (board[r][c] != 0) and (board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3]):
                return True
    # Check vertical
    for r in range(ROWS-3):
        for c in range(COLS):
            if (board[r][c] != 0) and (board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c]):
                return True
    # Check positive slope
    for r in range(ROWS - 3):
        for c in range(COLS-3):
            if (board[r][c] != 0) and (board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3]):
                return True
    # Check negative slope
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if (board[r][c] != 0) and (board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3]):
                return True

playing = True
turn = 0
set_board()
draw_board()
while playing:
    CLOCK.tick(FPS)

    if winner():
        pygame.draw.rect(window, BLACK, (0, 0, WIDTH, SQUARE))
        text = font.render("WINNER!!! Click to Continue", True, WHITE)
        text_rect = text.get_rect(midtop=(WIDTH // 2, 15))
        window.blit(text, text_rect)
        pygame.display.update()
        play_again = False
        while not play_again:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    play_again = True
                    set_board()
                    break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(window, BLACK, (0,0, WIDTH, SQUARE))
            x_pos = event.pos[0]
            if turn == 0:
                pygame.draw.circle(window, RED, (x_pos, SQUARE // 2), RADIUS)
            else:
                pygame.draw.circle(window, YELLOW, (x_pos, SQUARE // 2), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x_pos = math.floor(event.pos[0]/100)
            for r in range(ROWS):
                if board[r][x_pos] == 0:
                    board[r][x_pos] = turn+1
                    turn = (turn + 1) % 2
                    break

    draw_board()