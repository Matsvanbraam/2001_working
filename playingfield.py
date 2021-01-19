import numpy as np
import pygame

class PlayingField():

    def __init__(self):
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7
        self.SQUARESIZE = 100
        self.RADIUS = int(self.SQUARESIZE / 2 - 5)

        self.width = self.COLUMN_COUNT * self.SQUARESIZE
        self.height = (self.ROW_COUNT + 1) * self.SQUARESIZE
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)

        self.board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))

        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)

    # Represent board by matrix, done by numpy
    def create_board(self):
        # Matrix of all 0's with 6 rows, 7 column
        return self.board

    #Print board upside down
    def print_board(self, board):
        self.draw_board(self.board)
        pygame.display.update()
        print(np.flip(board, 0))

    # Show board with pygame graphics
    def draw_board(self, board):
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
               # Draw elements of board with repeating pattern
               # Draw blue rectangles that fill the screen, except top row
               pygame.draw.rect(self.screen, self.BLUE, (c*self.SQUARESIZE, r*self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
               # Draw black circles inside these rectangles to represent an open place
               pygame.draw.circle(self.screen, self.BLACK, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int(r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)

        # Draw active pieces, Red for Player and Yellow for AI
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(self.screen, self.RED, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(self.screen, self.YELLOW, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
