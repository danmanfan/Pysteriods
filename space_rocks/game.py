# -*- coding: utf-8 -*-
"""
Created on Mon May  9 19:02:00 2022

https://realpython.com/asteroids-game-python/#prerequisites

@author: Daniel Flynn
"""

import pygame

# from game_over import GameOver
from models import Asteroid, Spaceship, OneUp
from pygame.math import Vector2
from utils import get_random_position, load_sprite, print_text, print_points


class SpaceRocks:
    
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    MIN_ASTEROID_DISTANCE = 150
    INITIAL_GAME_LIVES = 5
    INITIAL_SPACESHIP_POS = (400, 300)

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.points_font = pygame.font.Font(None, 20)
        self.message = ""
        self.number_of_asteroids = 3
        self.points = "00000000"
        self.asteroids = []
        self.bullets = []
        self.oneUps = []
        self.spaceship = Spaceship(self.INITIAL_SPACESHIP_POS, self.INITIAL_GAME_LIVES, self.bullets.append)
        self.generate_asteroids(self.number_of_asteroids)
        
        for i in range(self.spaceship.lives): # the OneUp objects being added
            self.oneUps.append(OneUp(((i * 10) + 10, self.SCREEN_HEIGHT - 10)))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()
            if self.message == "Game Over":
                pygame.time.wait(1000)
                break
            if self.message == "Next Level":
                # self.get_game_objects.remove(self.spaceship)
                pygame.time.wait(1000)
                self.number_of_asteroids += 1
                self.spaceship.velocity = Vector2(0)
                self.spaceship.position = Vector2(self.INITIAL_SPACESHIP_POS)
                self.spaceship.active = True
                self._get_game_objects().append(self.spaceship)
                self.generate_asteroids(self.number_of_asteroids)
                self.message = ""
            
    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")
        
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                and self.spaceship.active
            ):
                self.spaceship.shoot()
                
        is_key_pressed = pygame.key.get_pressed()
    
        if self.spaceship:
            if self.spaceship.active:
                if is_key_pressed[pygame.K_RIGHT]:
                    self.spaceship.rotate(clockwise=True)
                elif is_key_pressed[pygame.K_LEFT]:
                    self.spaceship.rotate(clockwise=False)
                if is_key_pressed[pygame.K_UP]:
                    self.spaceship.accelerate()
    
    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
            
        if self.spaceship:
            
            if not self.spaceship.active:
                self.spaceship.active = True
                for asteroid in self.asteroids:
                    self.spaceship.active = self.spaceship.active and (
                        asteroid.position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE)
                        # self._get_game_objects().append(self.spaceship)
            
            
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship) and self.spaceship.active:
                    
                    self._get_game_objects().remove(self.spaceship)
                    self.spaceship.lives -= 1
                    self.oneUps.pop()
                    self.spaceship.active = False
                    self.spaceship.velocity = Vector2(0)
                    self.spaceship.position = Vector2(self.INITIAL_SPACESHIP_POS)
                    # self.time_of_collisiun = pygame.time.Clock().get_time()
                    if(self.spaceship.lives < 1):
                        self.spaceship = None
                        # self.bullets = []
                        self.message = "Game Over"
                        break
        
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.points = str(asteroid.points + int(self.points))
                    while len(self.points) < 8 :
                        self.points = "0" + self.points
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    
                    asteroid.split()
                    break
    
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)
                
        if not self.asteroids and self.spaceship:
            self._get_game_objects().remove(self.spaceship)
            self.spaceship.active = False
            self.message = "Next Level"



    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
            
        if self.message:
            print_text(self.screen, self.message, self.font)
          
        print_points(self.screen, self.points, self.points_font)    
        pygame.display.flip()
        self.clock.tick(60)
        
    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets, *self.oneUps]
        
        if self.spaceship:
            if self.spaceship.active:
                game_objects.append(self.spaceship)
            
        return game_objects
    
    def generate_asteroids(self, number_of_asteroids):
        for _ in range(number_of_asteroids):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break
                
            self.asteroids.append(Asteroid(position, self.asteroids.append))