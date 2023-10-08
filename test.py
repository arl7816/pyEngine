# this is the base setup for any project in the 
import pygame as game
import pyengine as engine
from pyengine import convertInput as key
import random
import math
import enemyFile

WIDTH, HEIGHT = 900,700

DISPLAY = game.display.set_mode((WIDTH, HEIGHT), game.DOUBLEBUF) # sets up the display
game.display.set_caption("Camera Test")

FPS = 300
game.event.set_allowed([game.QUIT, game.KEYDOWN])
enemies = []


def addEnemy(enemy):
  global enemies
  print(enemies)
  enemies.append(enemy)
  print(enemies)
#you got out, you think you are free for a moment, but then you aren't anywhere familiar so many beingss trying to kill you, whats the point in going on.
def moveEnemy(enemies, player, speed):
  for enemy in enemies:
    #enemy.movement((player.x, player.y), speed)
    if (enemy.objectType == "TOMA"):
      enemy.movement((player.x, player.y), speed/400) 
    if(enemy.objectType == "TOMASON"):
      enemy.movement((player.x, player.y), speed*3)
  if (engine.checkCollision(enemy.enemy, player)):
    player.destroy()

def destroyEnemy():
  pass
#all is dark all you can see for eternity are what seems to be "stars" and "planets" after observing for a while you see A HUGE TOMATO FLZYING AT YOZU, ITS THE TOMATO KING
def drawBackground():
  for _ in range(0,100):
    x = random.randint(0, WIDTH)
    y = random.randint(0,HEIGHT)

    width = random.random() * random.randint(1,10)
    height = width

    radius = random.random() * random.randint(1,5)
    #a failed civilization of star fruit they fell to the powerful tomato kingdom 
    #star = engine.Circle((x, y), radius, (255,255,255))
    #star.trigger = True

    star = engine.Rectangle((x, y), (width, height), (255,255,255), True)
    engine.changeLayer(0, star)

def deathState(score):
  def boxSizeIncrease(box):
    if box.height < HEIGHT - 100:
      box.height += 5
    elif box.x > 100:
      box.x -= 2.5
      box.width += 5

      if box.x <= 100:
        engine.Text("Comic Sans", 32, "Score: " + score, coor=(box.x+box.width/2, box.y+50))

        memory = engine.memory.get()
        try:
          if int(memory["high score"]) < int(score):
            memory["high score"] = score
            engine.memory.save(memory)
        except:
          memory["high score"] = score
          engine.memory.save(memory)

        engine.Text("Comic Sans", 32, "High Score: " + memory["high score"], coor=(box.x+box.width/2, box.y+100))


  grayBox = engine.Bar((WIDTH/2-5, 50), (5,5), (18,28,51))
  engine.Timer(0.01, boxSizeIncrease, grayBox).repeat = -1
#score acronym for Score that number that keeps going up.
def increaseScore(text, amount = 0):
  text.text = str(int(text.text) + amount)
#define the "enemies", are they really your enemies when you are intruding on their land
def spawnEnemy():
  global enemies
  enemy = enemyFile.TomaSon()
  enemy.enemy.basicHit()
  print(enemies)
  enemies.append(enemy)
  print(enemies)

def spawnBullet(arange, size=1):
  if not(arange.enemy.enabled): return
  global enemies
  enemies.append(enemyFile.OrangeBullet())

def main():
  global enemies
  engine.loadLevel() # must be called at the start of every level
  #time is relative, how will you spend your last moments on this earth every moment is fleeting and you spend all of your time data mining this game
  clock = game.time.Clock()
  
  enemies = [enemyFile.TomaSon()] #tomason, toma's son is inspired by his father and wants to become the next tomato king but since he isnt as strong or as big he, he relies on his speed and his bretheren
  enemies[0].dynamic = False
  #someone doesnt know how to code
  #def spawnEnemy():
    #enemies.append(enemys.basic(WIDTH/2, HEIGHT + 30, 30, 30, "down/up"))

  # base load here
  #wspawnEnemy()

#creating the prison shackling you to reality
  ground = engine.Rectangle((0, HEIGHT-20), (WIDTH, 30), (255,255,255))
  walls = [engine.Rectangle((0,0),(30,HEIGHT), (255,255,255)), engine.Rectangle((WIDTH-30, 0), (30,HEIGHT), (255,255,255))]



  ground.dynamic = False
  for wall in walls:
    wall.dynamic = False
#creats the players reflection a imperfect vesion of the original  no one can compare to the original :) rick doesnt know if he should trust this entity but he has no choice...
  mirror = engine.Rectangle((300, 350),(30, 30))

  text = engine.Text("roboto", 32, "0", coor=(WIDTH/2, 20))
  engine.Timer(0.1, increaseScore, text, 1).repeat = -1
