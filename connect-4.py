import math
import random
import numpy as np
import pygame
import sys
import tkinter as tk
from tkinter import messagebox
import time
from graphviz import Digraph

# Defining Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255,255,255)

# Defining the game dimensions
ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4
EMPTY = 0
player_score=0
ai_score=0

def createBoard():
    newBoard = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return newBoard


def dropPiece(board, row, column, piece):
    board[row][column] = piece


def isLocationValid(board, column):
    # Checking if the last row in the selected column is filled
    return board[ROW_COUNT - 1][column] == 0


def getFreeRow(board, column):
    # Loop to check for the deepest free row in the selected column
    for r in range(ROW_COUNT):
        if board[r][column] == 0:
            return r


def printBoard(board):
    print(np.flip(board, 0))


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if isLocationValid(board, col):
            valid_locations.append(col)
    return valid_locations


#  heurisitic function
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    # winning move
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    # opponent has one move to win
    elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    elif window.count(opp_piece) == 4 :
        score -= 100
    return score


def score_position(board, piece):
    score = 0
    # center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    # center_count = center_array.count(piece)
    # score += center_count * 3
    # score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH - 1]
            score += evaluate_window(window, piece)

    # score vertical
    for c in range(COLUMN_COUNT):
        column_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = column_array[r:r + WINDOW_LENGTH - 1]
            score += evaluate_window(window, piece)

    # score positive diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # score negative diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def drawBoard(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()



def getTheTotalScore(board, piece):
    total_score=0
    # Check horizontal win
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            # Check if all consecutive cells in the row have the same value as 'piece'
            if all(board[row][col + i] == piece for i in range(4)):
                total_score+=1

    # Check vertical win
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT):
            # Check if all consecutive cells in the column have the same value as 'piece'
            if all(board[row + i][col] == piece for i in range(4)):
                total_score+=1

    # Check diagonal (right) win
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            # Check if all consecutive cells in the diagonal (right) have the same value as 'piece'
            if all(board[row + i][col + i] == piece for i in range(4)):
                total_score+=1

    # Check diagonal (left) win
    for row in range(ROW_COUNT - 3):
        for col in range(3, COLUMN_COUNT):
            # Check if all consecutive cells in the diagonal (left) have the same value as 'piece'
            if all(board[row + i][col - i] == piece for i in range(4)):
                total_score+=1
    return total_score



def check_if_terminal(board):
    if getTheTotalScore(board,PLAYER_PIECE) > player_score:
        return True
    if getTheTotalScore(board,AI_PIECE) > ai_score:
        return True
    if len(get_valid_locations(board)) == 0:
        return True


