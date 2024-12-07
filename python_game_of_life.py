#Python game of life - based on functions from lab1 jupyter notebook pum24

import random
import time
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--size", "-s", type=int, default=10, help="Size of the board")
parser.add_argument("--prob", "-p", type=float, default=0.2, help="Probability of a cell being alive")
parser.add_argument("--steps", "-n", type=int, default=20, help="Number of steps to run the simulation for")
args = parser.parse_args()


def get_empty_board(n): # return n x n table of dead cells (a list of lists)
    board = []
    for i in range(n):
        board.append([0]*n)
    return board

def print_board(grid): # print the table
    for row in range(len(grid)):
        str = ''
        for element in grid[row]:
            if element == len(grid[row])-1:
                print('\n')
            else:
                if element == 0:
                    str = str + ". "
                else:
                    str = str + "X "
        print(str)

def get_random_board(n, p): # return n x n table where each cell is alive with probability 0.2
    options = [1,0]
    board = []
    for row in range(n):
        row = []
        for element in range(n):
            row.append(random.choices(options,weights = [p,1-p])[0])
        board.append(row)
    return board

def add_glider(board): # return a board with a glider
    board[0][2] = board[1][0] = board[1][2] = board[2][1] = board[2][2] = 1
    return board

board = get_random_board(args.size,args.prob)
#glider_board = add_glider(board)

def count_live_neighbors(board, x, y): # return the number of live neighbors of cell x, y
    counter = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i >= 0 and y+j >= 0 and x+i+1 <= len(board) and y+j+1 <= len(board):
                if (i != 0 and j == 0) or (i != 0 and j != 0) or (i == 0 and j != 0):
                    if board[y+j][x+i] == 1:
                        counter += 1
    return counter


def step(board):  # return board at the next timestep
    blank_board = get_empty_board(len(board))
    for a in range(len(board)):
        for b in range(len(board)):
            if board[b][a] == 0 and count_live_neighbors(board, a, b) == 3:
                blank_board[b][a] = 1
            if board[b][a] == 1:
                if count_live_neighbors(board, a, b) == 2 or count_live_neighbors(board, a, b) == 3:
                    blank_board[b][a] = 1
                else:
                    blank_board[b][a] = 0

    return blank_board


for _ in range(args.steps):    # run for 20 steps
    os.system('cls')   # clear the output
    if _ == 0:
        print('Stan wyjściowy')
        print_board(board)  # print the board
        time.sleep(1)  # wait for half a second
        new_board = step(board)  # generate the next step
        board = new_board
    else:
        print(f'Step number {_}')
        print_board(board)          # print the board
        time.sleep(1)               # wait for half a second
        new_board = step(board)     # generate the next step
        board = new_board

