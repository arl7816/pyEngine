import pygame as game
import math
import time
import os
import json

game.mixer.pre_init(44100, 16, 2, 4096)
game.init() # starts up pygame and all its functions

# keeps track of games info (loaded stuff)
gameObjects = []
hudObjects = []
timers = []
frameNumber = 1
lookup = {}

version = "0.1.4"
running = True

vec = game.math.Vector2

# global variables
class variables():
  def __init__(self) -> None:
    pass

  def set(key, value):
    lookup[key] = value
  
  def get(key):
    if not(key in lookup):
      return None
    
    return lookup[key]

  def everything():
    return lookup

  def delete(key):
    if key in lookup:
      del lookup[key]

  def reset():
    lookup = {}

# local variables
class Variables(): 
  def __init__(self) -> None:
    self.lookup = {}

  def set(self, key, value):
    self.lookup[key] = value
  
  def get(self, key):
    if not(key in self.lookup):
      return None
    
    return self.lookup[key]

  def everything(self):
    return self.lookup

  def delete(self, key):
    if key in self.lookup:
      del self.lookup[key]

  def reset(self):
    self.lookup = {}

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
    for dataPair in dataPairs:
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
    self.repeat = 0
    timers.remove(self)

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
    self.enabled = False
    hudObjects.remove(self)

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

  dynamic = True

  def destroy(self):
    self.enabled = False
    gameObjects.remove(self)

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

  def rotate(self, angle):
    pass

  def setSize(self, width=None, height=None):
    if width == None: width = self.getWidth()
    if height == None: height = self.getHeight()
    self.image = game.transform.smoothscale(self.image, (width, height))

    if self.hitbox != None:
      self.hitbox.width = width
      self.hitbox.height = height

  def move(self, addX, addY, DISPLAY=None):
    self.x += addX
    self.y += addY
    if self.hitbox != None:
      self.hitbox.move(addX, addY)

  def basicHit(self):
    self.hitbox = Hitbox((self.x, self.y), (self.getWidth(), self.getHeight()))
  
  def addHitBox(hitbox):
    pass

  def update(self, DISPLAY):
    DISPLAY.blit(self.image, (self.x,self.y))

    if self.hitbox != None:
      self.hitbox.update(DISPLAY)

class Shape(GameObject):
  objectType = "poly"

  points = []
  color = (0,0,255)
  center = None
  radius = 0

  hollow = False

  def __init__(self, points, color=(0,0,255)):
    self.points = []
    for point in points:
      self.points.append(vec(point[0], point[1]))

    self.color = color

    self.center = self.findCenter()

    self.objectType = "poly"

    self.radius = self.getRadius()

    gameObjects.append(self)
    
  def move(self, addX=0, addY=0):
    distance = vec(addX, addY)
    for index in range(len(self.points)):
      self.points[index] += distance
    self.center += distance

    #checkCollision(self)

  def teleport(self, newX, newY):
    addX = newX - self.center.x
    addY = newY - self.center.y
    distance = vec(addX, addY)
    self.center += distance
    for index in range(len(self.points)):
      self.points[index] += distance

  def rotate(self, angle):
    # rotate the edges around the shape's center
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

    #checkCollision(self)
    
  def findCenter(self):
    pSum = vec()
    for p in self.points:
      pSum += p
    return pSum/len(self.points)

  def getRadius(self):
    radius = 0
    for point in self.points:
      distance = dist(self.center.x, self.center.y, point.x, point.y)
      if distance > radius:
        radius = distance

    return radius

  def update(self, DISPLAY):
    if not(self.hollow):
      game.draw.polygon(DISPLAY, self.color, self.points)
    else:
      if self.trigger:
        game.draw.polygon(DISPLAY, (255,0,0), self.points, 2)
      else:
        game.draw.polygon(DISPLAY, (0,255,0), self.points, 2)

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

class Rectangle(Shape):
  height = 30
  width = 30

  color = (255,0,0)

  def __init__(self,coor=(0,0), size=(30,30), color=(255,0,0), trigger=False):
    self.points = [vec(coor[0],coor[1]), vec(coor[0]+size[0], coor[1]), vec(coor[0]+size[0], coor[1]+size[1]), vec(coor[0], coor[1]+size[1])]

    self.color = color

    self.center = self.findCenter()
    self.radius = self.getRadius()

    self.trigger = trigger

    gameObjects.append(self)

