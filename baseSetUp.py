# this is the base setup for any project in the 
import pygame as game
import pygameEngine as engine

WIDTH, HEIGHT = 450,200

DISPLAY = game.display.set_mode((WIDTH, HEIGHT)) # sets up the display
game.event.set_allowed([game.QUIT, game.KEYDOWN]) # events you want must be added here
game.display.set_caption("Temp name")

FPS = 60

def main():
  engine.loadLevel() # must be called at the start of every level
  clock = game.time.Clock()

  # base load here

  while 1:
    deltaTime = clock.tick(FPS) # keeps the framerate constant

    for event in game.event.get():
      if event.type == game.QUIT: game.quit(); return

    # do stuff here
    
    engine.update(DISPLAY) # applys physics if desired and updates graphics
  game.quit()

if __name__ == "__main__":
  main()
