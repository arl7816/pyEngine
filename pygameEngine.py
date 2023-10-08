import pygame as game
import math
import time
import os
import json

game.init() # starts up pygame and all its functions

# keeps track of games info (loaded stuff)
gameObjects = []
hudObjects = []
timers = []
frameNumber = 1

version = "0.1.4"

vec = game.math.Vector2

class memory():
  createdMemoryDumps = {
    # fileName: bool
  }

  # del dict[item]

  def createFile(fileName="defaultMemoryFile.json"):
    with open(fileName, "w") as newFile:
      json.dump({}, newFile)

  def get(fileName="defaultMemoryFile.json"):
    try:
      with open(fileName, "r") as readFile:
        return json.load(readFile)
    except:
      memory.createFile(fileName)
      with open(fileName, "r") as readFile:
        return json.load(readFile)
  
  def save(data,fileName="defaultMemoryFile.json"):
    with open(fileName, "w") as writeFile:
      json.dump(data, writeFile)

  def manage(dataName, data, fileName="defaultMemoryFile.json"):
    # manage does not support array or dictionary yet
    currentMemory = memory.get(fileName)
    currentMemory[dataName] = data
    memory.save(currentMemory, fileName)

  # these dont work nicely at the moment
  def makeMemoryDump(*dataPairs, fileName="defaultMemoryFile.json"):
    currentMemory = memory.get(fileName)
    print(dataPairs)
    for dataPair in dataPairs:
      print(dataPair)
      currentMemory[dataPair[0]] = dataPair[1]
    memory.save(currentMemory, fileName)

  def memoryDump(fileName,*dataPairs):
    # creates a timer that pumps in the new memory vales every 't' seconds for each file
    try:
      memory.createdMemoryDumps[fileName]
    except:
      memory.createdMemoryDumps[fileName] = True
      Timer(1, memory.makeMemoryDump, *dataPairs, fileName=fileName)

class music():
  
  def play(file,amount=-1):
    game.mixer.music.load(file)
    game.mixer.music.play(amount-1)

  def pause():
    game.mixer.music.pause()

  def unpause():
    game.mixer.music.unpause()
  
  def restart():
    game.mixer.music.rewind()
  
  def stop():
    game.mixer.music.stop()

  def volume(newVolume=None):
    if newVolume != None:
      game.mixer.music.set_volume(newVolume)

    return game.mixer.music.get_volume()

  def time(newTime):
    if newTime != None:
      music.restart()
      game.mixer.music.set_pos(newTime)
    
    return game.mixer.music.get_pos()

  def next(file):
    game.mixer.music.queue(file)

# creates a timer that calls a function every x seconds
class Timer():
  callTime = None
  funct = None
  repeat = 1 # -1 = repeat forever
  name = "Default"
  startTime = None
  arguments = None
  defaults = None

  enabled = True

  def __init__(self, callTime, funct, *arguments, **defaults):
    self.callTime = callTime
    self.funct = funct
    self.arguments = arguments
    self.defaults = defaults

    self.startTime = time.perf_counter()

    timers.append(self)
  
  def checkTime(self):
    currentTime = time.perf_counter()
    elapTime = currentTime-self.startTime
    if elapTime >= self.callTime and self.repeat != 0:
      self.funct(*self.arguments, **self.defaults)
      self.startTime = currentTime
      if self.repeat != 0:
        self.repeat -= 1

  def destroy(self):
    del self

class hudObject():
  enabled = True
  isShown = True
  x = None
  y = None

  name = "Default Name"

  def move(self, addX, addY):
    self.x += addX
    self.y += addY
  
  def teleport(self, newX, newY):
    self.x = newX
    self.y = newY

  def __str__(self) -> str:
    return self.name

  def destroy(self):
    del self

class Image(hudObject):
  image = None

  def __init__(self, image, coor=(0,0)):
    self.image = game.image.load(image).convert()
    self.x, self.y = coor[0], coor[1]

    hudObjects.append(self)

  def getWidth(self):
    return self.image.get_width()

  def getHeight(self):
    return self.image.get_height()

  def setSize(self, width=None, height=None):
    if width == None: width = self.getWidth()
    if height == None: height = self.getHeight()
    self.image = game.transform.smoothscale(self.image, (width, height))

  def show(self, DISPLAY):
    DISPLAY.blit(self.image, (self.x,self.y))

