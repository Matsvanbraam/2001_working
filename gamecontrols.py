# Project by Mats van Braam and Laura Schep

import random
import pygame
import sys
import math
from playingfield import PlayingField
from voicecontrols import VoiceControls


class GameControls:

    def __init__(self, row, col, piece):

        self.game_over = False
        self.PLAYER = 0
        self.AI = 1
        self.PLAYER_PIECE = 1
        self.AI_PIECE = 2
        self.EMPTY = 0

        self.turn = 0

        self.WIN_TEXT = (255, 255, 255)
        self.WINDOW_LENGTH = 4

        self.playingfield = PlayingField()
        self.board = self.playingfield.board
        self.ROW_COUNT = self.playingfield.ROW_COUNT
        self.COLUMN_COUNT = self.playingfield.COLUMN_COUNT
        self.SQUARESIZE = self.playingfield.SQUARESIZE
        self.screen = self.playingfield.screen

        self.voicecontrols = VoiceControls()

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
                        # Uncomment these two comments, to click in order to place a piece instead of voice
                        posx = event.pos[0]
                        col = int(math.floor(posx / self.SQUARESIZE))
                        # Comment this comment, to click in order to place a piece instead of voice
                        # col = self.voicecontrols.listening()

                        if self.is_valid_location(self.board, col):
                            row = self.get_next_open_row(self.board, col)
                            self.drop_piece(self.board, row, col, self.PLAYER_PIECE)

                            if self.winning_move(self.board, self.PLAYER_PIECE):
                                label = self.font.render("PLAYER WINS!", 1, self.WIN_TEXT)
                                # Updates that specific part of the screen
                                self.screen.blit(label, (40, 10))
                                self.game_over = True

                            self.playingfield.print_board(self.board)

                            # Switch turns in case of a valid location by taking remainder of variable turn and see if they are even or uneven
                            self.turn += 1
                            self.turn = self.turn % 2

                            # print(self.turn)

            if self.turn == self.AI and not self.game_over:
                # posx = event.pos[0]
                # col = int(math.floor(posx/self.SQUARESIZE))
                # col = random.randint(0,self.COLUMN_COUNT-1)
                col, minimax_score = self.minimax(self.board, 3, True)

                # print(col)
                # print(self.turn)

                if self.is_valid_location(self.board, col):
                    pygame.time.wait(500)
                    row = self.get_next_open_row(self.board, col)
                    self.drop_piece(self.board, row, col, self.AI_PIECE)

                    if self.winning_move(self.board, self.AI_PIECE):
                        label = self.font.render("AI WINS!", 2, self.WIN_TEXT)
                        # Updates that specific part of the screen
                        self.screen.blit(label, (40, 10))
                        self.game_over = True

                    self.playingfield.print_board(self.board)

                    # Switch turns in case of a valid location by taking remainder of variable turn and see if they are even or uneven
                    self.turn += 1
                    self.turn = self.turn % 2

                    # print(self.turn)

            # Wait for 3 seconds to create delay when winning
            if self.game_over:
                pygame.time.wait(3000)
                sys.exit()
                # pass

    # Make column choice drop a piece into board, from input to board
    def drop_piece(self, board, row, col, piece):
        # Fill in the piece in the chosen column in the first row that is empty
        board[row][col] = piece

    # Check if the number that is turned in is legal and has a valid location, see if the top row is not filled
    def is_valid_location(self, board, col):
        # If this is true, column has not been filled all the way, so a legal move
        return board[self.ROW_COUNT - 1][col] == 0

    # See in which row of the chosen column the piece will fall
    def get_next_open_row(self, board, col):
        # Check which is first row that is empty and return that
        for r in range(self.ROW_COUNT):
            if board[r][col] == 0:
                return r

    # Check if we have won NOT MOST EFFICIENT CHECK IF CAN DO BETTER
    def winning_move(self, board, piece):
        # Check all horizontal locations for win
        # In last 3 columns you can not start a win so subtract them, all rows can work
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT):
                # Check if 4 pieces are next to each other, so win
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                    return True

        # Check all vertical locations for win
        # In last 3 rows you can not start a win so subtract them, all columns can work
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT - 3):
                # Check if 4 pieces are next to each other, so win
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT - 3):
                # Check if 4 pieces are next to each other, so win
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(3, self.ROW_COUNT):
                # Check if 4 pieces are next to each other, so win
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                    return True

    #Create a score value for a specific board situation
    def evaluate_window(self, window, piece):
        score = 0

        # Set correct opponent
        opp_piece = self.PLAYER_PIECE
        if piece == self.PLAYER_PIECE:
            opp_piece = self.AI_PIECE

        # Scores for current player
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
            score += 2

        # Scores for opponent
        if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
            score -= 4
        return score

    def score_position(self, board, piece):
        score = 0

        # Score center column
        center_array = [int(i) for i in list(board[:, self.COLUMN_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score horizontal
        # In a specific row, check all column positions
        for r in range(self.ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.COLUMN_COUNT - 3):
                window = row_array[c:c + self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)
        # Score vertical
        # In a specific column, check all row positions
        for c in range(self.COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.ROW_COUNT - 3):
                window = col_array[r:r + self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)
        # Score positively sloped diagonals
        # In a specific (r,c) coordinate, check the (r+i,c+i) positions for i is within the window length
        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)
        # Score negatively sloped diagonals
        # In a specific (r,c) coordinate, check the (r+3-1,c+i) positions for i is within the window length
        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)
        return score

    # Terminal node if someone has won or if there are no valid locations left
    def is_terminal_node(self, board):
        return self.winning_move(board, self.PLAYER_PIECE) or self.winning_move(board, self.AI_PIECE) or len(self.get_valid_locations(board)) == 0

    def minimax(self, board, depth, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            # Check why situation is terminal and return corresponding score
            # You return (None, score), because you always should return a column and a value within this function
            # Since we don't know the column that makes the situation terminal, we return None
            if is_terminal:
                if self.winning_move(board, self.AI_PIECE):
                    return (None, 100000000000)
                elif self.winning_move(board, self.PLAYER_PIECE):
                    return (None, -100000000000)
                # There are no more valid moves
                else:
                    return (None, 0)
            # Depth = 0
            else:
                return (None, self.score_position(board, self.AI_PIECE))

            # Maximizingplayer's turn, so AI's turn
        if maximizingPlayer:
            value = -math.inf
            # Pick a random column that is valid
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.AI_PIECE)
                # Look for max value within the board at a certain depth and switch to min
                new_score = self.minimax(b_copy, depth - 1, False)[1]
                # If that calculated score is > value, use that column
                if new_score > value:
                    value = new_score
                    column = col
            return column, value

            # Minimizingplayer's turn, so Player's turn
        else:
            value = math.inf
            # Pick a random column that is valid
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.PLAYER_PIECE)
                # Look for min value within the board at a certain depth and switch to min
                new_score = self.minimax(b_copy, depth - 1, True)[1]
                # If that calculated score is < value, use that column
                if new_score < value:
                    value = new_score
                    column = col
            return column, value

    # Create a list of all columns you can drop a piece in
    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if self.is_valid_location(board, col):
                # Add valid columns to the list
                valid_locations.append(col)
        return valid_locations
