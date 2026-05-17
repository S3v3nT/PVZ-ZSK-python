import pygame
import os
from random import randint
pygame.init()
window = pygame.display.set_mode((1400,600))
print("Aktualny katalog roboczy:", os.getcwd())
print("Katalog skryptu:", os.path.dirname(os.path.abspath(__file__)))
scriptDir = os.path.dirname(os.path.abspath(__file__))

class uczenZSK:
    def __init__(self):
        self.x_cord = 0
        self.y_cord = 0
        self.image = pygame.image.load(os.path.join(scriptDir, 'assets', 'dave.png'))
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
    def draw(self): 
        window.blit(self.image,(self.x_cord, self.y_cord))
    def move(self, keys):
        speed = 6
        if keys[pygame.K_w]:
            self.y_cord -=speed
        if keys[pygame.K_s]:
            self.y_cord +=speed
        if keys[pygame.K_a]:
            self.x_cord -=speed
        if keys[pygame.K_d]:
            self.x_cord +=speed
        
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

class peashooter:
    def __init__(self):
        self.x_cord = 100
        self.y_cord = 100
        self.image = pygame.image.load(os.path.join(scriptDir, 'assets', 'peashooterZsk.png'))
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
    def draw(self):
        window.blit(self.image,(self.x_cord, self.y_cord))

def main():
    run = True
    player = uczenZSK()
    defender = peashooter()
    clock = pygame.time.Clock()
    background = pygame.image.load(os.path.join(scriptDir, 'assets', 'ogrod.jpg'))
    
    while run:
        clock.tick(60) 
        
        pygame.time.Clock().tick(60)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False
        
        keys = pygame.key.get_pressed()
        
        player.move(keys)
        
        window.blit(background,(0,0))
        player.draw()
        defender.draw()
        pygame.display.update()

if __name__== "__main__":
    main()