def minimax(board, depth, maxmizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = check_if_terminal(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if getTheTotalScore(board, AI_PIECE) > ai_score:
                return 1000000000000, None
            elif getTheTotalScore(board, PLAYER_PIECE) > player_score:
                return -1000000000000, None
            else:  # no more possible moves
                if getTheTotalScore(board, AI_PIECE) > getTheTotalScore(board, PLAYER_PIECE):
                    return 1000000000000, None
                elif getTheTotalScore(board, PLAYER_PIECE) > getTheTotalScore(board, AI_PIECE):
                    return -1000000000000, None
                else:
                    return 0, None
        else:  # depth is zero
            return score_position(board, AI_PIECE), None

    if maxmizingPlayer:  # if AI is the player
        # column=random.choice(valid_locations)
        value = -math.inf
        for col in valid_locations:
            row = getFreeRow(board, col)
            temp_board = board.copy()
            dropPiece(temp_board, row, col, AI_PIECE)
            new_score, last_col = minimax(temp_board, depth - 1, False)
            if new_score > value or (new_score == value and last_col == None):
                value = new_score
                column = col
        return value, column
    else:  # if human id the player
        # column=random.choice(valid_locations)
        value = math.inf
        for col in valid_locations:
            row = getFreeRow(board, col)
            temp_board = board.copy()
            dropPiece(temp_board, row, col, PLAYER_PIECE)
            new_score, _ = minimax(temp_board, depth - 1, True)
            if new_score < value:
                value = new_score
                column = col
        return value, column


def minimax_pruning(board, depth, alpha, beta, maxmizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = check_if_terminal(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if getTheTotalScore(board, AI_PIECE) > ai_score:
                return 1000000000000, None
            elif getTheTotalScore(board, PLAYER_PIECE) > player_score:
                return -1000000000000, None
            else:  # no more possible moves
                if getTheTotalScore(board, AI_PIECE) > getTheTotalScore(board, PLAYER_PIECE):
                    return 1000000000000, None
                elif getTheTotalScore(board, PLAYER_PIECE) > getTheTotalScore(board, AI_PIECE):
                    return -1000000000000, None
                else:
                    return 0, None
        else:  # depth is zero
            return score_position(board, AI_PIECE), None

    if maxmizingPlayer:  # if AI is the player
        column = random.choice(valid_locations)
        value = -math.inf
        for col in valid_locations:
            row = getFreeRow(board, col)
            temp_board = board.copy()
            dropPiece(temp_board, row, col, AI_PIECE)
            new_score, last_col = minimax_pruning(temp_board, depth - 1, alpha, beta, False)
            if new_score > value or (new_score == value and last_col == None):
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, column
    else:  # if human is the player
        column = random.choice(valid_locations)
        value = math.inf
        for col in valid_locations:
            row = getFreeRow(board, col)
            temp_board = board.copy()
            dropPiece(temp_board, row, col, PLAYER_PIECE)
            new_score, _ = minimax_pruning(temp_board, depth - 1, alpha, beta, True)
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, column

def get_time_taken(start_time):
    end_time = time.time()
    return round(end_time - start_time, 2)

# Function to start the game with user-input depth and player choice
def start_game():
    global depth_minimax
    global depth_pruning
    global turn

    try:
        depth_minimax = int(minimax_depth_entry.get())
        depth_pruning = int(pruning_depth_entry.get())
        player_choice = player_choice_var.get()  # Get the player's choice

        if player_choice == 0:  # Player vs. Player
            turn = 0
        else:  # Player vs. AI
            turn = 1

        root.destroy()  # Close the start window
    except ValueError:
        messagebox.showerror("Error", "Please enter valid depths.")

# Initialize Tkinter
root = tk.Tk()
root.title("Connect Four - Start Menu")

# Adjust window size and background
root.geometry("700x500")
root.configure(bg="#0077cc")

# Welcome label
welcome_label = tk.Label(root, text="Welcome to Connect Four!", font=("BoldenVandemo", 36, "bold"), fg="white", bg="#0077cc")
welcome_label.pack(pady=20)

# Player choice label
player_choice_label = tk.Label(root, text="Choose who starts:", font=("BoldenVandemo", 18), fg="white", bg="#0077cc")
player_choice_label.pack()

# Player choice radio buttons
player_choice_var = tk.IntVar()
player_choice_var.set(1)  # Default to Player vs. AI
player_choice_player = tk.Radiobutton(root, text="Player", variable=player_choice_var, value=0, font=("BoldenVandemo", 16), fg="white", bg="#0077cc", selectcolor="#0077cc")
player_choice_player.pack()
player_choice_ai = tk.Radiobutton(root, text="AI", variable=player_choice_var, value=1, font=("BoldenVandemo", 16), fg="white", bg="#0077cc", selectcolor="#0077cc")
player_choice_ai.pack()

# Minimax depth input
minimax_depth_label = tk.Label(root, text="Enter Minimax depth:", font=("BoldenVandemo", 18), fg="white", bg="#0077cc")
minimax_depth_label.pack()
minimax_depth_entry = tk.Entry(root, font=("Arial", 16))
minimax_depth_entry.pack()

# Minimax with pruning depth input
pruning_depth_label = tk.Label(root, text="Enter Minimax with pruning depth:", font=("BoldenVandemo", 18), fg="white", bg="#0077cc")
pruning_depth_label.pack()
pruning_depth_entry = tk.Entry(root, font=("Arial", 16))
pruning_depth_entry.pack()

# Start button
start_button = tk.Button(root, text="Start Game", command=start_game, font=("BoldenVandemo", 18, "bold"), bg="white")
start_button.pack(pady=20)

root.mainloop()

board = createBoard()
game_over = False

# Initialize Pygame
pygame.init()

SQUARE_SIZE = 100
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_SIZE / 2 - 5)
move_number = 1

screen = pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()


myfont = pygame.font.SysFont("BoldenVandemo", 75)


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            x_position = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (x_position, int(SQUARE_SIZE / 2)), RADIUS)

        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Ask for Player 1 Input
            if turn == PLAYER:
                x_position = event.pos[0]
                column = int(math.floor(x_position / SQUARE_SIZE))

                if isLocationValid(board, column):
                    row = getFreeRow(board, column)
                    dropPiece(board, row, column, PLAYER_PIECE)

                    if getTheTotalScore(board, PLAYER_PIECE) > player_score:
                        player_score = getTheTotalScore(board, PLAYER_PIECE) 
                        player_score_str=str(player_score)
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                        label = myfont.render("Player score =" + player_score_str, 1, WHITE)
                        screen.blit(label, (40, 10))

                    if(len(get_valid_locations(board)) == 0):
                        if(player_score>ai_score):
                            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                            label = myfont.render("Player wins! score:" + player_score_str, 1, WHITE)
                            screen.blit(label, (40, 10))   
                        elif(ai_score>player_score):
                            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                            label = myfont.render("Computer wins! score:" + ai_score_str, 1, WHITE)
                            screen.blit(label, (40, 10))   
                        else:
                            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                            label = myfont.render("It's a tie!", 1, WHITE)
                            screen.blit(label, (40, 10))                       

                        game_over = True
                    turn += 1
                    turn = turn % 2
                    # printBoard(board)
                    drawBoard(board)

            # Ask for Player 2 Input
    if turn == AI and not game_over:
        start_time = time.time()
        #choose the algorithm you want to use
        _,column= minimax_pruning(board, depth_pruning, -math.inf, math.inf, True)
        #_, column = minimax(board, depth_minimax, True)
        if isLocationValid(board, column):
            pygame.time.wait(500)
            row = getFreeRow(board, column)
            dropPiece(board, row, column, AI_PIECE)

            # Stop timer and get time taken
            time_taken = get_time_taken(start_time)
            print(f"Time taken by AI to make move {move_number} is {time_taken} in secs. (Using Minimax)")

            # Increment move number
            move_number += 1

            if getTheTotalScore(board, AI_PIECE) > ai_score:
                ai_score=getTheTotalScore(board, AI_PIECE)
                ai_score_str=str(ai_score)
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                label = myfont.render("Computer score =" + ai_score_str, 1, WHITE)
                screen.blit(label, (40, 10))
            if(len(get_valid_locations(board)) == 0):
                if(player_score>ai_score):
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                    label = myfont.render("Player wins! score:" + player_score_str, 1, WHITE)
                    screen.blit(label, (40, 10))   
                elif(ai_score>player_score):
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                    label = myfont.render("Computer wins! score: " + ai_score_str, 1, WHITE)
                    screen.blit(label, (40, 10))   
                else:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                    label = myfont.render("It's a tie!" , 1, WHITE)
                    screen.blit(label, (40, 10))                       

                game_over = True

            # printBoard(board)
            drawBoard(board)
            turn += 1
            turn = turn % 2

    if game_over is True:
        pygame.time.wait(5000)