class Hitbox(Rectangle):
  def __init__(self,coor=(0,0), size=(30,30), color=(255,0,0), trigger=False):
    self.points = [vec(coor[0],coor[1]), vec(coor[0]+size[0], coor[1]), vec(coor[0]+size[0], coor[1]+size[1]), vec(coor[0], coor[1]+size[1])]

    self.color = color

    self.center = self.findCenter()
    self.radius = self.getRadius()

    self.trigger = trigger

    self.hollow = True


class Triangle():
  def __init__(self, coor=(0,0), size=5) -> None:
    self.points = []
  
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

    self.x += addX
    self.y += addY
  
  def update(self, DISPLAY):
    if self.isShown:
      game.draw.circle(DISPLAY, self.color, (self.x, self.y), self.radius)

class ParticleSystem():
  pass

class camera():
  def move(addX,addY):
    addX = -addX
    addY = -addY

    for gameObject in gameObjects:
      gameObject.move(addX, addY)

def input():
  return game.key.get_pressed()

def convertInput(code):
  return game.key.key_code(code)

def checkCollision(object1, object2=None):
  if object2 == None:
    for gameObject in gameObjects:
      if object1 != gameObject:
        result = checkCollision(object1, gameObject)
        if result == True:
          return True
    return False
  else:
    if not(object1.enabled) or not(object2.enabled): return False

    if object1.objectType == "sprite" and object1.hitbox != None:
      initX = object1.hitbox.center.x
      initY = object1.hitbox.center.y
      result = checkCollision(object1.hitbox, object2)
      deltaX = object1.hitbox.center.x - initX
      deltaY = object1.hitbox.center.y - initY
      object1.x += deltaX
      object1.y += deltaY

      return result



    if object2.objectType == "sprite" and object2.hitbox != None:
      initX, initY = object2.hitbox.center.x, object2.hitbox.center.y
      result = checkCollision(object1, object2.hitbox)
      deltaX = object2.hitbox.center.x - initX
      deltaY = object2.hitbox.center.y - initY
      object2.x += deltaX
      object2.y += deltaY

      return result

    if object1.objectType == "poly" and object2.objectType == "poly":
      return checkPolyCollision(object1, object2)
    elif object1.objectType == "circle" and object2.objectType == "circle":
      return checkCircleCollision(object1, object2)
    elif object1.objectType == "circle" and object2.objectType == "poly" or object1.objectType == "poly" and object2.objectType == "circle":
      return checkCircleToPolyCollision(object1, object2)
    else:
      return False

def checkCircleCollision(circle1, circle2):
  distance = dist(circle1.x, circle1.y, circle2.x, circle2.y)
  radii = circle1.radius + circle2.radius

  if distance < radii:

    if circle1.trigger or circle2.trigger:
      return True

    centerA = vec(circle1.x, circle1.y)
    centerB = vec(circle2.x, circle2.y)
    direction = centerB - centerA
    normal = direction.normalize()
    depth = radii-distance

    if circle2.dynamic:
      circle2.move(normal.x*depth/2, normal.y*depth/2)
      circle1.move(-normal.x*depth/2, -normal.y*depth/2)
    else:
      circle1.move(-normal.x*depth, -normal.y*depth)

    return True
  
  return False

def checkPolyCollision(poly1, poly2):
  def edgeDirection(point1, point2):
    return point2.x - point1.x, point2.y-point1.y

  def vertsToEdges(points):
    return [edgeDirection(points[i], points[(i + 1) % len(points)])for i in range(len(points))]

  def normalize(vector):
    vector = vec(vector)
    norm = math.sqrt(vector.x**2 + vector.y ** 2)
    return vector.x / norm, vector.y / norm
  
  def orthogonal(vector):
    vector = vec(vector)
    return vector.y, -vector.x

  def dot(vector1, vector2):
    vector1, vector2 = vec(vector1), vec(vector2)
    return vector1.x * vector2.x + vector1.y * vector2.y

  def project(vertices, axis):
    dots = [dot(vertex, axis) for vertex in vertices]
    return [min(dots), max(dots)]

  def overlap(projectionA, projectionB):
    return min(projectionA) <= max(projectionB) and \
           min(projectionA) <= max(projectionB)

  if dist(poly1.x, poly1.y, poly2.x, poly2.y) > poly1.radius + poly2.radius: return False

  points1 = poly1.points
  points2 = poly2.points

  edges = vertsToEdges(points1) + vertsToEdges(points2)
  axes = [normalize(orthogonal(edge)) for edge in edges]

  normal = vec(0,0)
  depth = 2147483647

  for axis in axes:
    projectA = project(points1, axis)
    projectB = project(points2, axis)

    overlapping = overlap(projectA, projectB)

    if not(overlapping):
      return False

    axisDepth = min(max(projectB) - min(projectB), max(projectA) - min(projectB))
    if axisDepth < depth:
      depth = axisDepth
      normal = axis

  if poly1.trigger or poly2.trigger:
    return True

  centerA = poly1.center
  centerB = poly2.center

  direction = centerB-centerA

  normal = vec(normal)
  if dot(direction, normal) < 0:
    normal = -normal

  if poly2.dynamic and poly1.dynamic:
    poly2.move(normal.x*depth/2,normal.y*depth/2)
    poly1.move(-normal.x*depth/2,-normal.y*depth/2)
  else:
    if not(poly1.dynamic):
      poly2.move(normal.x*depth,normal.y*depth)
    elif not(poly2.dynamic):
      poly1.move(-normal.x*depth, -normal.y*depth)