class Button(hudObject):
  image = None
  width = 50
  height = 20
  text = None
  center = vec(0,0)

  def __init__(self, coor=(0,0), size=(50,20), text=None, image=None) -> None:
    self.x, self.y = coor[0], coor[1]

    self.width = size[0]
    self.height = size[1]
    self.text = text
    self.image = image

    #hudObjects.append(self) implement this later

class Bar(hudObject):
  width = 0
  height = 0
  color = (255,255,255)

  hollow = False

  def __init__(self, coor=(0,0), size=(30,30), color=(255,255,255)):
    self.x, self.y = coor[0], coor[1]

    self.width, self.height = size[0], size[1]

    self.color = color

    hudObjects.append(self)

  def show(self, DISPLAY):
    if not(self.hollow):
      game.draw.rect(DISPLAY, self.color, (self.x, self.y, self.width, self.height))
    else:
      game.draw.rect(DISPLAY, self.color, (self.x, self.y, self.width, self.height), 2)

class Dot(hudObject):
  radius = 5
  color = (255,255,255)

  hollow = False

  def __init__(self, coor=(0,0), radius=5, color=(255,255,255)):
    self.x, self.y = coor[0], coor[1]
    self.radius = radius
    self.color = color

    hudObjects.append(self)

  def show(self, DISPLAY):
    if not(self.hollow):
      game.draw.circle(DISPLAY, self.color, (self.x, self.y), self.radius)
    else:
      game.draw.circle(DISPLAY, self.color, (self.x, self.y), self.radius, 2)


class Text(hudObject):

  font = None
  size = None
  text = ""
  textColor = (255,255,255)
  highlight = None

  def __init__(self, font, size, text="", textColor=(255,255,255), highlight=None, coor=(0,0)):
    self.font = font
    self.size = size
    self.text = text
    self.textColor = textColor
    self.highlight = highlight
    self.x, self.y = coor[0], coor[1]

    hudObjects.append(self)

  def show(self, DISPLAY):
    if self.isShown:
      font = game.font.SysFont(self.font, self.size)
      text = font.render(self.text, True, self.textColor)

      textRect = text.get_rect()
      textRect.center = (self.x, self.y)

      DISPLAY.blit(text, textRect)

class GameObject():
  mass = 1
  gravity = 9.81

  x = 0
  y = 0

  color = (255,0,0)

  trigger = False
  hasPhysics = False

  name = "Default Name"

  isShown = True

  forces = (0,0)

  enabled = True

  def destroy(self):
    del self

  def applyForce(self, force=(0,0)):
    self.forces = (self.forces[0]+force[0], self.forces[1]+force[1])

  def teleport(self, newX, newY):
    self.x, self.y = newX, newY

  def __str__(self):
    return self.name

class Sprite(GameObject):
  objectType = "sprite"

  image = None

  hitBoxes = []

  hitbox = None # this is temp

  def __init__(self, image, coor=(0,0), size=None):
    self.x, self.y = coor[0], coor[1]
    
    self.image = game.image.load(image).convert()

    if size != None:
      self.image = game.transform.smoothscale(self.image, (size[0],size[1]))

    gameObjects.append(self)

  def getWidth(self):
    return self.image.get_width()

  def getHeight(self):
    return self.image.get_height()

  def setSize(self, width=None, height=None):
    if width == None: width = self.getWidth()
    if height == None: height = self.getHeight()
    self.image = game.transform.smoothscale(self.image, (width, height))

    if self.hitbox != None:
      self.hitbox.width = width
      self.hitbox.height = height

  def move(self, addX, addY, DISPLAY=None):
    if self.hitbox != None:
      orginalX = self.hitbox.x
      orginalY = self.hitbox.y

      self.hitbox.move(addX, addY, DISPLAY)
      # need to use the delta X and Y, not the coors
      deltaX = self.hitbox.x - orginalX
      deltaY = self.hitbox.y - orginalY

      self.x += deltaX
      self.y += deltaY
    else:
      self.x += addX
      self.y += addY

  def basicHit(self):
    self.hitbox = Hitbox((self.x, self.y), (self.getWidth(), self.getHeight()))
  
  def addHitBox(hitbox):
    pass

  def update(self, DISPLAY):
    DISPLAY.blit(self.image, (self.x,self.y))

    if self.hitbox != None:
      self.hitbox.update(DISPLAY)

