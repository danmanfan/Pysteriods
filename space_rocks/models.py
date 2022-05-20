# -*- coding: utf-8 -*-
"""
Created on Mon May  9 22:21:20 2022

https://realpython.com/asteroids-game-python/#prerequisites

@author: Daniel Flynn
"""

from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import get_random_velocity, load_sound, load_sprite, wrap_position


UP = Vector2(0, -1)

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        
    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)
        
    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)
        
    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius
    
class Spaceship(GameObject):
    
    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    BULLET_SPEED = 3
    TERMINAL_VELOCITY = 20
        
    def __init__(self, position, lives, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        self.direction = Vector2(UP)
        self.lives = lives
        self.active = True
        super().__init__(position, load_sprite("spaceship"), Vector2(0))
        
    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)
        
    def accelerate(self):
        tempVelocity = self.velocity + (self.direction * self.ACCELERATION)
        if (tempVelocity.magnitude() <= self.TERMINAL_VELOCITY):
            self.velocity = tempVelocity
        
    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
        
    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()
        
class OneUp(GameObject):
    
    def __init__(self, position):
        super().__init__(position, rotozoom(load_sprite("spaceship"), 0, .25), Vector2(0))
        
class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size
        
        
        size_to_scale = {
            3 :1,
            2: 0.5,
            1: 0.25,
        }
        
        points_by_size = {
            3 : 100,
            2 : 50,
            1 : 25,
        }
        
        self.points = points_by_size[size]
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)
        
        super().__init__(
            position, sprite, get_random_velocity(1, 3)    
        )
        
    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1    
                )
                self.create_asteroid_callback(asteroid)
        
class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)
        
    def move(self, surface):
        self.position = self.position + self.velocity