#
  return True

def checkCircleToPolyCollision(object1, object2):
  def dot(vector1, vector2):
    vector1, vector2 = vec(vector1), vec(vector2)
    return vector1.x * vector2.x + vector1.y * vector2.y

  def project(vertices, axis):
    dots = [dot(vertex, axis) for vertex in vertices]
    return [min(dots), max(dots)]

  def overlap(projectionA, projectionB):
    return min(projectionA) <= max(projectionB) and \
           min(projectionA) <= max(projectionB)

  def orthogonal(vector):
    vector = vec(vector)
    return vector.y, -vector.x

  if object1.objectType == "poly":
    poly = object1
    circle = object2
  else:
    poly = object2
    circle = object1

  #if dist(poly.center.x, poly.center.y, circle.x, circle.y) > poly.radius + circle.radius: return False

  closestPoint = 0
  for index, point in enumerate(poly.points):
    distance = dist(point.x, point.y, circle.x, circle.y)
    if index == 0: 
      minDistance = distance
    if distance < minDistance: 
      minDistance = distance
      closestPoint = index

  closestPoint = poly.points[closestPoint]

  magnitude = math.sqrt(math.pow(closestPoint.x, 2) + math.pow(closestPoint.y, 2))
  if magnitude != 0:
    axis = vec(closestPoint.x * (1/magnitude), closestPoint.y * (1/magnitude))
  
  axis = vec(orthogonal(axis))
  axis.normalize()

  temp = dot(axis, vec(circle.x, circle.y))
  circleMin = temp - circle.radius
  circleMax = temp + circle.radius

  circleProj = vec(circleMin, circleMax)


  polyProj = project(poly.points, axis)

  return overlap(circleProj, polyProj)

def fixCircleToPolyCollision(circle, poly, depth):
  pass

def fixPolyToCircleCollision(poly, circle, depth):
  pass

def dist(x1, y1, x2, y2):
  deltaX = x2-x1
  deltaY = y2-y1

  return math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))

def applyMovement(gameObject):
  netY = gameObject.forces[1]
  netX = gameObject.forces[0]

  netY += gameObject.mass*gameObject.gravity


  if gameObject.forces[1] > 0:
    gameObject.forces = (gameObject.forces[0], 0)
  gameObject.forces = (gameObject.forces[0], gameObject.forces[1] + 10)
  

  if not(gameObject.trigger):
    gameObject.move(netX,netY)
  else:
    gameObject.move(netX,netY)

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


def update(DISPLAY, deltaTime=1, background=(0,0,0)):
  global frameNumber
  frameNumber += 1

  if background != None:
    DISPLAY.fill((0,0,0))

  # O(t+g+1/2(g**2-g)+h)

  for timer in timers:
    if timer.enabled:
      timer.checkTime()

  for i in range(len(gameObjects)):

    y = i+1
    if gameObjects[i].enabled:
      if gameObjects[i].hasPhysics:
        applyMovement(gameObjects[i])

      if not(gameObjects[i].trigger):
        while y < len(gameObjects):
          if not(gameObjects[y].trigger) and gameObjects[y].enabled:
            checkCollision(gameObjects[i], gameObjects[y])
          y += 1

      if gameObjects[i].isShown:
        gameObjects[i].update(DISPLAY)

  for hudObject in hudObjects:
    if hudObject.enabled:
      if hudObject.isShown:
        hudObject.show(DISPLAY)

  game.display.update()
