import pygame as pg
import traceback
from math import pi, sin, cos
 
 
W_WIDTH = 800
W_HEIGHT = 600
FPS = 60
TWO_PI = pi * 2
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
 
vec = pg.math.Vector2
 
def construct_hexagon(center, size, rotation=0):
    # construct a hexagon from a given center and radius
    points = []
    for i in range(6):
        angle_deg = 60 * i - rotation
        angle_rad = pi / 180 * angle_deg
        points.append(vec(center.x + size * cos(angle_rad),
                         center.y + size * sin(angle_rad)))
    return points
 
 
def vec_to_int(vec):
    return (int(vec.x), int(vec.y))
 
 
 
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((W_WIDTH, W_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        
        self.shapes = []
        # create a hexagon (controll with WASD)
        Shape(self, points=construct_hexagon(vec(400, 300), 80), 
                        control='WASD')
        # create a triangle (controll with the arrow keys)
        tri = Shape(self, points=[vec(500, 500), vec(440, 460), vec(440, 540)],
                                 control='ARROW')
        tri.move_to((300, 100))
        
        # create a trapezoid (can't be controlled)
        trap = Shape(self, points=[vec(40, 10), vec(0, 170), vec(300, 170), vec(260, 10)])
        trap.move_to((400, 500))
        
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
    
    
    def update(self, dt):
        for shape in self.shapes:
            shape.update(dt)
       
        
    def draw(self):
        self.screen.fill(BLACK)
        for shape in self.shapes:
            shape.draw(self.screen)
        pg.display.update()
        
        
    def run(self):
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update(delta_time)
            self.draw()
        pg.quit()
        
 
 
class Shape:
    '''
    This class constructs a polygon from any number of given vectors
    '''
    def __init__(self, game, points, control='None'):
        self.game = game
        self.game.shapes.append(self)
        self.points = points
        self.center = self.find_center()
        self.vel = vec()
        self.rotation = 0
        self.speed = 200 # dont need
        self.control = control # dont need
        self.overlap = False # trigger
        
        self.edges = [Line(self.points[i], self.points[i + 1]) 
                      for i in range(-1, len(self.points) - 1)]
        self.diagonals = [Line(self.center, p) for p in self.points]
        
    
    def update(self, dt):       
        if self.control != 'None':
            keys = pg.key.get_pressed()
            if self.control == 'WASD':
                rot = keys[pg.K_d] - keys[pg.K_a]
                move = keys[pg.K_w] - keys[pg.K_s]
            elif self.control == 'ARROW':
                rot = keys[pg.K_RIGHT] - keys[pg.K_LEFT]
                move = keys[pg.K_UP] - keys[pg.K_DOWN]
            
            # rotate
            angle = pi * rot * dt
            self.rotation += angle
            self.rotate(angle)
            # move
            self.vel.x += move * dt * self.speed
            self.vel = self.vel.rotate(self.rotation * 360 / TWO_PI)
            self.move(self.vel)
            self.vel *= 0
        
        # construct edges and diagonals based on the new coordinates
        self.edges = [Line(self.points[i], self.points[i + 1]) 
                      for i in range(-1, len(self.points) - 1)]
        self.diagonals = [Line(self.center, p) for p in self.points]
        
        for shape in self.game.shapes:
            # check for collisions with the other shapes
            if shape != self and self.shape_overlap(shape):
                self.overlap = True
                shape.overlap = True
    
    
    def rotate(self, angle):
        # rotate the edges around the shape's center
        for point in self.points:
            # translate the center to the origin
            point -= self.center
            # rotate point around the origin
            original_x = point.x
            original_y = point.y
            point.x = original_x * cos(angle) - original_y * sin(angle)
            point.y = original_y * cos(angle) + original_x * sin(angle)
            # translate back to shape's center
            point += self.center
    
    
    def draw(self, screen):
        # change color based on collision check
        if self.overlap: 
            color = RED
        else:
            color = WHITE
        pg.draw.polygon(screen, color, self.points, 2)
        # pg.draw.polygon(screen, color, self.points) for solid shapes
        pg.draw.line(screen, color, self.center, self.points[0])
        '''
        # for debugging
        for diag in self.diagonals:
            diag.draw(screen, color)
        for edge in self.edges:
            edge.draw(screen, color)
        '''
        # reset the overlap flag after all collisions are checked
        self.overlap = False
        
        
    def find_center(self):
        # calculate geometric center (centroid) as mean of all points
        # https://en.wikipedia.org/wiki/Centroid
        p_sum = vec()
        for p in self.points:
            p_sum += p
        return p_sum / len(self.points)
    
    
    def move(self, amount):
        # move all points of this shape by a given vector
        self.center += amount
        for point in self.points:
                point += amount
    
    
    def move_to(self, position):
        # move the center to a given position and change all points accordingly
        # just a convenience function, could possibly be refactored
        old_center = self.center
        self.center = position
        amount = position - old_center
        for point in self.points:
                point += amount
                
    
    def shape_overlap(self, other):
        # https://github.com/OneLoneCoder/olcPixelGameEngine/blob/master/OneLoneCoder_PGE_PolygonCollisions1.cpp
        # check if the diagonals of this shape overlap any of the edges of 
        # the other shape. If true, move this shape's points by the
        # displacement vector that gets modified by the intersects_line function
        for diag in self.diagonals:
            for edge in other.edges:
                displacement = vec()
                if diag.intersects_line(edge, displacement):
                    self.move(displacement)
                    return True
        return False
        
 
 
class Line:
    '''
    custom Line class that represents a line with a start and end vector
    and provides a method for intersection checking
    '''
    def __init__(self, start, end):
        self.start = vec(start)
        self.end = vec(end)
    
    
    def draw(self, screen, color=WHITE, width=1):
        pg.draw.line(screen, color, self.start, self.end, width)
        
        
    def intersects_line(self, other, displacement):
        # http://www.jeffreythompson.org/collision-detection/line-rect.php
        # check if two Line objects intersect
        # if true, change the displacement vector by the distance between
        # this line's end and the intersection
        denA = ((other.end.y - other.start.y) * (self.end.x - self.start.x) - 
                (other.end.x - other.start.x) * (self.end.y - self.start.y))
        denB = ((other.end.y - other.start.y) * (self.end.x - self.start.x) - 
                (other.end.x - other.start.x) * (self.end.y - self.start.y))
        if denA == 0 or denB == 0:
            return False
        else:
            numA = ((other.end.x - other.start.x) * (self.start.y - other.start.y) - 
                    (other.end.y - other.start.y) * (self.start.x - other.start.x))
            numB = ((self.end.x - self.start.x) * (self.start.y - other.start.y) - 
                    (self.end.y - self.start.y) * (self.start.x - other.start.x))
            uA = numA / denA
            uB = numB / denB
            if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
                displacement.x -= (1.0 - uA) * (self.end.x - self.start.x)
                displacement.y -= (1.0 - uA) * (self.end.y - self.start.y)
                return True
            else:
                return False
    
    
    
if __name__ == '__main__':
    try:
        g = Game()
        g.run()
    except:
        traceback.print_exc()
        pg.quit()
