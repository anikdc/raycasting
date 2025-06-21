import math
import pygame

class Minimap():
    def __init__(self, player_img, screen, map):
        self.x = 0
        self.y = 0  
        self.angle = 0
        self.map = map
        self.img=player_img
        self.screen=screen
        self.mapx=9
        self.mapy=10
        self.k=20

    def update_state(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def drawminimap(self):
        for i in range(self.mapy):
            for j in range(self.mapx):
                #left, top (counts pixels from top), width, height
                if self.map[i][j]==1: #White pixels, cannot go 
                    pygame.draw.rect(self.screen, (255,255,255), (j*self.k, i*self.k, self.k, self.k))
                else:   #Black pixels, can pass through
                    pygame.draw.rect(self.screen, (0,0,0), (j*self.k, i*self.k, self.k, self.k))
    
    def drawplayer(self, x,y,angle):
        self.drawminimap()
        transformed_img = pygame.transform.rotate(self.img, -math.degrees(angle))
        rect=transformed_img.get_rect()
        rect.center=(self.x*self.k,self.y*self.k)
        self.screen.blit(transformed_img, rect) #image to draw, position to draw (top-left)
    
