import pygame
import os
from random import randint
pygame.init()
window = pygame.display.set_mode((1400,600))
print("Aktualny katalog roboczy:", os.getcwd())
print("Katalog skryptu:", os.path.dirname(os.path.abspath(__file__)))
scriptDir = os.path.dirname(os.path.abspath(__file__))

class uczenZSL:
    def __init__(self):
        self.x_cord = 0
        self.y_cord = 0
        self.image = pygame.image.load(os.path.join(scriptDir, 'assets', 'peashooterZsk.jpg'))
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
    def draw(self): 
        window.blit(self.image,(self.x_cord, self.y_cord))

def main():
    run = True
    zombie = uczenZSL()
    clock = pygame.time.Clock()
    background = pygame.image.load(os.path.join(scriptDir, 'assets', 'ogrod.jpg'))
    
    while run:
        clock.tick(60) 
        
        pygame.time.Clock().tick(60)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False
        
        window.blit(background,(0,0))
        zombie.draw()
        pygame.display.update()

if __name__== "__main__":
    main()