# -*- coding: utf-8 -*-
"""
Created on Sun May 15 10:57:40 2022

@author: Daniel Flynn
"""
import pygame

from game import SpaceRocks
from pygame import Color
from utils import load_sprite, print_menu_text

class MainMenu:
    START_IDX = 0
    QUIT_IDX = 1
    
    def __init__(self):
        self.space_rocks = SpaceRocks()
        self.screen = pygame.display.set_mode((self.space_rocks.SCREEN_WIDTH, self.space_rocks.SCREEN_HEIGHT))
        self.background = load_sprite("space", False)
        self.title_font = pygame.font.Font(None, 64)
        self.menu_font = pygame.font.Font(None, 32)
    # Have game name, selection at start.
        self.menu_idx = 0
        self.menu = ["start", "quit"]
        self.title = "Pysteroids"
    # Have background music
    
    def main_loop(self):
        while True:
            self.menu_selection(self.menu)
            self.menu_view(self.menu)
            
    
    # Menu selection to start or end game
    def menu_selection(self, menu):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.menu_idx == self.QUIT_IDX
            )):
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.menu_idx == self.START_IDX:
                SpaceRocks().main_loop()
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN :
                if self.menu_idx == len(menu) - 1:
                    self.menu_idx = 0
                else:
                    self.menu_idx += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
                if self.menu_idx == 0:
                    self.menu_idx = len(menu) - 1
                else:
                    self.menu_idx -= 1
        
        
        

    def menu_view(self, menu):
        self.screen.blit(self.background, (0, 0))
        menu_len = len(menu)
        print_menu_text(self.screen, self.title, self.menu_font, 0, Color("white"))
        for i in range(menu_len):
              print_menu_text(self.screen, menu[i], self.menu_font, i + 1, Color("gray"))        
        print_menu_text(self.screen, menu[self.menu_idx], self.menu_font, self.menu_idx + 1, Color("white"))
        pygame.display.flip()
        
    def high_score_list_top_ten(self):
        pass

class GameOver(MainMenu):
    def menu_view(self, menu):
        self.screen.blit(self.background, (0, 0))
        menu_len = len(menu)
        print_menu_text(self.screen, self.title, self.menu_font, 0, Color("red"))
        for i in range(menu_len):
              print_menu_text(self.screen, menu[i], self.menu_font, i + 1, Color("gray"))        
        print_menu_text(self.screen, menu[self.menu_idx], self.menu_font, self.menu_idx + 1, Color("white"))
        pygame.display.flip()
    

        
        


