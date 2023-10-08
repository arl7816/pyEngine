import pygame as game
from pygame.sprite import spritecollide
import pyengine as engine
import math

vec = game.Vector2

class basicenemy():
    objectType = "TOMA"
    
    def movement(self, coor=(0,0), speed=1):
        deltaX = coor[0] - self.enemy.x
        deltaY = coor[1] - self.enemy.y

        distance = engine.dist(coor[0], coor[1], self.enemy.x, self.enemy.y)

        deltaX /= distance
        deltaY /= distance

        self.enemy.move(deltaX*speed, deltaY*speed)
    def __init__(self, coor=(0,0)) -> None:
        self.size = 7
        self.enemy = engine.Sprite("TOMA.png", coor, (30*self.size,30*self.size))
        #engine.Timer(1, self.movement, (self.player.x, self.player.y)).repeat = -1
class TomaSon(basicenemy):
    objectType = "TOMASON"

    def __init__(self, coor=(0,0,)) -> None:
        self.size = 1.5
        self.enemy = engine.Sprite("TOMASON.png", coor, (30*self.size,30*self.size))
class Arange():
    objectType = "ARANGE"

    def movement(self, walls, coor=(0,0), speed=.0000001):
        if (engine.checkCollision(self.enemy, walls[0]) or engine.checkCollision(self.enemy, walls[1])):
            self.dir = -self.dir
        self.enemy.move(speed * speed * self.dir, 0)

    def __init__(self, coor=(0,0)) -> None:
        self.size = 1.5
        self.enemy = engine.Sprite("ARANGE.jpg", coor, (30*self.size,30*self.size))
        self.enemy.basicHit() #:)
        self.dir = 1
        
        
class OrangeBullet():
    def __init__(self, coor=(0,0), size=(1,1)) -> None:
        self.enemy  = engine.Sprite("angycat.jpg", coor, size)
        self.enemy.basicHit()
        self.speed = 1.5
        self.objectType = "bullet"
    
    def movement(self, coor=(0,0), speed=1):
        self.enemy.move(0,speed * self.speed)

    def __str__(self) -> str:
        return "I am a bullet"




    