def Shape(GameObject):
  objectType = "poly"

  points = []
  color = (0,0,255)
  center = None

  def __init__(self, points, color=(0,0,255)):
    for point in points:
      self.points.append(vec(point[0], point[1]))

    self.color = color

    self.center = findCenter()

    gameObjects.append(self)
    

  def findCenter(self):
    pSum = vec()
    for p in self.points:
      pSum += p
    return pSum/len(self.points)

  def update(self, DISPLAY):
    game.draw.polygon(DISPLAY, self.color, self.points)

class Line(GameObject):
  objectType = "line"
  points = None
  color = None
  center = None
  rotation = 0

  def __init__(self, points, color=(0,0,255)):
    self.points = [vec(points[0][0], points[0][1]), vec(points[1][0], points[1][1])]

    self.color = color

    pSum = vec()
    for p in self.points:
      pSum += p
    self.center = pSum/2

    gameObjects.append(self)

  def move(self, addX, addY, DISPLAY=None):
    oldVecs = [vec(self.points[0].x,self.points[0].y), vec(self.points[1].x, self.points[1].y)]
    oldCenter = self.center

    self.points[0].x += addX
    self.points[0].y += addY

    self.points[1].x += addX
    self.points[1].y += addY

    self.center.x += addX
    self.center.y += addY

    for gameObject in gameObjects:
      if gameObject.objectType == "line" and gameObject != self and self.checkCollision(gameObject, oldCenter=oldCenter):
        self.color = (255,0,0)
      else:
        self.color = (0,0,255)

  def rotate(self, angle):
    oldVecs = [vec(self.points[0].x,self.points[0].y), vec(self.points[1].x, self.points[1].y)]

    angle = math.pi * angle
    self.rotation += angle
    for point in self.points:
      # translate the center to the origin
      point -= self.center
      # rotate point around the origin
      original_x = point.x
      original_y = point.y
      point.x = original_x * math.cos(angle) - original_y * math.sin(angle)
      point.y = original_y * math.cos(angle) + original_x * math.sin(angle)
      # translate back to shape's center
      point += self.center
    for gameObject in gameObjects:
      if gameObject.objectType == "line" and gameObject != self and self.checkCollision(gameObject, oldVecs):
        self.color = (255,0,0)
      else:
        self.color = (0,0,255)


  def checkCollision(self, other, oldVecs=None, oldCenter=None):
    x1, y1 = self.points[0].x, self.points[0].y
    x2, y2 = self.points[1].x, self.points[1].y
    x3, y3 = other.points[0].x, other.points[0].y
    x4, y4 = other.points[1].x, other.points[1].y

    try:
      uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
      uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    except:
      return False

    if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
      intersectionX = x1 + (uA * (x2-x1))
      intersectionY = y1 + (uA * (y2-y1))
      interSectionVec = vec(intersectionX, intersectionY)

      fixDelta = other.center - oldCenter
      self.points[0] -= fixDelta
      self.points[1] -= fixDelta
      self.center -= fixDelta

      return True
    return False

  def update(self, DISPLAY):
    game.draw.line(DISPLAY, self.color, self.points[0], self.points[1])

