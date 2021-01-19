import pygame
import sys

from keyboard_handler import KeyboardHandler
from playingfield import PlayingField
from gamecontrols import GameControls

class Game:

    def __init__(self):
        pygame.init()

        # reference classes
        self.playingfield = PlayingField()
        self.gamecontrols = GameControls(0,0,0)

        # size of screen and board
        self.ROW_COUNT = self.playingfield.ROW_COUNT
        self.COLUMN_COUNT = self.playingfield.COLUMN_COUNT
        self.SQUARESIZE = self.playingfield.SQUARESIZE
        self.screen = self.playingfield.screen
        self.board = self.playingfield.board

        # keyboard handler
        self.keyboard_handler = KeyboardHandler()
        # font

        # time
        self.time = pygame.time.get_ticks()

    def game_loop(self):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.time
        self.time = current_time
        self.handle_events()
        self.update_game(delta_time)
        self.draw_components()

    def update_game(self, dt):
        #Main game game_loop
        self.gamecontrols.player_actions()

    def draw_components(self):
        #background draw once
        #create board
        pass


    def reset(self):
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            if event.type == pygame.KEYUP:
                self.handle_key_up(event)
            if event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_pressed(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_released(event)

    def handle_key_down(self, event):
        self.keyboard_handler.key_pressed(event.key)

    def handle_key_up(self, event):
        self.keyboard_handler.key_released(event.key)

    def handle_mouse_motion(self, event):
        pass

    def handle_mouse_pressed(self, event):
        pass

    def handle_mouse_released(self, event):
        pass


if __name__ == "__main__":
    game = Game()
    while True:
        game.game_loop()