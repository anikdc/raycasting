import pygame
import math
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
running = True

x=1.5
y=1.5
angle=0
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

mapx=9
mapy=10
k=20
def drawminimap():
    for i in range(mapy):
        for j in range(mapx):
            #left, top (counts pixels from top), width, height
            if map[i][j]==1: #White pixels, cannot go 
                pygame.draw.rect(screen, (255,255,255), (j*k, i*k, k, k))
            else:   #Black pixels, can pass through
                pygame.draw.rect(screen, (0,0,0), (j*k, i*k, k, k))

def updateplayer(x, y, angle, screen, font):
    speed = 0.05
    angularspeed = 0.05
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        angle -= angularspeed
    if keys[pygame.K_RIGHT]:
        angle += angularspeed
    if keys[pygame.K_UP]:
        if map[int(y)][int(x + math.cos(angle) * speed)] != 1:
            x += math.cos(angle) * speed
        if map[int(y + math.sin(angle) * speed)][int(x)] != 1:
            y += math.sin(angle) * speed
    if keys[pygame.K_DOWN]:
        if map[int(y)][int(x - math.cos(angle) * speed)] != 1:
            x -= math.cos(angle) * speed
        if map[int(y - math.sin(angle) * speed)][int(x)] != 1:
            y -= math.sin(angle) * speed

    coord_text = f"x: {x:.2f}, y: {y:.2f}"
    text_surface = font.render(coord_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.topright = (screen.get_width() - 10, 10)
    screen.blit(text_surface, text_rect)

    return x, y, angle

def drawplayer(img,x,y,angle):
    transformed_img = pygame.transform.rotate(img, -math.degrees(angle))
    rect=transformed_img.get_rect()
    rect.center=(x*k,y*k)
    screen.blit(transformed_img, rect) #image to draw, position to draw (top-left)
    
player_img = pygame.transform.scale_by((pygame.image.load("resources/miniplayer_sprite.png").convert_alpha()),0.15)
font = pygame.font.SysFont(None, 24)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))

    x,y,angle=updateplayer(x,y,angle,screen,font)

    drawminimap()
    drawplayer(player_img,x,y,angle)

    pygame.display.flip()
    clock.tick(60) 
pygame.quit()
