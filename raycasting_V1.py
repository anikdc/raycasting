import pygame
import math
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
running = True

class Raycaster():
    def __init__(self):
        self.x = 1.5
        self.y = 1.5
        self.angle = 0
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
        x, y = self.x, self.y
        dx = math.cos(rayangle)
        dy = math.sin(rayangle)

        for i in range(400):
            map_x, map_y = int(x), int(y)
            if self.map[map_y][map_x] == 1:
                distance = math.sqrt((x-self.x)**2 + (y-self.y)**2)
                wallheight = min(600, int(600 / (distance + 0.00001)))
                return distance, wallheight
            x += dx * 0.02
            y += dy * 0.02
        
        return 400, 1

    def raycast(self):
        rays = 200
        screenwidth = 800
        slicewidth = screenwidth / rays

        for i in range(rays):
            rayangle = self.angle - (self.fov/2) + (i / rays) * self.fov
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
            self.x += math.cos(self.angle) * speed
            self.y += math.sin(self.angle) * speed
        if keys[K_DOWN]:
            self.x -= math.cos(self.angle) * speed
            self.y -= math.sin(self.angle) * speed

    def drawwallslice(self, i, wallheight, slicewidth, distance):
        color = max(0, min(255, int(255 - distance * 20)))
        pygame.draw.rect(screen, (color, 0, color), 
                         (i * slicewidth, 300 - wallheight // 2, 
                          slicewidth + 1, wallheight))


raycaster = Raycaster()

font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    raycaster.updateplayer()
    
    screen.fill((0, 0, 0))
    raycaster.raycast()
    
    debug_text = f"Pos: ({raycaster.x:.2f}, {raycaster.y:.2f}), Angle: {raycaster.angle:.2f}"
    text_surface = font.render(debug_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))
    
    pygame.display.flip()
    clock.tick(60) 

pygame.quit()



