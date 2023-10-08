import pygame as game
import pygameEngine as engine
import random

WIDTH, HEIGHT = 400, 250

DISPLAY = game.display.set_mode((WIDTH, HEIGHT))
game.display.set_caption("Ping pong")

FPS = 60

def addScore(text):
  text.text = str(int(text.text)+1)

def input(player1, player2):
  speed = 6

  keys = engine.input()
  if keys[game.K_s]: player1.move(0,1*speed, DISPLAY)
  if keys[game.K_w]: player1.move(0,-1*speed, DISPLAY)
  #if keys[game.K_a]: player1.move(-1*speed,0, DISPLAY)
  #if keys[game.K_d]: player1.move(1*speed,0, DISPLAY)

  if keys[game.K_UP]: player2.move(0,-1*speed, DISPLAY)
  if keys[game.K_DOWN]: player2.move(0,1*speed, DISPLAY)
  #if keys[game.K_LEFT]: player2.move(-1*speed,0, DISPLAY)
  #if keys[game.K_RIGHT]: player2.move(1*speed,0, DISPLAY)

def resetGame(player1, player2, block):
  player1.xCoor = 10
  player1.yCoor = HEIGHT//2

  player2.xCoor = WIDTH-40
  player2.yCoor = HEIGHT//2

  block.xCoor, block.yCoor = WIDTH//2, HEIGHT//2

def main():
  clock = game.time.Clock()
  run = True

  player1 = engine.Rectangle((0+10,HEIGHT//2), (20,40), (255,255,255), trigger=True)
  player2 = engine.Rectangle((WIDTH-40, HEIGHT//2), (20,40), (255,255,255), trigger=True)
  block = engine.Rectangle((WIDTH//2, HEIGHT//2), (15,15), color=(255,255,255))

  player1Score = engine.Text("Roboto", 32, "0", coor=(100, 20))
  player2Score = engine.Text("Roboto", 32, "0", coor=(350, 20))

  ballSpeed = 3
  ballX = random.randrange(-1,2,2)
  ballY = random.randrange(-1,2,2)

  while run:
    clock.tick(FPS)
    for event in game.event.get():
      if event.type == game.QUIT:
        run = False

    input(player1, player2)
    block.move(ballSpeed * ballX, ballSpeed * ballY, DISPLAY)

    hasCollided = False

    if engine.checkCollision(block, player1) or engine.checkCollision(block, player2):
      if not(hasCollided):
        ballX = -ballX
        ballY = -ballY
        hasCollided = True

    if not(engine.checkCollision(block, player1) or engine.checkCollision(block, player2)):
      hasCollided = False

    if block.yCoor == 0:
      ballY = -ballY

    if block.yCoor + block.height == HEIGHT:
      ballY = -ballY 

    if block.xCoor == 0:
      addScore(player2Score)
      resetGame(player1, player2, block)
      ballX = random.randrange(-1,2,2)
      ballY = random.randrange(-1,2,2)
    if block.xCoor + block.width == WIDTH:
      addScore(player1Score)
      resetGame(player1, player2, block)
      ballX = random.randrange(-1,2,2)
      ballY = random.randrange(-1,2,2)
      

    DISPLAY.fill((0,0,0))

    player1.update(DISPLAY)
    player2.update(DISPLAY)
    block.update(DISPLAY)

    player1Score.show(DISPLAY)
    player2Score.show(DISPLAY)

    game.display.update()
  game.quit()

if __name__ == "__main__":
  main()
