import pygame as game
import random

WIDTH, HEIGHT = 900,500

FPS = 60

DISPLAY = game.display.set_mode((WIDTH, HEIGHT))
game.display.set_caption("First Pygame Game")


class Object():
  player = None

  coor = [0,0]
  color = [255,0,0]
  size = [30,30]

  def __init__(self, color=[255,0,0], startCoor=[0,0], startSize=[30,30]) -> None:
    self.color = color
    self.coor = startCoor
    self.size = startSize

  def changeColor(self, newColor):
    pass

class Player(Object):
  type = "rect"

  def move(self, addX=0, addY=0) -> None:

    if addX != 0:
      if addX > 0:
        # check right
        if self.coor[0] + self.size[0] + addX >= WIDTH: addX = WIDTH - (self.coor[0] + self.size[0])
      else:
        # check left
        if self.coor[0] + addX <= 0: addX = -self.coor[0]

    if addY != 0:
      if addY > 0:
        # check downward
        if self.coor[1] + self.size[1] + addY >= HEIGHT: addY = HEIGHT - (self.coor[1] + self.size[1])
      else:
        # check upward
        if self.coor[1] + addY <= 0: addY = -self.coor[1]

    self.coor[0] += addX
    self.coor[1] += addY

  def update(self):
    self.player = game.draw.rect(DISPLAY, self.color, (self.coor[0],self.coor[1], self.size[0],self.size[1]))

class Ball(Object):
  type = "circle"

  speed = 6
  x = random.randrange(-1,2,2)
  y = random.randrange(-1,2,2)

  def move(self):
    self.coor[0] += self.x*self.speed
    self.coor[1] += self.y*self.speed

  def update(self):
    game.draw.circle(DISPLAY, self.color, self.coor, self.size[0])

def input(player1, player2):
  playerSpeed = 6
  keys = game.key.get_pressed()
  '''if keys[game.K_a]:
    player1.move(-playerSpeed)
  if keys[game.K_d]:
    player1.move(playerSpeed)'''
  if keys[game.K_s]:
    player1.move(addY=playerSpeed)
  if keys[game.K_w]:
    player1.move(addY=-playerSpeed)

  if keys[game.K_DOWN]:
    player2.move(addY = playerSpeed)
  if keys[game.K_UP]:
    player2.move(addY=-playerSpeed)
  '''if keys[game.K_LEFT]:
    player2.move(-playerSpeed)
  if keys[game.K_RIGHT]:
    player2.move(playerSpeed)'''

def main():
  print("Game has begun")

  run = True
  clock = game.time.Clock()

  player2 = Player([0,0,255], [830, 250], [40,100])
  player1 = Player([0,255,0], [30, 250], [40,100])
  ball = Ball(startCoor=[450,250], startSize=[15,0])

  while run:
    clock.tick(FPS)
    for event in game.event.get():
      if event.type == game.QUIT:
        run = False
    
    input(player1, player2)
    ball.move()

    DISPLAY.fill((0,0,0))
    player1.update()
    player2.update()
    ball.update()
    game.display.update()
  
  print("Game has ended")
  game.quit()


main()