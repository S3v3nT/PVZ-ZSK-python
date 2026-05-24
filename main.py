import pygame
import os
from random import randint, choice
pygame.init()
window = pygame.display.set_mode((1400,600))
print("Aktualny katalog roboczy:", os.getcwd())
print("Katalog skryptu:", os.path.dirname(os.path.abspath(__file__)))
scriptDir = os.path.dirname(os.path.abspath(__file__))

class peashooter:
    def __init__(self, x_cord, y_cord):
        self.shoot_cooldown = 0
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.image = pygame.image.load(os.path.join(scriptDir, 'assets', 'peashooterZsk.png'))
        self.image = pygame.transform.scale(self.image, (80, 80))  # width, height
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
        self.x_cord += 3
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
        self.image = pygame.transform.scale(self.image, (75, 125))
        
        self.hp = 200
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
    
    def draw(self):
        window.blit(self.image,(self.x_cord, self.y_cord))
    
    def move(self):
        self.x_cord -= 0.5
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
    
def get_wave_count(elapsed_time):
    """Return how many zombies to spawn based on game time"""
    if elapsed_time < 10:
        return 0
    if elapsed_time < 30 and elapsed_time > 10:
        return 1  # Wave 1: 1 zombie (10-30 seconds)
    elif elapsed_time < 60:
        return 2  # Wave 2: 2 zombies (30-60 seconds)
    elif elapsed_time < 120:
        return 3  # Wave 3: 3 zombies (60-120 seconds)
    elif elapsed_time < 180:
        return 4
    elif elapsed_time < 240:
        return 5
    else:
        return randint(6, 10)  # Wave 4+: random 4-7 zombies (180+ seconds)

class Sunflower:
    def __init__(self, x_cord, y_cord):
        self.production_cooldown = 0
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.image = pygame.image.load(os.path.join(scriptDir, 'assets', 'sunflowerZsk.png'))
        self.image = pygame.transform.scale(self.image, (80, 80))  # width, height
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))

