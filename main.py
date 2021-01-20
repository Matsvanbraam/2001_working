# Project by Mats van Braam and Laura Schep
# 19/01/2021

# This program contains a fun connect 4 against a minimax algorithm that is controlled by your voice.
# When it's your turn, click on the screen once and speak clearly.
# The console will tell you if it doesn't understand you properly.

# Videos that were used as a basis are by Keith Galli

# We are aware that the program does not fully work.
# We have a version that does work, however everything is in one class.
# When creating these classes everything went great, until we implemented the minimax.
# We do not know how to solve this and hope it can be resolved during the oral exam.

import pygame
import sys

from keyboard_handler import KeyboardHandler
#from playingfield import PlayingField
from gamecontrols import GameControls

class Game:

    def __init__(self):
        pygame.init()

        # reference classes
        # self.playingfield = PlayingField()
        self.gamecontrols = GameControls(0,0,0)

        # size of screen and board
        # self.screen = self.playingfield.screen
        # self.board = self.playingfield.board

        # keyboard handler
        self.keyboard_handler = KeyboardHandler()
        self.time = pygame.time.get_ticks()

    def game_loop(self):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.time
        self.time = current_time
        self.handle_events()
        self.update_game(delta_time)
        self.draw_components()

    def update_game(self, dt):
        #Execute the gamecontrols
        self.gamecontrols.player_actions()

    def draw_components(self):
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