import math
import pygame
import rc_engine
from pygame.locals import *

x=1.5   #X coordinate of the player
y=1.5   #Y coordinate of the player
angle=0 #Initial angle of the player
fov=math.pi/3
map=[[1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 0, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 1, 0, 1, 0, 1, 1, 1],
     [1, 0, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 1, 1, 0, 1, 0, 0, 1],
     [1, 0, 1, 0, 0, 1, 0, 0, 1],
     [1, 0, 0, 1, 0, 1, 1, 1, 1],
     [1, 0, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 1, 0, 0, 0, 0, 0, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1]]

pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

raycaster = rc_engine.Raycaster(screen, map)
running = True


def updateplayer():
    global x, y, angle
    speed = 0.05
    angularspeed = 0.05
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        angle -= angularspeed
    if keys[K_RIGHT]:
        angle += angularspeed
    if keys[K_UP]:
        #Doesn't clip through walls
        if map[int(y)][int(x+math.cos(angle) * speed)] != 1:
            x += math.cos(angle) * speed
        if map[int(y+math.sin(angle) * speed)][int(x)] != 1:
            y += math.sin(angle) * speed
    if keys[K_DOWN]:
        if map[int(y)][int(x-math.cos(angle) * speed)] != 1:
            x -= math.cos(angle) * speed
        if map[int(y-math.sin(angle) * speed)][int(x)] != 1:
            y -= math.sin(angle) * speed
    '''     
    if keys[K_w]:
        fov+=speed
    if keys[K_s]:
        fov-=speed
    '''
    raycaster.update_state(x,y,angle, fov)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    updateplayer()

    screen.fill((0, 0, 0))
    #'''
    pygame.draw.rect(screen, (0,255,0), (0,300,800,300)) #Sky
    pygame.draw.rect(screen, (0,0,255), (0,0,800,300)) #Ground
    #'''
    raycaster.raycast()
    debug_text = f"Pos: ({raycaster.x:.2f}, {raycaster.y:.2f}), Angle: {raycaster.angle:.2f}"
    text_surface = font.render(debug_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))
    fps = clock.get_fps()                            
    screen.blit(font.render(f"FPS: {fps:.1f}", True, (255,255,0)), (10,40)) 

    pygame.display.flip()
    clock.tick(60) 

pygame.quit()