class Rectangle(GameObject):
  objectType = "rect"

  height = 30
  width = 30

  color = (255,0,0)

  trigger = False

  def __init__(self,coor=(0,0), size=(30,30), color=(255,0,0), trigger=False):
    self.x, self.y = coor[0], coor[1]

    self.width, self.height = size[0], size[1]

    self.color = color

    self.trigger = trigger

    gameObjects.append(self)

  def move(self, addX, addY, DISPLAY=None, screenSize=None):
    # will move the character, if display or screen size is given, treast the screen as a border

    width, height = None,None

    if DISPLAY != None:
      width, height = DISPLAY.get_size()
    if screenSize != None:
      width, height = screenSize[0], screenSize[1]

    if width != None:
      # do our movements
      if addX != 0:
        if addX > 0:
          # check right
          if self.x + self.width + addX > width: addX = width - (self.x + self.width)
        else:
          # check left
          if self.x + addX < 0: addX = -self.x

      if addY != 0:
        if addY > 0:
          # check downward
          if self.y + self.height + addY > height: addY = height - (self.y + self.height)
        else:
          # check upward
          if self.y + addY < 0: addY = -self.y
    
    if not(self.trigger):
      for gameObject in gameObjects:
        if gameObject.objectType == "rect" and gameObject != self:
          addX, _ = checkCollision(self, gameObject, addX, 0)
          _, addY = checkCollision(self, gameObject, 0, addY)

    self.x += addX
    self.y += addY
    
  
  def update(self, DISPLAY):

    if self.isShown:
      game.draw.rect(DISPLAY, self.color, (self.x, self.y, self.width, self.height))

    #game.draw.rect(DISPLAY, self.color, (self.x, self.y, self.width, self.height), 2) for hit boxes

class Hitbox(Rectangle):
  def __init__(self,coor=(0,0), size=(30,30), color=(255,0,0), trigger=False):
    self.x, self.y = coor[0], coor[1]

    self.width, self.height = size[0], size[1]

    self.color = color

    self.trigger = trigger

  def update(self, DISPLAY):

    if not(self.trigger):
      game.draw.rect(DISPLAY, (0,255,0), (self.x, self.y, self.width, self.height), 2)
    else:
      game.draw.rect(DISPLAY, (255,0,0), (self.x, self.y, self.width, self.height), 2)
  
class Circle(GameObject):
  objectType = "circle"

  radius = None

  color = None

  def __init__(self, coor=(0,0), radius=5, color=(0,0,255)):
    self.x, self.y = coor[0], coor[1]
    self.radius = radius
    self.color = color
    
    gameObjects.append(self)

  def move(self, addX, addY, DISPLAY=None, screenSize=None):
    width, height = None, None
    if DISPLAY != None: width, height = DISPLAY.get_size()
    if screenSize != None: width, height = screenSize[0], screenSize[1]

    if width != None:
      if addX != 0:
        if addX > 0:
          if self.x + self.radius + addX >= width: addX = width - (self.x+self.radius)
        else:
          if self.x - self.radius + addX <= 0: addX = -(self.x - self.radius)
      
      if addY != 0:
        if addY > 0:
          if self.y + self.radius + addY >= height: addY=height-(self.y+self.radius)
        else:
          if self.y - self.radius + addY <= 0: addY = -(self.y - self.radius)

    if not(self.trigger):
      for gameObject in gameObjects:
        if gameObject.objectType == "circle" and gameObject != self and not(gameObject.trigger):
          addX, addY = checkCollision(self, gameObject, addX, addY)

    self.x += addX
    self.y += addY
  
  def update(self, DISPLAY):
    if self.isShown:
      game.draw.circle(DISPLAY, self.color, (self.x, self.y), self.radius)

class camera():
  def move(addX,addY):
    addX = -addX
    addY = -addY

    for gameObject in gameObjects:
      gameObject.teleport(gameObject.x+addX, gameObject.y+addY)

def input():
  return game.key.get_pressed()

def convertInput(code):
  return game.key.key_code(code)