def main():
    placing_peashooter = False
    elapsed_time = 0  # Track seconds elapsed
    # 9x5 tile grid system
    tile_cols = 9
    tile_rows = 5
    tile_width = 80
    tile_height = 100
    grid_start_x = 250
    grid_start_y = 50
    
    # Generate all tile positions
    tile_positions = {}  # (col, row) -> (x, y)
    for col in range(tile_cols):
        for row in range(tile_rows):
            x = grid_start_x + col * tile_width
            y = grid_start_y + row * tile_height
            tile_positions[(col, row)] = (x, y)
    
    occupied_tiles = {}  # (col, row) -> peashooter object
    
    run = True
    game_over = False
    peaballs = []
    zombies = []
    score = 0
    sunCurrency = 25
    
    peashooter_card = pygame.image.load(os.path.join(scriptDir, 'assets', 'peashooterCard.png'))
    peashooter_card = pygame.transform.scale(peashooter_card, (80, 100))
    peaShooterCard_rect = peashooter_card.get_rect(topleft=(20, 100))
    
    font = pygame.font.SysFont(None, 36)
    bigFont = pygame.font.SysFont(None, 70)
    
    clock = pygame.time.Clock()
    
    background = pygame.image.load(os.path.join(scriptDir, 'assets', 'ogrod.jpg'))
    shoot_rate = 45
    
    scoreCooldown = 0
    scoreRate = 30
    
    zombie_cooldown = 0
    zombie_rate = 60
    
    while run:
        clock.tick(60) 
        elapsed_time += 1/60 
        pygame.time.Clock().tick(60)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False
            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart the game
                        return main()
                    elif event.key == pygame.K_q:
                        run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
               if peaShooterCard_rect.collidepoint(event.pos) and sunCurrency >= 100:
                   placing_peashooter = True  # Activate placement mode
                   peashooter_card.set_alpha(180)  # Make card semi-transparent
               
               elif placing_peashooter:  # Click on tiles to place
                   mouse_x, mouse_y = event.pos
                   # Find which tile was clicked
                   clicked_col = None
                   clicked_row = None
                   
                   for col in range(tile_cols):
                       if grid_start_x + col * tile_width <= mouse_x < grid_start_x + (col + 1) * tile_width:
                           clicked_col = col
                           break
                   
                   for row in range(tile_rows):
                       if grid_start_y + row * tile_height <= mouse_y < grid_start_y + (row + 1) * tile_height:
                           clicked_row = row
                           break
                   
                   # Place peashooter if valid tile
                   if clicked_col is not None and clicked_row is not None:
                       if (clicked_col, clicked_row) not in occupied_tiles:
                           x, y = tile_positions[(clicked_col, clicked_row)]
                           occupied_tiles[(clicked_col, clicked_row)] = peashooter(x, y)
                       sunCurrency -= 100
                       placing_peashooter = False
                       peashooter_card.set_alpha(255)  # Restore card to full opacity
        
        keys = pygame.key.get_pressed()
        
        if not game_over:
            # Update each peashooter's shooting
            for tile_pos, pea in occupied_tiles.items():
                if pea.shoot_cooldown > 0:
                    pea.shoot_cooldown -= 0.5

                # Check if this specific peashooter can shoot
                if pea.shoot_cooldown == 0:
                    # Check if any zombie is in this peashooter's lane
                    for zomb in zombies:
                        if abs(zomb.y_cord - pea.y_cord) < 100:  # Same row
                            peaballs.append(peaBall(pea))
                            pea.shoot_cooldown = shoot_rate  # Reset cooldown
                            break
            
            # Spawn zombies
            if zombie_cooldown > 0:
                zombie_cooldown -= 0.5
            
            if zombie_cooldown == 0:
                wave_count = get_wave_count(elapsed_time)
                for _ in range(wave_count):
                    random_row = randint(0, tile_rows - 1)
                    y = grid_start_y + random_row * tile_height
                    zombies.append(zombie(y))
                
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
                # Check if zombie reached the house (behind peashooters)
                if zomb.x_cord < 200:
                    game_over = True
                if zomb.x_cord < 0:
                    if zomb in zombies:
                        zombies.remove(zomb)
            
            if scoreCooldown > 0:
                scoreCooldown -= 1
            
            if scoreCooldown == 0:
                score += 1
                scoreCooldown = scoreRate
            
        window.blit(background,(0,0))
        window.blit(peashooter_card, peaShooterCard_rect)
        
        for peaball in peaballs:
            peaball.draw()
        
        for zomb in zombies:
            zomb.draw()
        
        for peaball in peaballs:
            pygame.draw.rect(window, (0, 100, 255), peaball.hitbox, 2)
        
        for zomb in zombies:
            pygame.draw.rect(window, (0, 255, 0), zomb.hitbox, 2)
        
        # Draw tile hitboxes
        # for col in range(tile_cols):
        #     for row in range(tile_rows):
        #         x = grid_start_x + col * tile_width
        #         y = grid_start_y + row * tile_height
        #         tile_rect = pygame.Rect(x, y, tile_width, tile_height)
        #         pygame.draw.rect(window, (255, 0, 0), tile_rect, 1)
        
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(score_text, (20, 20))
        
        sunCurrency_text = font.render(f"Suns: {sunCurrency}", True, (255, 255, 255))
        window.blit(sunCurrency_text, (20, 75))
        
        for tile_pos, pea in occupied_tiles.items():
            pea.draw()
        
        if placing_peashooter:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if cursor is in any tile
            for col in range(tile_cols):
                for row in range(tile_rows):
                    if (grid_start_x + col * tile_width <= mouse_x < grid_start_x + (col + 1) * tile_width and
                        grid_start_y + row * tile_height <= mouse_y < grid_start_y + (row + 1) * tile_height):
                        if (col, row) not in occupied_tiles:
                            preview_image = pygame.image.load(os.path.join(scriptDir, 'assets', 'peashooterZsk.png'))
                            preview_image = pygame.transform.scale(preview_image, (80, 80))
                            preview_image.set_alpha(180)  # 50% transparent
                            x, y = tile_positions[(col, row)]
                            window.blit(preview_image, (x, y))  # Show at tile position
                        break
        
        # Display game over screen
        if game_over:
            overlay = pygame.Surface((1400, 600))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            window.blit(overlay, (0, 0))
            
            game_over_text = bigFont.render("GAME OVER", True, (255, 0, 0))
            final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
            restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
            
            game_over_rect = game_over_text.get_rect(center=(700, 200))
            score_rect = final_score_text.get_rect(center=(700, 300))
            restart_rect = restart_text.get_rect(center=(700, 400))
            
            window.blit(game_over_text, game_over_rect)
            window.blit(final_score_text, score_rect)
            window.blit(restart_text, restart_rect)
        
        pygame.display.update()

if __name__== "__main__":
    main()