#display fps var
  fps = engine.Text("roboto", 32, "FPS: 0", coor=(WIDTH-100, 32))  

  #spawns the player, rick in a strage world where tomatoes from pvz want to kill you also some fruit guy wants to kill you but thats okay
  sprite = engine.Sprite("undertaleHeart.png", (WIDTH/2, HEIGHT/2))
  sprite.setSize(30,30)
  sprite.basicHit()
  sprite.hitbox = engine.Hitbox((sprite.x, sprite.y), (30,30))
  
  engine.music.play("Epic Song.mp3")
  engine.music.volume(.1)
  #WE MAKE DA ENEMY

  drawBackground()

  #mirror.trigger = True
  mirror.dynamic = False

  engine.music.play("Beat #1.wav")
#spawn orange man and his goons
  enemies = [enemyFile.basicenemy(coor = (30,400)),enemyFile.TomaSon(),enemyFile.Arange(coor= (100, 100))]
  enemies[0].enemy.basicHit()
  enemies[1].enemy.basicHit()#dom likes nathan <3 <3 <3
  enemies[1].trigger = True
  enemies[0].trigger = True

  # the variable keeping tomason respawn like mincraft
  svariable = engine.Timer(5, spawnEnemy)
  svariable.repeat = -1

  engine.Timer(2,spawnBullet,enemies[2])



  while 1:
    deltaTime = clock.tick(FPS) # keeps the framerate constant
    fps.text = "FPS: " + str(math.floor(clock.get_fps()))
  #so basically its saying  you know how when it clicks the x button it quits the game so actually let me rephrase this  every single frame were going to go through the for loop that goes through the event systems abnd then what were are going to do on the line right here is when they click on the x quits the game
    print(enemies[2].enemy.enabled)
    enemies[2].enabled = True
    for event in game.event.get():
      if event.type == game.QUIT: 
        game.quit()
        return
       
      if event.type == game.KEYDOWN:
        pressed = engine.input()
      # you are on the floor... crying about your terrible decisions in your meaningless life all the roads you couldve went down you chose the wrong one... you have to face your decisions head on right now., so you die :) <3
        if pressed[key("k")]:
          text.isShown = False
          deathState(text.text)
      # if r pressed :) restart
        if pressed[key("r")]:
          main()
          return

    # do stuff here

    for enemy in enemies:
      #if enemy touch yo mirror fren KILLLL!!!!!!!!!! 
      if enemy.objectType == "ARANGE":
        enemy.movement(walls, (sprite.x, sprite.y), .3*deltaTime)
      else:
        enemy.movement((sprite.x, sprite.y), .3*deltaTime)  

      
      if engine.checkCollision(enemy.enemy, mirror):
        enemy.enemy.destroy()
      #if enemy touch human kill!!!    
      if engine.checkCollision(enemy.enemy, sprite):
        sprite.destroy()
        destroyEnemy()
        deathState(text.text)
        #funny enemy spawn
      if enemies[0].enemy.enabled:
        svariable.repeat = 0
  #character movement
    speed = .7
    movementX = 0
    movementY = 0
    keys = engine.input()
    if keys[key("w")]:
     movementY = -1
    if keys[key("s")]:
      movementY = 1
    if keys[key("a")]:
      movementX = -1
    if keys[key("d")]:
      movementX = 1
  #camera movement
    if keys[key("up")]:
      engine.camera.move(0,-5)
    if keys[key("down")]:
      engine.camera.move(0,5)
    if keys[key("left")]:
      engine.camera.move(-5,0)
    if keys[key("right")]:
      engine.camera.move(5,0)
    #movement
    sprite.move(movementX*speed*deltaTime, movementY*speed*deltaTime)
    mirror.move(-movementX*speed*deltaTime, -movementY*speed*deltaTime)
    #if miror hit main character he die
    if engine.checkCollision(sprite, mirror):
      sprite.destroy()
      deathState(text.text)
    #if mirror hit wall it die
    if engine.checkCollision(mirror, ground):
      mirror.destroy()
    if engine.checkCollision(mirror, walls[0]):
      mirror.destroy()
    if engine.checkCollision(mirror, walls[1]):
      mirror.destroy()
    if engine.checkCollision(mirror, ground):
      mirror.destroy()

    

    moveEnemy(enemies, sprite, .1*deltaTime)

    engine.update(DISPLAY) # applys physics if desired and updates locations
  game.quit()

if __name__ == "__main__":
  main()