def checkCollision(object1, object2, addX=None, addY=None):
  # it is assumed that object1 is the moving object

  if object1.objectType == "sprite" and object1.hitbox != None:
    object1 = object1.hitbox
  if object2.objectType == "sprite" and object2.hitbox != None:
    object2 = object2.hitbox

  if object1.objectType == "circle" and object2.objectType == "circle":
    if addX != None or addY != None:
      if addX == None: addX = 0
      if addY == None: addY = 0

      if object1.trigger or object2.trigger:
        return addX, addY

      hypoDeltaX = object1.x + addX - object2.x
      hypoDeltaY = object1.y + addY - object2.y

      if math.sqrt(math.pow(hypoDeltaX, 2) + math.pow(hypoDeltaY, 2)) < object1.radius + object2.radius:
        distanceX = object1.x - object2.x
        distanceY = object1.y - object2.y
        radiiSum = object1.radius + object2.radius
        netDistance = math.sqrt(math.pow(distanceX, 2) + math.pow(distanceY, 2))
        if netDistance == 0:
          return 0,0
        unitX = distanceX / netDistance
        unitY = distanceY / netDistance
        
        correctX = object2.x + (radiiSum) * unitX
        correctY = object2.y + (radiiSum) * unitY

        addX = correctX - object1.x
        addY = correctY - object1.y

        return addX, addY
      else:
        return addX, addY
    else:
      deltaX = object1.x - object2.x
      deltaY = object1.y - object2.y
      distance = math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))
      return distance <= object1.radius + object2.radius

  elif object1.objectType == "rect" and object2.objectType == "rect":
    if addX != None or addY != None:
      if addX == None: addX = 0
      if addY == None: addY = 0

      if object1.trigger or object2.trigger:
        return addX, addY

      hypoX = object1.x + addX
      hypoY = object1.y + addY

      if not(hypoX > object2.x + object2.width or hypoX + object1.width < object2.x or hypoY > object2.y + object2.height or hypoY + object1.height < object2.y):
        
        # there will be a  collision
        if object1.x >= object2.x:
          distanceX = (object1.x)-(object2.x+object2.width)
        else:
          distanceX = (object1.x+object1.width)-object2.x


        if object1.y >= object2.y:
          distanceY = (object1.y)-(object2.y+object2.height)  
        else:
          distanceY = (object1.y+object1.height)-object2.y

        if addX != 0 and distanceY != 0:
          if distanceX == 0:
            return 0,0
          elif distanceX > 0:
            # object1 is on the right side, moving left
            addX = -(object1.x - (object2.x+object2.width))
          else:
            # object1 is on the left, moving right
            addX = object2.x - (object1.x+object1.width)

        if addY != 0 and distanceX != 0:
          if distanceY == 0:
            return 0,0
          elif distanceY > 0:
            # object1 is below and is moving up
            addY = -(object1.y - (object2.y+object2.height))
          else:
            # object1 below and is moving down
            addY = (object2.y - (object1.y+object1.height))

      return addX, addY
    else:
      return not(object1.x > object2.x + object2.width or object1.x + object1.width < object2.x or object1.y > object2.y + object2.height or object1.y + object1.height < object2.y)
  elif object1.objectType == "circle" and object2.objectType == "rect":
    return True
  elif object1.objectType == "rect" and object2.objectType == "circle":
    return True

def dist(x1, y1, x2, y2):
  deltaX = x2-x1
  deltaY = y2-y1

  return math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))

def applyMovement(gameObject, DISPLAY):
  netY = gameObject.forces[1]

  netY += gameObject.mass*gameObject.gravity

  if not(gameObject.trigger):
    gameObject.move(0,netY, DISPLAY)
  else:
    gameObject.move(0,netY)

def changeLayer(newLayer, object=None, name=""):
  for index, gameObject in enumerate(gameObjects):
    if object != None and object == gameObject or name != "" and name == gameObject.name:
      gameObjects.insert(newLayer, gameObject)
      gameObjects.pop(index + 1)
      return True

  for index, hudObject in enumerate(hudObjects):
    if object != None and object == hudObject or name != "" and name == hudObject.name:
      hudObjects.insert(newLayer, hudObject)
      hudObjects.pop(index + 1)
      return True
  return False

def loadLevel():
  global hudObjects
  global gameObjects
  global frameNumber
  global timers

  hudObjects = []
  gameObjects = []
  timers = []
  frameNumber = 1


def update(DISPLAY):
  global frameNumber
  frameNumber += 1

  for timer in timers:
    if timer.enabled:
      timer.checkTime()

  for gameObject in gameObjects:
    if gameObject.enabled:
      if gameObject.hasPhysics:
        applyMovement(gameObject, DISPLAY)
      if gameObject.isShown:
        gameObject.update(DISPLAY)

  for hudObject in hudObjects:
    if hudObject.enabled:
      if hudObject.isShown:
        hudObject.show(DISPLAY)
