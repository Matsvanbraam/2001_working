import random
import pygame
import sys
import math
from playingfield import PlayingField


class GameControls:

    def __init__(self, row, col, piece):
        self.game_over = False
        self.PLAYER = 0
        self.AI = 1
        # Randomize turn between Player and AI
        self.turn = random.randint(self.PLAYER, self.AI)
        self.WIN_TEXT = (255, 255, 255)

        self.playingfield = PlayingField()
        self.board = self.playingfield.board
        self.ROW_COUNT = self.playingfield.ROW_COUNT
        self.COLUMN_COUNT = self.playingfield.COLUMN_COUNT
        self.SQUARESIZE = self.playingfield.SQUARESIZE
        self.screen = self.playingfield.screen

        self.row = row
        self.col = col
        self.piece = piece
        self.font = pygame.font.SysFont(pygame.font.get_fonts()[0], 64)


    def player_actions(self):
        self.playingfield.print_board(self.board)
        while not self.game_over:
            # pygame library checks is any input is given
            for event in pygame.event.get():
                # Close game when needed
                if event.type == pygame.QUIT:
                    sys.exit()

                # Check is there is mousebutton down input (AUDIO LATER ADDED)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.turn == self.PLAYER:
                        posx = event.pos[0]
                        col = int(math.floor(posx/self.SQUARESIZE))

                        if self.is_valid_location(self.board, col):
                            row = self.get_next_open_row(self.board, col)
                            self.drop_piece(self.board, row, col, 1)

                            if self.winning_move(self.board, 1):
                                label = self.font.render("PLAYER WINS!", 1, self.WIN_TEXT)
                                # Updates that specific part of the screen
                                self.screen.blit(label, (40, 10))
                                self.game_over = True

                            # Switch turns in case of a valid location by taking remainder of variable turn and see if they are even or uneven
                            self.turn += 1
                            self.turn = self.turn % 2

                            self.playingfield.print_board(self.board)

            if self.turn == self.AI and not self.game_over:
                # posx = event.pos[0]
                # col = int(math.floor(posx/self.SQUARESIZE))
                col = random.randint(0, self.COLUMN_COUNT-1)

                if self.is_valid_location(self.board, col):
                    pygame.time.wait(500)
                    row = self.get_next_open_row(self.board, col)
                    self.drop_piece(self.board, row, col, 2)

                    if self.winning_move(self.board, 2):
                        label = self.font.render("AI WINS!", 2, self.WIN_TEXT)
                        # Updates that specific part of the screen
                        self.screen.blit(label, (40, 10))
                        self.game_over = True

                    # Switch turns in case of a valid location by taking remainder of variable turn and see if they are even or uneven
                    self.turn += 1
                    self.turn = self.turn % 2

                    self.playingfield.print_board(self.board)

            # Wait for 3 seconds to create delay when winning
            if self.game_over:
                pygame.time.wait(3000)
                sys.exit()
                # pass

    # Make column choice drop a piece into board, from input to board
    def drop_piece(self, board, row, col, piece):
        # Fill in the piece in the chosen column in the first row that is empty
        self.board[row][col] = piece

    # Check if the number that is turned in is legal and has a valid location, see if the top row is not filled
    def is_valid_location(self, board, col):
        # If this is true, column has not been filled all the way, so a legal move
        return self.board[self.ROW_COUNT-1][col] == 0

    # See in which row of the chosen column the piece will fall
    def get_next_open_row(self, board, col):
        # Check which is first row that is empty and return that
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    # Check if we have won NOT MOST EFFICIENT CHECK IF CAN DO BETTER
    def winning_move(self, board, piece):
        # Check all horizontal locations for win
        # In last 3 columns you can not start a win so subtract them, all rows can work
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT):
                # Check if 4 pieces are next to each other, so win
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and self.board[r][c + 3] == piece:
                    return True

        # Check all vertical locations for win
        # In last 3 rows you can not start a win so subtract them, all columns can work
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT - 3):
                # Check if 4 pieces are next to each other, so win
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and self.board[r + 3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT - 3):
                # Check if 4 pieces are next to each other, so win
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][c + 2] == piece and self.board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(3, self.ROW_COUNT):
                # Check if 4 pieces are next to each other, so win
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][c + 2] == piece and self.board[r - 3][c + 3] == piece:
                    return True