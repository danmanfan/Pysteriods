# -*- coding: utf-8 -*-
"""
Created on Mon May 16 14:25:51 2022

@author: Daniel Flynn
"""
import pygame

from game import SpaceRocks
from utils import print_menu_text

class GameSelection:
    
    def __init__(self):
        self.space_rocks = SpaceRocks()
    
    def game_selection(self, menu):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.menu_idx == self.QUIT_IDX
            )):
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.menu_idx == self.START_IDX:
                self.space_rocks.main_loop()
                
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

    