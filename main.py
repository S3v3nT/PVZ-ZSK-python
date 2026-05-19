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
        
        self.hp = 100
        
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
        
        self.x_cord = max(0, min(self.x_cord, 1400 - self.width))
        self.y_cord = max(0, min(self.y_cord, 600 - self.height))
        
        self.hitbox = pygame.Rect(self.x_cord + 10, self.y_cord + 10, self.width - 20, self.height - 20)
        
    def getHP(self):
        return self.hp
    
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

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
        
        self.hitbox = pygame.Rect(self.x_cord + 5, self.y_cord + 5, self.width - 12, self.height - 12)
        
    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))
    
    def move(self):
        self.x_cord += 2
        self.hitbox = pygame.Rect(self.x_cord + 5, self.y_cord + 5, self.width - 12, self.height - 12)
    
    
    def isOffscreen(self):
        return self.x_cord > 1450
    
    def update(self, player):
        steps = 5
        step_size = 8.0 / steps

        for _ in range(steps):
            self.x_cord += step_size
            self.hitbox.x = self.x_cord + 4
            self.hitbox.y = self.y_cord + 4

            if player.hitbox.colliderect(self.hitbox):
                player.take_damage(25)
                return True
        return False


def main():
    run = True
    playerAlive = True
    player = uczenZSK()
    defender = peashooter()
    peaballs = []
    score = 0
    
    font = pygame.font.SysFont(None, 36)
    bigFont = pygame.font.SysFont(None, 70)
    
    clock = pygame.time.Clock()
    
    background = pygame.image.load(os.path.join(scriptDir, 'assets', 'ogrod.jpg'))
    
    shoot_cooldown = 0
    shoot_rate = 45
    
    scoreCooldown = 0
    scoreRate = 30
    
    while run:
        clock.tick(60) 
        
        pygame.time.Clock().tick(60)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False
        
        if player.hp <= 0:
            playerAlive = False
        
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
            hit = peaball.update(player)

            if hit or peaball.x_cord > 1450:
                peaballs.remove(peaball)
        
        for peaball in peaballs[:]:
            peaball.move()
            if peaball.isOffscreen():
                peaballs.remove(peaball)
        
        if scoreCooldown > 0:
            scoreCooldown -= 1
        
        if scoreCooldown == 0:
            if player.hp > 0:
                score += 1
                scoreCooldown = scoreRate
        
        window.blit(background,(0,0))
        
        if playerAlive:
            for peaball in peaballs:
                peaball.draw()
            
            pygame.draw.rect(window, (255, 0, 0), player.hitbox, 2)
            for peaball in peaballs:
                pygame.draw.rect(window, (0, 100, 255), peaball.hitbox, 2)
            
            hp_text = font.render(f"HP: {player.hp}", True, (255, 255, 255))
            window.blit(hp_text, (20, 20))
            
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            window.blit(score_text, (20, 60))
            
            defender.draw()
            
            if player.hp > 0:
                player.draw()
        
        if playerAlive == False:
            gameOverText = bigFont.render(f"Game over :(", True, (0, 0, 0))
            window.blit(gameOverText, (500, 200))
            window.blit(score_text, (600, 300))
        pygame.display.update()

if __name__== "__main__":
    main()