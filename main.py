import pygame
import os
from random import randint, choice
pygame.init()
window = pygame.display.set_mode((1400,600))
print("Aktualny katalog roboczy:", os.getcwd())
print("Katalog skryptu:", os.path.dirname(os.path.abspath(__file__)))
scriptDir = os.path.dirname(os.path.abspath(__file__))

class peashooter:
    def __init__(self, x_cord=200, y_cord=60):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.image = pygame.image.load(os.path.join(scriptDir, 'assets', 'peashooterZsk.png'))
        self.image = pygame.transform.scale(self.image, (100, 100))  # width, height
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
        self.image = pygame.transform.scale(self.image, (30, 30))  # width, height
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
    
    def update(self):
        self.move()
        if self.isOffscreen():
            return True
        return False

class zombie:
    def __init__(self, y_cord):
        self.x_cord = 1400
        self.y_cord = y_cord
        self.image = pygame.image.load(os.path.join(scriptDir, 'assets', 'zombie.png'))
        self.image = pygame.transform.scale(self.image, (75, 125))  # width, height
        self.hp = 100
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
    def draw(self):
        window.blit(self.image,(self.x_cord, self.y_cord))
    def move(self):
        self.x_cord -= 0.5
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

def main():
    placing_peashooter = False
    lanes = [50, 150, 250, 350, 450]
    run = True
    peashooters = []  # Start with one peashooter
    peaballs = []
    zombies = []
    score = 0
    peashooter_card = pygame.image.load(os.path.join(scriptDir, 'assets', 'peashooterCard.png'))
    peashooter_card = pygame.transform.scale(peashooter_card, (80, 100))  # Adjust size as needed
    card_rect = peashooter_card.get_rect(topleft=(20, 100))  # Position it (x, y)
    font = pygame.font.SysFont(None, 36)
    bigFont = pygame.font.SysFont(None, 70)
    
    clock = pygame.time.Clock()
    
    background = pygame.image.load(os.path.join(scriptDir, 'assets', 'ogrod.jpg'))
    
    shoot_cooldown = 0
    shoot_rate = 45
    
    scoreCooldown = 0
    scoreRate = 30
    
    zombie_cooldown = 0
    zombie_rate = 60
    
    while run:
        clock.tick(60) 
        
        pygame.time.Clock().tick(60)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
               if card_rect.collidepoint(event.pos):
                   placing_peashooter = True  # Activate placement mode
               elif placing_peashooter:  # Click on lanes to place
                   mouse_x, mouse_y = event.pos
                   for lane_y in lanes:
                       if abs(mouse_y - lane_y) < 50:  # Within lane range
                           # Check if already has peashooter in this lane
                           already_placed = False
                           for pea in peashooters:
                               if abs(pea.y_cord - lane_y) < 50:
                                   already_placed = True
                                   break
                           
                           if not already_placed:
                               peashooters.append(peashooter(240, lane_y))
                           
                           placing_peashooter = False
                           break
        
        keys = pygame.key.get_pressed()
        
        if shoot_cooldown > 0:
            shoot_cooldown -= 0.5
        
        if shoot_cooldown == 0:
            for pea in peashooters:
                # Check if any zombie is in this peashooter's lane
                for zomb in zombies:
                    if abs(zomb.y_cord - pea.y_cord) < 100:  # Within lane range
                        peaballs.append(peaBall(pea))
                        break  # Only shoot once per peashooter
            shoot_cooldown = shoot_rate
        # Spawn zombies
        if zombie_cooldown > 0:
            zombie_cooldown -= 0.5
        
        if zombie_cooldown == 0:
            zombies.append(zombie(choice(lanes)))
             # Adjust rate based on score
            zombie_rate = max(20, 100 - (score // 100))
            zombie_cooldown = zombie_rate
        
        # Update peaballs and check collision with zombies
        for peaball in peaballs[:]:
            is_offscreen = peaball.update()

            if is_offscreen:
                if peaball in peaballs:
                    peaballs.remove(peaball)
                continue
            
            # Check collision with zombies
            for zomb in zombies[:]:
                if peaball.hitbox.colliderect(zomb.hitbox):
                    zomb.hp -= 25
                    if zomb.hp <= 0:
                        zombies.remove(zomb)
                        score += 100
                    if peaball in peaballs:
                        peaballs.remove(peaball)
                    break
        
        # Move zombies
        for zomb in zombies[:]:
            zomb.move()
            if zomb.x_cord < 0:
                if zomb in zombies:
                    zombies.remove(zomb)
        
        if scoreCooldown > 0:
            scoreCooldown -= 1
        
        if scoreCooldown == 0:
            score += 1
            scoreCooldown = scoreRate
            
        window.blit(background,(0,0))
        window.blit(peashooter_card, card_rect)
        
        for peaball in peaballs:
            peaball.draw()
        
        for zomb in zombies:
            zomb.draw()
        
        for peaball in peaballs:
            pygame.draw.rect(window, (0, 100, 255), peaball.hitbox, 2)
        
        for zomb in zombies:
            pygame.draw.rect(window, (0, 255, 0), zomb.hitbox, 2)
        
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(score_text, (20, 20))
        
        for pea in peashooters:
            pea.draw()
        
        if placing_peashooter:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if cursor is in any lane
            
            for lane_y in lanes:
                if abs(mouse_y - lane_y) < 50:  # Within lane range
                    preview_image = pygame.image.load(os.path.join(scriptDir, 'assets', 'peashooterZsk.png'))
                    preview_image = pygame.transform.scale(preview_image, (100, 100))
                    preview_image.set_alpha(128)  # 50% transparent
                    window.blit(preview_image, (240, lane_y))  # Show at placement position
                    break
        
        pygame.display.update()

if __name__== "__main__":
    main()