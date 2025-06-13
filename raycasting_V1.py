import pygame
import math

from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
running = True

class Raycaster():
    def __init__(self):
        self.x = 1.5    #X coordinate of the player
        self.y = 1.5    #Y coordinate of the player
        '''
        if the ray is pointing directly at the center of the screen i.e straight-up
        then rayangle=self.angle
        '''
        self.angle = 0  #Initial angle of the player
        self.fov = math.pi/3
        self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 1, 0, 1, 0, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 1, 1, 0, 1, 0, 0, 1],
                    [1, 0, 1, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 1, 0, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 1, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1]]
    
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
        
    def updateplayer(self):
        speed = 0.05
        angularspeed = 0.05
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.angle -= angularspeed
        if keys[K_RIGHT]:
            self.angle += angularspeed
        if keys[K_UP]:
            #Change code here to make sure it doesn't clip through walls
            self.x += math.cos(self.angle) * speed
            self.y += math.sin(self.angle) * speed
        if keys[K_DOWN]:
            self.x -= math.cos(self.angle) * speed
            self.y -= math.sin(self.angle) * speed
        '''     
        if keys[K_w]:
            self.fov+=speed
        if keys[K_s]:
            self.fov-=speed
        '''
    def drawwallslice(self, i, wallheight, slicewidth, distance):
        sim_renderdist=35   #Simulates render distance, works inversely
        color = max(0, min(255, int(255 - distance * sim_renderdist)))  #Faraway, darker colours
        pygame.draw.rect(screen, (color, 0, color), #(R,G,B)
                         (i * slicewidth, 300-wallheight//2,    #left, top (counts pixels from top), width, height
                          slicewidth, wallheight))
        '''
        i is the current ray, 
        '''

raycaster = Raycaster()

font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    raycaster.updateplayer()
    
    screen.fill((0, 0, 0))
    '''
    pygame.draw.rect(screen, (0,255,0), (0,300,800,300)) #Sky
    pygame.draw.rect(screen, (0,0,255), (0,0,800,300)) #Ground
    '''
    raycaster.raycast()
    
    debug_text = f"Pos: ({raycaster.x:.2f}, {raycaster.y:.2f}), Angle: {raycaster.angle:.2f}"
    screen.blit(text_surface, (10, 10))
    
    text_surface = font.render(debug_text, True, (255, 255, 255))
    pygame.display.flip()
    clock.tick(60) 

pygame.quit()



