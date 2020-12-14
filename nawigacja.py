'''
In this program you can use the mouse to make a red dot on the black canvas and
as soon as the dor is there, an arrow will proceed in the dot's direction.
You can change the position of the dot as many times as you will by clicking at a
different spot. Then the arrow will always point itself towards the dot.
If the arrow reaches the dot, then the program halts.
'''


import pygame
import random
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, KEYDOWN, K_ESCAPE, RLEACCEL, K_SPACE
import time
import math


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SPEED = 1

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
surf_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

clock = pygame.time.Clock()
pygame.init()



class Destination(pygame.sprite.Sprite):
    def __init__(self, location=surf_center):
        super(Destination,self).__init__()
        self.location = location
    def display(self):
        pygame.draw.circle(screen, (255,0,0), circle.location, 10)


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, bearing,location = surf_center):
        super(Vehicle, self).__init__()
        self.bearing = bearing
        self.location = location
        self.center = (self.location[0]+15,self.location[1]+15)
        self.surf = pygame.image.load("arrow.png").convert()


    def rotate(self, angle):
        old_surf = self.surf.copy()
        old_surf.fill((0,0,0))
        screen.blit(old_surf, self.location)
        pygame.display.flip()

        new_surf = pygame.image.load("arrow.png").convert()
        new_surf = pygame.transform.rotate(new_surf, angle + self.bearing)   
        new_surf = pygame.transform.scale(new_surf, (30,30))

        self.surf = new_surf

        screen.blit(self.surf, self.location)
        pygame.display.flip()
        self.bearing += angle
        


    def move(self, vector):
        pygame.draw.rect(screen, (0,0,0), self.location+(30,30))
        new_location = tuple([sum(x) for x in zip(self.location, vector)])
        self.location = new_location
        self.center = (self.location[0]+15,self.location[1]+15)
        screen.blit(self.surf, self.location)


circles = pygame.sprite.Group()
vehicle = Vehicle(0)
vehicle.move((0,0))


all_sprites = pygame.sprite.Group()
all_sprites.add(vehicle)

def distance(t1, t2):
    return ((t1[0]-t2[0])**2+(t1[1]-t2[1])**2)**0.5

def calc_angle(vec):
    vector = (vec[0], -vec[1])
    if vector[0] == 0 and vector[1] == 0:
        return 0
    try:
        angle = math.atan(vector[1]/vector[0])*180/math.pi
    except ZeroDivisionError:
        if vector[1]>0:
            return 90
        else:
            return 270
        
    if vector[0] >= 0 and vector[1]>0:
        return angle
    elif vector[0] >= 0 and vector[1]<0:
        return 360 + angle
    else:
        return 180 + angle
    
        
running = True
while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False


    if pygame.mouse.get_pressed() != (0,0,0):
        for c in circles:
            pygame.draw.circle(screen, (0,0,0), c.location, 10)
            c.kill()
            
        circle = Destination(pygame.mouse.get_pos())
        all_sprites.add(circle)
        circles.add(circle)
        circle.display()
        
    try:   
        vector = (circle.location[0]-vehicle.center[0], circle.location[1]-vehicle.center[1])
        norm = sum([abs(x)**2 for x in vector])
        norm = norm**0.5
        if norm != 0:
            vector = (SPEED*vector[0]/norm, SPEED*vector[1]/norm)
       
        angle =calc_angle(vector) - vehicle.bearing
       
        if abs(angle)>=3:
            vehicle.rotate(angle)
            print(vehicle.bearing, calc_angle(vector), vector)
        
        
        vehicle.move(vector)
        if distance(vehicle.center, circle.location)<5:
             running = False
    except NameError:
        pass
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()


