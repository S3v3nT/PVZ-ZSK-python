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
        self.x_cord = 200
        self.y_cord = 60
        self.image = pygame.image.load(os.path.join(scriptDir, 'assets', 'peashooterZsk.png'))
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
    def draw(self):
        window.blit(self.image,(self.x_cord, self.y_cord))

class peaBall:
    def __init__(self, peashooter):
        self.peashooter = peashooter
        self.x_cord = peashooter.x_cord + peashooter.width - 20
        self.y_cord = peashooter.y_cord + 25
        self.image = pygame.image.load(os.path.join(scriptDir, 'assets', 'peaBall.png'))
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        
    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))
    
    def move(self):
        self.x_cord += 8
    
    def isOffscreen(self):
        return self.x_cord > 1450


def main():
    run = True
    player = uczenZSK()
    defender = peashooter()
    peaballs = []
    
    clock = pygame.time.Clock()
    
    background = pygame.image.load(os.path.join(scriptDir, 'assets', 'ogrod.jpg'))
    
    shoot_cooldown = 0
    shoot_rate = 45
    
    while run:
        clock.tick(60) 
        
        pygame.time.Clock().tick(60)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False
        
        keys = pygame.key.get_pressed()
        
        player.move(keys)
        
        if shoot_cooldown > 0:
            shoot_cooldown -= 1
        
        if shoot_cooldown == 0:
            peaballs.append(peaBall(defender))
            shoot_cooldown = shoot_rate
        
        if clock == 1:
            clock = 0
            peaballs.append(peaBall(defender))
        
        for peaball in peaballs[:]:
            peaball.move()
            if peaball.isOffscreen():
                peaballs.remove(peaball)
        
        window.blit(background,(0,0))
        for peaball in peaballs:
            peaball.draw()
        defender.draw()
        player.draw()
        pygame.display.update()

if __name__== "__main__":
    main()