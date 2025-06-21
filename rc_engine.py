import math
import pygame

class Raycaster():
    def __init__(self, screen, map):
        self.x = 0
        self.y = 0  
        self.angle = 0
        self.fov = 0
        self.map = map
        self.screen=screen
    
    def update_state(self, x, y, angle, fov):
        self.x = x
        self.y = y
        self.angle = angle
        self.fov = fov
    def castray(self, rayangle):
        x, y = self.x, self.y   #current (x,y) of the ray
        dx = math.cos(rayangle) #Direction (NOT distance), cos=breadth/hypotenuse
        dy = math.sin(rayangle) #Direction (NOT distance), sin=perpendicular/hypotenuse

        for i in range(400):    #Breaking the loop, if ray continues increasing without hitting anything
            map_x, map_y = int(x), int(y)
            if self.map[map_y][map_x] == 1:
                distance = math.sqrt((x-self.x)**2 + (y-self.y)**2) #Standard distance formula
                try:
                    wallheight = min(600, int(600 / (distance)))
                except ZeroDivisionError:   #screenheight/distance can lead to division by 0
                    continue
                return distance, wallheight
            #Moves the ray head by a step of 0.02 in the same direction as dx
            x += dx * 0.02 
            y += dy * 0.02
        
        return 400, 1

    def drawwallslice(self, i, wallheight, slicewidth, distance):
        sim_renderdist=35   #Simulates render distance, works inversely
        color = max(0, min(255, int(255 - distance * sim_renderdist)))  #Faraway, darker colours
        pygame.draw.rect(self.screen, (color, 0, color), #(R,G,B)
                         (i * slicewidth, 300-wallheight//2,    #left, top (counts pixels from top), width, height
                          slicewidth, wallheight))
    
    def raycast(self):
        rays = 200
        screenwidth = 800
        slicewidth = screenwidth / rays

        for i in range(rays):
            '''
            self.angle - (self.fov/2) gives leftmost angle of the players vision
            i/rays is the offset from the left most side of the vision
            multiply i/rays * self.fov to scale the offset to our vision
            '''
            rayangle = self.angle - (self.fov/2) + (i / rays) * self.fov    #rayangle gives direction ray is pointing towards
            distance, wallheight = self.castray(rayangle)
            self.drawwallslice(i, wallheight, slicewidth, distance)